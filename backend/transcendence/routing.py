from django.urls import re_path

from chat import consumers as chat
from skribble import consumers as skribble
from tplace import consumers as tplace

# fmt: off
websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>[\w-]+)/$", chat.ChatConsumer.as_asgi()),
    re_path(r"ws/skribble/(?P<room_name>[\w-]+)/$", skribble.SkribbleConsumer.as_asgi()),
    re_path(r"ws/tplace/(?P<room_name>[\w-]+)/$", tplace.TplaceConsumer.as_asgi()),
]
# fmt: on
