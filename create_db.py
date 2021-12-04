from psycopg2 import connect, OperationalError
from psycopg2.errorcodes import DUPLICATE_DATABASE, DUPLICATE_TABLE

user='postgres'
password = 'coderslab'
create_db_sql = """CREATE DATABASE Workshop;"""
create_table_sql = """CREATE TABLE users
(
    id serial,
    username varchar(255) unique,
    hashed_password varchar(80),
    PRIMARY KEY(id)
);
"""

try:
    cnx = connect(user=user, password=password, host='localhost')
    print("Connection established")
    cursor = cnx.cursor()
    cursor.execute(create_db_sql)
    cnx.commit()
    cursor.execute(create_table_sql)
    cnx.commit()
except OperationalError as e:
    if e.pgcode == DUPLICATE_DATABASE:
        print("Requested database already exists")
    elif e.pgcode == DUPLICATE_TABLE:
        print("Requested table already esist")
    print("Connection cannot be established")





