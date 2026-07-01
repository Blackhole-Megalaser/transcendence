## Currently implemented API endpoints

GET /api/
Default page, contain only a link to **/api/users/**

### /api/users/

GET /api/users/
Returns the Userlist				[require to be logged as admin]

Possible Actions on **/api/users/**

	GET /api/users/me/
	Redirect to your user api page	[require to be logged]

	POST /api/users/login/
	Tries to log with the provided credentials

	POST /api/users/logout/
	Self explicit Logout

/api/users/root/					[require to be logged as admin]
Returns information specific to a user (here root as an exemple)

**API route below only allow for a user to see their own info, they require you to be logged in**

/api/users/root/tplace
Returns tplace informations for 'root'

/api/users/root/nyancoins
Returns the amount a nyancoins for 'root'

/api/users/root/colors
Returns the unlocked color lists for 'root'

/api/users/root/pixels
Returns the pixel info  for 'root'

/api/users/root/max-pixels
Returns only the 'maxPlaceablePixels' field for 'root'

/api/tplace/upgrades/max-pixels/        [POST, require logged in]
Buy max placable pixels with nyancoins. Payload: {"quantity": 1}
Cost: 150 nyancoins per +1 max placable pixel. Multiple pixels can be bought at once.
Returns updated tplace economy fields and nyancoins_spent.

/api/tplace/upgrades/regeneration-delay/        [POST, require logged in]
Buy pixel regeneration cooldown reductions with nyancoins. Payload: {"quantity": 1}
Each unit reduces regeneration_delay by 1 second.
Cooldown cannot be reduced below 15 seconds.
Cost starts at 300 nyancoins, then increases by 10% for each cooldown upgrade already bought and each additional unit in the same request.
Returns updated tplace economy fields and nyancoins_spent.
