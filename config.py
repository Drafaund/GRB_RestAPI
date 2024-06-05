# config.py
import getpass

DATABASE = {
    'dbname': 'GRB_DB',
    'user': input("Enter PostgreSQL username: "),
    'password': getpass.getpass("Enter PostgreSQL password: "),
    'host': 'localhost',
    'port': 5432
}


# DATABASE = {
#     'dbname': 'GRB_DB',
#     'user': 'postgres',
#     'password': 'alter',
#     'host': 'localhost',
#     'port': 5432
# }
