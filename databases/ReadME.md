
To access the vizulized database in your browser go to localhost:8080 
Login using root:admin 

To change the credentials update the password in the mySQL docker file

To populate the database with a test user
On the server running the backend 
`cd scripts`
`python create_user_table.py`

This will create an Appliction database and the create a User table in that database it will populate it with a user
The dummy user credentials are Username:Password