## How to reach the database (from inside the db container)

First enter the container

`docker exec -it transcendance-db-1 bash`

Then switch to the default postgres user

`su postgres`

Finally use the psql command to connect

`psql -U djangouser transcendence`

(**djangouser** as the user you're connecting with and **transcendence** as the database name)

Once in postgres, use **\d** to list relations, **\du** to see the database users

To see the user list:

`SELECT * FROM auth_user;` (django users)
`SELECT * FROM back_userprofile;` (userprofile as defined in models.py)