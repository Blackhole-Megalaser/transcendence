from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from rest_framework.test import APIClient

from .models import SkribblePlayer, SkribbleRoom, Word, WordList

TEST_CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    },
}


@override_settings(CHANNEL_LAYERS=TEST_CHANNEL_LAYERS)
class SkribbleRoomApiTests(TestCase):
    def setUp(self):
        self.wordlist, _ = WordList.objects.get_or_create(name="basic")
        self.words = [
            Word.objects.create(word=f"word {index}", list=self.wordlist)
            for index in range(1, 10)
        ]
        self.host_user = User.objects.create_user(username="host", password="pass")
        self.guest_user = User.objects.create_user(username="guest", password="pass")

        self.host = APIClient()
        self.host.force_login(self.host_user)
        self.guest = APIClient()
        self.guest.force_login(self.guest_user)

    def create_room(self, name="Room"):
        response = self.host.post("/api/skribble/rooms/", {"name": name}, format="json")
        self.assertEqual(response.status_code, 201)
        return response.data["code"]

    def join_guest(self, code):
        response = self.guest.post(
            f"/api/skribble/rooms/{code}/join/", {}, format="json"
        )
        self.assertEqual(response.status_code, 200)

    def start_game(self, code):
        response = self.host.post(
            f"/api/skribble/rooms/{code}/start_game/", {}, format="json"
        )
        self.assertEqual(response.status_code, 200)
        return SkribbleRoom.objects.get(code=code)

    def client_for_player(self, player):
        if player.player.user_id == self.host_user.id:
            return self.host
        return self.guest

    def other_client_for_player(self, player):
        if player.player.user_id == self.host_user.id:
            return self.guest
        return self.host

    def current_drawer(self, room):
        return SkribblePlayer.objects.get(room=room, order=room.current_player_index)

    def test_only_host_can_start_and_requires_two_players(self):
        code = self.create_room()

        response = self.host.post(
            f"/api/skribble/rooms/{code}/start_game/", {}, format="json"
        )
        self.assertEqual(response.status_code, 400)

        self.join_guest(code)
        response = self.guest.post(
            f"/api/skribble/rooms/{code}/configure/",
            {"max_rounds": 4},
            format="json",
        )
        self.assertEqual(response.status_code, 403)

        response = self.host.post(
            f"/api/skribble/rooms/{code}/configure/",
            {"max_rounds": 2},
            format="json",
        )
        self.assertEqual(response.status_code, 400)

        response = self.host.post(
            f"/api/skribble/rooms/{code}/configure/",
            {"max_rounds": 4},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["max_rounds"], 4)

        response = self.guest.post(
            f"/api/skribble/rooms/{code}/start_game/", {}, format="json"
        )
        self.assertEqual(response.status_code, 403)

        response = self.host.post(
            f"/api/skribble/rooms/{code}/start_game/", {}, format="json"
        )
        self.assertEqual(response.status_code, 200)
        room = SkribbleRoom.objects.get(code=code)
        self.assertTrue(room.game_started)
        self.assertFalse(room.game_finished)
        self.assertEqual(room.max_rounds, 4)
        self.assertEqual(room.host, self.host_user.userprofile)

    def test_guess_scores_and_masks_word_for_guessers(self):
        code = self.create_room()
        self.join_guest(code)
        room = self.start_game(code)
        drawer = self.current_drawer(room)
        drawer_client = self.client_for_player(drawer)
        guesser_client = self.other_client_for_player(drawer)

        response = drawer_client.post(
            f"/api/skribble/rooms/{code}/start_turn/",
            {"word": self.words[0].word},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["word"], self.words[0].word)
        self.assertEqual(response.data["word_mask"], "____ _")

        response = guesser_client.get(f"/api/skribble/rooms/{code}/state/")
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.data["word"])
        self.assertEqual(response.data["word_mask"], "____ _")

        response = guesser_client.post(
            f"/api/skribble/rooms/{code}/guess/",
            {"guess": self.words[0].word.upper()},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["correct"])
        self.assertTrue(response.data["turn_ended"])
        self.assertEqual(response.data["points"], 200)
        self.assertGreater(response.data["drawer_points"], 0)

        room.refresh_from_db()
        self.assertFalse(room.turn_started)
        self.assertIsNone(room.current_word)
        self.assertFalse(room.game_finished)

    def test_game_finishes_after_three_draws_per_player_and_replay_resets(self):
        code = self.create_room()
        self.join_guest(code)
        room = self.start_game(code)

        for turn_index in range(6):
            room.refresh_from_db()
            drawer = self.current_drawer(room)
            drawer_client = self.client_for_player(drawer)
            response = drawer_client.post(
                f"/api/skribble/rooms/{code}/start_turn/",
                {"word": self.words[turn_index].word},
                format="json",
            )
            self.assertEqual(response.status_code, 200)
            response = drawer_client.post(
                f"/api/skribble/rooms/{code}/end_turn/", {}, format="json"
            )
            self.assertEqual(response.status_code, 200)

        room.refresh_from_db()
        self.assertFalse(room.game_started)
        self.assertTrue(room.game_finished)
        self.assertEqual(room.round_counter, 3)

        response = self.host.post(
            f"/api/skribble/rooms/{code}/replay/",
            {"max_rounds": 4},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        room.refresh_from_db()
        self.assertTrue(room.game_started)
        self.assertFalse(room.game_finished)
        self.assertEqual(room.round_counter, 1)
        self.assertEqual(room.max_rounds, 4)
        self.assertEqual(list(room.players.values_list("score", flat=True)), [0, 0])
