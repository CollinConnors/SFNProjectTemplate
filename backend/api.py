"""The backend API for the MintBlockchain Applictaion

This modules uses Falcon
"""

#---------------IMPORT-----------------
#Base Libs
import os
import hashlib
import sys #For Debugging
import traceback #For Debugging

#Installed Libs
import falcon.asgi
from falcon_auth2 import AuthMiddleware
from falcon_auth2 import HeaderGetter
from falcon_auth2.backends import BasicAuthBackend
from falcon_auth2.backends import GenericAuthBackend
from falcon_auth2.backends import JWTAuthBackend
from falcon_auth2.backends import MultiAuthBackend
import mysql.connector
from authlib.jose import jwt as java_web_token

#Set Database Configurations
mysql_user = os.environ.get('MYSQL_USER','root')
"""The MySQL Username"""
mysql_password = os.environ.get('MYSQL_PASSWORD','admin')
"""The MySQL Password"""
mysql_host = os.environ.get('MYSQL_HOST','localhost')
"""The MySQL Host"""

#Set Authentication Configurations
auth_database = 'Application'
auth_table = 'users'
key = "a-secret-key" #This needs to be random

#--------------AUTHENTICATION METHODS--------

def make_token(username:str) -> bytes:
    """Generates a simple JWT from a given username

        | Args:
        |     username (str): The username
        | 
        | Returns:
        |     bytes: The JWT token issued
    """
    payload = {
        "sub": username,
        "iss": "an issuer",
        "aud": "an aud",
        "iat": 1609459200,
        "nbf": 1609459200,
        "exp": 1924992000,
    }
    token = java_web_token.encode({"alg": "HS256"}, payload, key)
    return(token)

async def authenticate(user:str, plaintexttext_password:str) -> bool:
    """Check if the user exists and the password matchs the database.
    
        | Args:
        |     user (str): The username
        |     plaintext_password (str): The users password in plaintext
        | 
        | Returns:
        |     bool: True if the user exists and the passwords match. Otherwise False
    """
    try:
        database = mysql.connector.connect(host = mysql_host, user = mysql_user, passwd = mysql_password, database = auth_database)
    except:
        return False
    cursor = database.cursor()
    cursor.execute(f"SELECT * FROM `{auth_table}` WHERE `username` = '{user}'")
    results = cursor.fetchall()
    database.close()
    if not len(results) == 1:
        return False
    person = results[0]
    unq_id = person[0]
    username = person[1]
    raw_hashed_password_hex = person[2]
    salt = hashlib.sha256((str(unq_id)+username).encode())
    hashed_password = hashlib.sha256((plaintexttext_password+salt.hexdigest()).encode())#This line salts and hashes the users plaintext password
    computed_hashed_password_hex = hashed_password.hexdigest()
    return(computed_hashed_password_hex == raw_hashed_password_hex)

async def basic_user_loader(attributes, user, password):
    if await authenticate(user, password):
        return {"username": user, "kind": "basic"}
    return None

async def jwt_user_loader(attributes, payload):
    # Perform additional authentication using the payload.
    # This is just an example
    if "sub" in payload:
        return {"username": payload["sub"], "kind": "jwt"}
    return None


#Create Authentication Backends
basic_backend = BasicAuthBackend(basic_user_loader)
jwt_backend = JWTAuthBackend(jwt_user_loader, key)
auth_backend = MultiAuthBackend((basic_backend, jwt_backend))
auth_middleware = AuthMiddleware(auth_backend)

#
#Set API Configurations
app = falcon.asgi.App(cors_enable=True, middleware=[auth_middleware])
base_url="/api/v1"
responseHeaders = {'Access-Control-Allow-Origin': '*'}
debug = True

