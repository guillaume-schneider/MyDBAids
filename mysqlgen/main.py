from mysqlgen.initializer import Initializer
from mysqlgen.db.interface import DBInterface
from mysqlgen.cli.connect import ConnectorCLI
from mysqlgen.cli.scripting import RealTimeCLI


def main():
    connector = ConnectorCLI()
    connector.connect()
    interface = DBInterface(connector.user, connector.password, connector.host, connector.database)
    RealTimeCLI().run(interface)

 
if "__main__" == __name__:
    Initializer()
    main()
