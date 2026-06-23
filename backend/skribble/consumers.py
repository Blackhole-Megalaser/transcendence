import json
import uuid
from datetime import datetime, timezone

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings
from redis import asyncio as redis

_redis_client = None
ROOM_HISTORIES = {}


def get_redis_client():
    global _redis_client

    if _redis_client is None:
        _redis_client = redis.from_url(
            settings.SKRIBBLE_REDIS_URL, decode_responses=True
        )

    return _redis_client


class SkribbleConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        self.history_key = f"chat:session:{self.room_name}:messages"

        if self.room_name not in ROOM_HISTORIES:
            ROOM_HISTORIES[self.room_name] = [
                {"type": "fill", "x": 0, "y": 0, "color": "#ffffff"}
            ]

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        await self.send_history()
        await self.send(
            text_data=json.dumps(
                {"type": "canvas.init", "history": ROOM_HISTORIES[self.room_name]}
            )
        )

    # Leave room group
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):

        # Handle text JSON message
        if text_data:
            try:
                text_data_json = json.loads(text_data)
            except json.JSONDecodeError:
                return

            action = text_data_json.get("action")

            if action == "send_drawing":
                payload = text_data_json.get("payload")

                history = ROOM_HISTORIES.get(self.room_name, [])

                if payload.get("type") == "clear":
                    ROOM_HISTORIES[self.room_name] = [
                        {"type": "fill", "x": 0, "y": 0, "color": "#ffffff"}
                    ]
                elif payload.get("type") == "undo":
                    if len(history) > 1:
                        history.pop()
                elif payload.get("type") == "paint":
                    if (
                        history
                        and history[-1].get("type") == "paint"
                        and history[-1].get("id") == payload.get("id")
                    ):
                        history[-1]["points"].extend(payload.get("points", []))
                    else:
                        history.append(payload)
                else:
                    history.append(payload)

                await self.channel_layer.group_send(
                    self.room_group_name, {"type": "canvas.update", "payload": payload}
                )
                return

            text = text_data_json.get("message", "").strip()
            if not text:
                return

            text = text[: settings.CHAT_MESSAGE_MAX_LENGTH]
            message = await self.build_message(text)
            serialized_message = json.dumps(message)

            redis_client = get_redis_client()
            await redis_client.rpush(self.history_key, serialized_message)
            await redis_client.ltrim(
                self.history_key, -settings.SKRIBBLE_HISTORY_LIMIT, -1
            )
            await redis_client.expire(self.history_key, settings.SKRIBBLE_HISTORY_TTL)

            await self.channel_layer.group_send(
                self.room_group_name, {"type": "chat.message", "message": message}
            )

    async def canvas_update(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "type": "canvas.update",
                    "payload": event.get("payload"),
                }
            )
        )

    async def chat_message(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "type": "message",
                    "message": event["message"],
                }
            )
        )

    async def send_history(self):
        redis_client = get_redis_client()
        raw_messages = await redis_client.lrange(
            self.history_key, -settings.SKRIBBLE_HISTORY_LIMIT, -1
        )
        messages = []

        for raw_message in raw_messages:
            try:
                messages.append(json.loads(raw_message))
            except json.JSONDecodeError:
                continue

        await self.send(
            text_data=json.dumps(
                {
                    "type": "history",
                    "messages": messages,
                }
            )
        )

    @sync_to_async
    def build_message(self, text):
        user = self.scope.get("user")
        author = "anonymous"
        image = None

        if user is not None and user.is_authenticated:
            author = user.username
            image = user.userprofile.profile_image

        return {
            "id": str(uuid.uuid4()),
            "author": author,
            "text": text,
            "picture": str(image.url) if image else None,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