#--------------API ENDPOINTS-----------------
#Endpoint URL = {base_url}/
class TestEndpoint:
    """Test if the server is alive
    
        Endpoint:
            {base_url}/

        Methods:
            GET, POST
    """
    auth = {"auth_disabled": True} #Required to disable authentication on this endpoint. By default authentication is required.
    async def on_get(self, req, resp):
        """Test if the server responds to GET requests
        
        | Endpoint: GET {base_url}/
        |
        | Responce:
        |   200:    
        |       {alive : True}
        |
        | Example Request:
        |   curl --request GET --url http://localhost/api/v1/ --user Username:Password
        |
        | Exampe Responce: 
        |    {
        |       "alive" : true
        |    }
        """
        try:
            resp.set_headers(responseHeaders)
            resp.media = {'alive':True}
            resp.status = falcon.HTTP_200
        except Exception as e:
            if debug:
                tb = sys.exc_info()[-1]
                print(f'ERROR:\tLine {traceback.extract_tb(tb, limit=1)[-1][1]} ---- {e}')
            resp.set_headers(responseHeaders)
            resp.media = {'ERROR':'Error on Test Endpoint'}
            resp.status = falcon.HTTP_404

    async def on_post(self, req, resp):
        """Test if the server responds to POST requests

        | Endpoint: POST {base_url}/
        |
        | Args:
        |     Arbitrary JSON
        | 
        | Responce:
        |   200:    
        |       Same JSON data sent by the user
        |
        | Example Request:
        |   curl --request POST --url http://localhost:443/api/v1/ --header 'Content-Type: application/json' --data '{"test":"test"}'
        |
        | Exampe Responce: 
        |    {
        |       "test" : "test"
        |    }
        """
        try:
            raw_data = await req.media
            resp.set_headers(responseHeaders)
            resp.media = raw_data
            resp.status = falcon.HTTP_200
        except Exception as e: #Use for debugging
            if debug:
                tb = sys.exc_info()[-1]
                print(f'ERROR:\tLine {traceback.extract_tb(tb, limit=1)[-1][1]} ---- {e}')
            resp.set_headers(responseHeaders)
            resp.media = {'ERROR':'Error on Test Endpoint'}
            resp.status = falcon.HTTP_404

#Endpoint URL = {base_url}/login
class Login:
    """Test if the server is alive
    
        Endpoint:
            {base_url}/login

        Methods:
            POST
    """
    auth = {"auth_disabled": True}
    async def on_post(self, req, resp):
        """Returns a JWT token for the user after validating the username and password

        | Endpoint: POST {base_url}/login
        |
        | Args:
        |     username: The username
        |     password: The password
        | 
        | Responce:
        |   200:
        |       A boolean representing if the authentication was succesful    
        |       A JWT Token that can be used later in the application
        |   401:
        |       False
        |
        | Example Request:
        |   curl --request POST --url http://localhost/api/v1/login --header 'Content-Type: application/json' --data '{"username":"Username","password":""Password}'
        |
        | Exampe Responce: 
        |   {
	    |     "success": true,
	    |     "jwt": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJVc2VybmFtZSIsImlzcyI6ImFuIGlzc3VlciIsImF1ZCI6ImFuIGF1ZCIsImlhdCI6MTYwOTQ1OTIwMCwibmJmIjoxNjA5NDU5MjAwLCJleHAiOjE5MjQ5OTIwMDB9.qSTfLP4VG5D0fkXIKczoNtb9aq0QPvZKQaE7RXdkPfs"
        |   }
        """
        try:
            raw_data = await req.media
            username = raw_data.get('username',None)
            password = raw_data.get('password',None)
            success = await authenticate(username,password)
            if not success:
                resp.set_headers(responseHeaders)
                resp.media = {"success":False}
                resp.status = falcon.HTTP_401
                return
            jwt = make_token(username)
            resp.set_headers(responseHeaders)
            resp.media = {"success":True,"jwt":str(jwt)[2:-1]} #
            resp.status = falcon.HTTP_200
        except Exception as e: #Use for debugging
            if debug:
                tb = sys.exc_info()[-1]
                print(f'ERROR:\tLine {traceback.extract_tb(tb, limit=1)[-1][1]} ---- {e}')
            resp.set_headers(responseHeaders)
            resp.media = {'ERROR':'Error on Login'}
            resp.status = falcon.HTTP_404

