"""This file contians helpful python commands to create databases and tables
If run as main: 
This file creates a new database called Appliction. 
In the Application database it creates a new table called users. 
The users table contains a userid (int) a username (varchar(255)) and a password(varchar(255))
The password field stores a salted hash of the users password.
"""
import mysql.connector
import os #required to read env varibles to login to the mysql db
import uuid #required to generate uuids
import hashlib #required to generate hashes

user = os.environ.get('MYSQL_USER','root')
"""The MySQL Username"""
password = os.environ.get('MYSQL_PASSWORD','admin')
"""The MySQL Password"""
host = os.environ.get('MYSQL_HOST','localhost')
"""The MySQL Host"""

def create_db(name:str) -> bool:
    """This function creates a new database of specified name
    
    | Args:
    |     name (str): The name of the new Database
    | 
    | Returns:
    |     bool: True if successful. Otherwise False.

    """
    try:
        database = mysql.connector.connect(host = host, user = user, passwd = password)
        cursor = database.cursor()
        cursor.execute(f'CREATE DATABASE {name}')
        database.close()
        return True
    except:
        return False

def create_table(database_name:str, table_name:str, feilds:str) -> bool:
    """This function creates a new table of specified name and feilds inside the specified database
    
    | Args:
    |     database_name (str): The name of the database
    |     table_name (str): The name of the table
    |     fields (str): The name of the database
    | 
    | Returns:
    |     bool: True if successful. Otherwise False.

    """
    try:
        database = mysql.connector.connect(host = host, user = user, passwd = password, database = database_name)
        cursor = database.cursor()
        cursor.execute(f'CREATE TABLE {table_name} {feilds}')
        database.close()
        return True
    except:
        return False
    
def insert_user(username:str, planetext_password:str,database_name:str) -> bool:
    """This function inserts specified user into the user table. 

     The function will create a unquie id using uui4 and will hash and salt the plaintext password.
    
    | Args:
    |     username (str): The username to be added (usernames must be unquie)
    |     planetext_password (str): The plain text password to be added
    |     database_name (str): The name of the database
    | 
    | Returns:
    |     bool: True if successful. Otherwise False.
    """
    try:
        database = mysql.connector.connect(host = host, user = user, passwd = password, database = database_name)
        cursor = database.cursor()
        unq_id = uuid.uuid4().int % 2147483647 #This generates a random unquie id
        salt = hashlib.sha256((str(unq_id)+username).encode())
        hashed_password = hashlib.sha256((planetext_password+salt.hexdigest()).encode())#This line salts and hashes the users plaintext password
        hashed_password_hex = hashed_password.hexdigest()
        sql = "INSERT INTO users (userid, username, password) VALUES (%s, %s, %s)"
        val = (unq_id,username,hashed_password_hex)
        cursor.execute(sql, val)
        database.commit()
        database.close()
        return True
    except Exception as e:
        print(e)
        return False

if __name__ == '__main__':
    create_db('Application')
    create_table('Application','users','(userid int NOT NULL UNIQUE, username varchar(255) UNIQUE, password varchar(255))')
    insert_user('Username', 'Password','Application')