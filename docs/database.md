## How to reach the database (from outside) [DEV ONLY]

To use this method, you have to expose your database container to the outside, only use this during development.

The form is as follows:

`psql -U yourPostgresUser -h yourHostname -p portExposed -d databaseName`

If you are using the default values from the .env.example, it would look like this

`psql -U djangouser -h localhost -p 5432 -d transcendence`

The exposed port may differ depending on redirections between host machine and docker container

You will get prompted for the database password (located in your env file)

## How to reach the database (from inside the db container)

First enter the container

`docker exec -it transcendance-db-1 bash`

Then switch to the default postgres user

`su postgres`

Finally use the psql command to connect

`psql -U djangouser transcendence`

(**djangouser** as the user you're connecting with and **transcendence** as the database name)

## How to consults the database after logging in

Once in postgres, use **\d** to list relations, **\du** to see the database users

To see the user list:

`SELECT * FROM auth_user;` (django users)

`SELECT * FROM back_userprofile;` (userprofile as defined in models.py)

To give nyancoins to user 1:

`UPDATE back_userprofile SET nyancoins = 200 WHERE id=1 ;`
