from initializer import Initializer
from db.interface import DBInterface

def main():
    DBInterface("py", "py", "localhost", "firefighter").init()


if "__main__" == __name__:
    Initializer()
    main()
