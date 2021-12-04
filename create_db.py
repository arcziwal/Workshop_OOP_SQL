from psycopg2 import connect, OperationalError
from psycopg2.errorcodes import DUPLICATE_DATABASE

user='postgres'
password = 'coderslab'

try:
    cnx = connect(user=user, password=password, host='localhost')
    print("Nawiązano połączenie")
    pass
except OperationalError as e:
    if e.pgcode == DUPLICATE_DATABASE:
        print("Istnieje już taka baza danych")
    print("Nie udało się nawiązać połączenia")




