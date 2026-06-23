import json
import random
from channels.generic.websocket import AsyncWebsocketConsumer

class GameConsumer(AsyncWebsocketConsumer):
    # Liste temporaire des joueurs connectés dans ce salon (en production, utilisez Redis ou la DB)
    connected_players = {}

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_code']
        self.room_group_name = f'game_{self.room_name}'

        # Rejoindre le groupe de la pièce
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Quitter le groupe
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Réception d'un message envoyé par UN client VueJS
    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')

        if action == 'join_game':
            # On enregistre le joueur dans ce salon
            username = data.get('username')
            if self.room_group_name not in self.connected_players:
                self.connected_players[self.room_group_name] = []
            if username not in self.connected_players[self.room_group_name]:
                self.connected_players[self.room_group_name].append(username)

        elif action == 'start_game':
            players = self.connected_players.get(self.room_group_name, [])
            if players:
                # Le serveur choisit le premier dessinateur au hasard
                first_painter = random.choice(players)
                
                # On envoie l'information à TOUT LE MONDE dans le groupe
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'broadcast_game_start',
                        'painter': first_painter
                    }
                )

    # Cette méthode est appelée par group_send (diffusion générale)
    async def broadcast_game_start(self, event):
        # Envoi effectif du message JSON au navigateur (VueJS)
        await self.send(text_data=json.dumps({
            'status': 'game_started',
            'current_painter': event['painter']
        }))