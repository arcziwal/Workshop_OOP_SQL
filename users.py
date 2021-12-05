import argparse
from models import User
from psycopg2 import OperationalError, connect
from psycopg2.errorcodes import UNIQUE_VIOLATION
from clcrypto import check_password

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password (min 8 characters)")
parser.add_argument("-n", "--new_pass", help="new password (min 8 characters)")
parser.add_argument("-l", "--list", help="list all users", action="store_true")
parser.add_argument("-d", "--delete", help="delete user", action="store_true")
parser.add_argument("-e", "--edit", help="edit user", action="store_true")


args = parser.parse_args()


def list_users(cursor):
    users = User.load_all_users(cursor)
    for user in users:
        print(user.username)


def create_user(cursor, username, password):
    if len(password) < 8:
        print("Password is tho short. It should have minimum 8 characters.")
    else:
        try:
            user = User(username=username, password=password)
            user.save_to_db(cursor)
            print("User created")
        except OperationalError as e:
            if e.pgcode == UNIQUE_VIOLATION:
                print("Użytkownik już istnieje")


def delete_user(cursor, username, password):
    user = User.load_user_by_username(cursor, username)
    if not user:
        print("Użytkownik nie istnieje")
    elif check_password(password, user.hashed_password):
        user.delete(cursor)
        print("Użytkownik usunięty")
    else:
        print("Błędne hasło")


def edit_user(cursor, username, password, new_pass):
    user = User.load_user_by_username(cursor, username)
    if not user:
        print("Użytkownik nie istnieje")
    elif check_password(password, user.hashed_password):
        if len(new_pass) < 8:
            print("Password is tho short. It should have minimum 8 characters.")
        else:
            user.hashed_password = new_pass
            user.save_to_db(cursor)
            print("Password changed.")
    else:
        print("Incorrect password")

if __name__ == "__main__":
    try:
        cnx = connect(database="workshop", user="postgres", password="coderslab", host='localhost')
        cnx.autocommit = True
        cursor = cnx.cursor()
        if args.username and args.password and args.edit and args.new_pass:
            edit_user(cursor, args.username, args.password, args.new_pass)
        elif args.username and args.password and args.delete:
            delete_user(cursor, args.username, args.password)
        elif args.username and args.password:
            create_user(cursor, args.username, args.password)
        elif args.list:
            list_users(cursor)
        else:
            parser.print_help()
        cursor.close()
        cnx.close()
    except ConnectionError as err:
        print("Błąd połączenia")