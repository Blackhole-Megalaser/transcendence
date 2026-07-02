## Currently implemented API endpoints

GET /api/
Default page, contain only a link to **/api/users/**

### USERS API /api/users/

GET /api/users/
Returns the Userlist				[requires to be logged as admin]

Possible Actions on **/api/users/**

**A user can only consult his own data, looking for anyone else information requires to be admin**

#### Unauthenticated requests

	POST /api/users/login/
	Tries to log with the provided credentials
	Payload: {"username":"userHere", "password":"topSecret"}

	POST /api/users/signup/
	Tries to signup with the provided credentials

#### Authenticated requests

	POST /api/users/logout/
	Self explicit Logout

	GET /api/users/me/
	Redirect to your user api page

	POST /api/users/me/change_email
	Tries to change the email with the provided one if it is valid
	Payload: {"email":"newmail@adress.com"}

	GET /api/users/root/
	Returns information specific to a user (here root as an exemple)

	GET /api/users/root/tplace
	Returns tplace informations for 'root'

	GET /api/users/root/nyancoins
	Returns the amount a nyancoins for 'root'

	GET /api/users/root/colors
	Returns the unlocked color lists for 'root'

	GET /api/users/root/pixels
	Returns the pixel info for 'root'

	GET /api/users/root/max-pixels
	Returns only the 'maxPlaceablePixels' field for 'root'

	POST /api/tplace/upgrades/max-pixels/
	Buy max placable pixels with nyancoins. Payload: {"quantity": 1}
	Cost: 150 nyancoins per +1 max placable pixel. Multiple pixels can be bought at once.
	Returns updated tplace economy fields and nyancoins_spent.

	POST /api/tplace/upgrades/regeneration-delay/
	Buy pixel regeneration cooldown reductions with nyancoins. Payload: {"quantity": 1}
	Each unit reduces regeneration_delay by 1 second.
	Cooldown cannot be reduced below 15 seconds.
	Cost starts at 300 nyancoins, then increases by 10% for each cooldown upgrade already bought and each additional unit in the same request.
	Returns updated tplace economy fields and nyancoins_spent.

	GET /api/users/me/avatar/
	Returns the avatar url

	POST /api/users/me/avatar/
	Update your avatar with the given image and send the new avatar url

	GET /api/users/me/friends
	Returns the friendlist and current pending friend requests

	GET /api/users/me/friendlist
	Returns the friendlist

	GET /api/users/me/friends_request
	Returns the pending friend requests

	POST /api/users/me/friends_request
	Execute the action on the friends for the given user
		- `send` to send a friend request
		- `accept` to accept a friend request
		- `reject` to reject a friend request
		- `remove_friend` to remove someone from your friendlist
	Payload: {"action":"send", "password":"topSecret"}

### WORDLIST API

This route can be accessed without authentication.

	GET /api/wordlists
	Returns every wordlist, the list name and the associated words


### TPLACE API

	GET /api/tplace/canvas/		[no auth required]

	POST /api/tplace/giveme/	[requires to be admin]
	Add the given number of nyancoins to the current (admin) user

### SKRIBBLE API

#### SKRIBBLE ROOMS

- `POST /api/skribble/rooms/`
  - Create a room and join it.
  - Payload can include `name` and optional `max_rounds`.
  - `max_rounds` minimum is `3`.

- `POST /api/skribble/rooms/<code>/join/`
  - Join a waiting room.
  - Fails once the game is started or finished.

- `POST /api/skribble/rooms/leave/`
  - Leave current room.
  - If host leaves, backend assigns the next player as host.
  - If drawer leaves during a turn, backend ends the turn without awarding points.

- `POST /api/skribble/rooms/<code>/start_game/`
  - Host only.
  - Requires at least 2 players.

- `POST /api/skribble/rooms/<code>/configure/`
  - Host only.
  - Only allowed before the game starts.
  - Payload: `{ "max_rounds": 3 }` or higher.

- `GET /api/skribble/rooms/<code>/state/`
  - Source of truth for current room/game state.
  - Drawer receives `word`; guessers receive `word: null` and `word_mask` as underscores.

- `GET /api/skribble/rooms/<code>/select_word/`
  - Current drawer only.
  - Returns 3 possible words before the turn starts.

- `POST /api/skribble/rooms/<code>/start_turn/`
  - Current drawer only.
  - Payload: `{ "word": "chosen word" }`.

- `POST /api/skribble/rooms/<code>/guess/`
  - Guessers only.
  - Payload: `{ "guess": "message text" }`.
  - If correct, do not display the guessed word in chat; show a system message instead.

- `POST /api/skribble/rooms/<code>/end_turn/`
  - Host, drawer, or expired timer.
  - Payload can be `{ "reason": "manual" }`.

- `POST /api/skribble/rooms/<code>/replay/`
  - Host only.
  - Keeps the room and starts a new game.
  - Payload can include optional `{ "max_rounds": 4 }`.
