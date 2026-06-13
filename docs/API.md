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