class HiddenEndpoint:
    """Test if the user is logged in
    
        Endpoint:
            {base_url}/hidden

        Methods:
            GET, POST
    """
    async def on_get(self, req, resp):
        """Test if the user is logged in with a GET request
        
        | Endpoint: GET {base_url}/hidden
        |
        | Responce:
        |   200:    
        |       {alive : True}
        |
        | Example Request:
        |   curl --request GET --url http://localhost/api/v1/hidden --user Username:Password
        |   curl --request GET --url http://localhost/api/v1/hidden --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJVc2VybmFtZSIsImlzcyI6ImFuIGlzc3VlciIsImF1ZCI6ImFuIGF1ZCIsImlhdCI6MTYwOTQ1OTIwMCwibmJmIjoxNjA5NDU5MjAwLCJleHAiOjE5MjQ5OTIwMDB9.S7fYq9S-vTNmL7H00hDw6gUNpT0lnPSDYFi2KzK83Wk'
        |
        | Exampe Responce: 
        |    {
        |       "alive" : true
        |    }
        """
        try:
            resp.set_headers(responseHeaders)
            resp.media = {'alive':True}
            resp.status = falcon.HTTP_200
        except Exception as e:
            if debug:
                tb = sys.exc_info()[-1]
                print(f'ERROR:\tLine {traceback.extract_tb(tb, limit=1)[-1][1]} ---- {e}')
            resp.set_headers(responseHeaders)
            resp.media = {'ERROR':'Error on Test Endpoint'}
            resp.status = falcon.HTTP_404

    async def on_post(self, req, resp):
        """Test if the user is logged in with a POST request

        | Endpoint: POST {base_url}/hidden
        |
        | Args:
        |     Arbitrary JSON
        | 
        | Responce:
        |   200:    
        |       Same JSON data sent by the user
        |
        | Example Request:
        |   curl --request POST --url http://localhost/api/v1/hidden --header 'Content-Type: application/json' --data '{"test":"test"}' --user Username:Password
        |   curl --request POST --url http://localhost/api/v1/hidden --header 'Content-Type: application/json' --data '{"test":"test"}' --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJVc2VybmFtZSIsImlzcyI6ImFuIGlzc3VlciIsImF1ZCI6ImFuIGF1ZCIsImlhdCI6MTYwOTQ1OTIwMCwibmJmIjoxNjA5NDU5MjAwLCJleHAiOjE5MjQ5OTIwMDB9.S7fYq9S-vTNmL7H00hDw6gUNpT0lnPSDYFi2KzK83Wk'
        |
        | Exampe Responce: 
        |    {
        |       "test" : "test"
        |    }
        """
        try:
            raw_data = await req.media
            resp.set_headers(responseHeaders)
            resp.media = raw_data
            resp.status = falcon.HTTP_200
        except Exception as e: #Use for debugging
            if debug:
                tb = sys.exc_info()[-1]
                print(f'ERROR:\tLine {traceback.extract_tb(tb, limit=1)[-1][1]} ---- {e}')
            resp.set_headers(responseHeaders)
            resp.media = {'ERROR':'Error on Test Endpoint'}
            resp.status = falcon.HTTP_404

#--------------ASSIGN ENDPOINTS--------------------
test_endpoint=TestEndpoint()
"""{base_url}/"""
login=Login()
"""{base_url}/login"""
hidden=HiddenEndpoint()
"""{base_url}/hidden"""

#--------------ASSIGN Routes--------------------
app.add_route(f'{base_url}/', test_endpoint)
app.add_route(f'{base_url}/login', login)
app.add_route(f'{base_url}/hidden', hidden)