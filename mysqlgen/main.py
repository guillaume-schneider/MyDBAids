from mysqlgen.initializer import Initializer
from mysqlgen.db.interface import DBInterface


def main():
    DBInterface("root", "", "localhost", "firefighter").init()

 
if "__main__" == __name__:
    Initializer()
    main()
