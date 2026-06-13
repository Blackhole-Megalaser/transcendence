# Websocket

Websocket is a different protocol than HTTP. (ws://url or wss://url)

[Websocket wikipedia page](https://en.wikipedia.org/wiki/WebSocket)<br>
[Django tutorial about websockets](https://channels.readthedocs.io/en/latest/tutorial/index.html)<br>
[Websocket protocol RFC](https://datatracker.ietf.org/doc/html/rfc6455)

They are implemented through [**Daphne**](https://pypi.org/project/daphne/), a django compatible ASGI server (Asynchronous Server Gateway Interface), it can manage both HTTP and Websocket

Websockets are used for real-time application like the chat together with a redis layer to keep a cache/history. You can consider the redis instance like a pipe in standard bash (to simplify).