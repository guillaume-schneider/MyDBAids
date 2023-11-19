from mysqlgen.initializer import Initializer
from mysqlgen.db.interface import DBInterface


def main():
    interface = DBInterface("root", "", "localhost", "firefighter").init()
    interface.inject(10)

 
if "__main__" == __name__:
    Initializer()
    main()
