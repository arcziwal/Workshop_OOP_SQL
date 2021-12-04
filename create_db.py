from psycopg2 import connect, OperationalError
from psycopg2.errorcodes import DUPLICATE_DATABASE, DUPLICATE_TABLE

user='postgres'
password = 'coderslab'
create_db_sql = """CREATE DATABASE workshop;"""
create_table_users_sql = """CREATE TABLE users
(
    id serial,
    username varchar(255) unique,
    hashed_password varchar(80),
    PRIMARY KEY(id)
);
"""
create_table_messages_sql = """CREATE TABLE messages
(
    id serial,
    FOREIGN KEY(id)
    REFERENCES users(id),
    creation_date timestamp,
    text varchar(255),
    PRIMARY KEY(id)
);
"""

try:
    cnx = connect(user=user, password=password, host='localhost')
    print("Connection established")
    cursor = cnx.cursor()
    cnx.autocommit = True
    cursor.execute(create_db_sql)
    cursor.close()
    cnx.close()
    cnx = connect(user=user, password=password, host='localhost', database='workshop')
    cursor = cnx.cursor()
    cnx.autocommit = True
    cursor.execute(create_table_users_sql)
    cursor.execute(create_table_messages_sql)
except OperationalError as e:
    if e.pgcode == DUPLICATE_DATABASE:
        print("Requested database already exists")
    elif e.pgcode == DUPLICATE_TABLE:
        print("Requested table already esist")
    print(f"Connection cannot be established. {e}")
else:
    cursor.close()
    cnx.close()
