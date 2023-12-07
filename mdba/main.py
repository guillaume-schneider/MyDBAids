from mdba.initializer import Initializer
from mdba.db.interface import DBInterface
from mdba.cli.connect import ConnectorCLI
from mdba.cli.scripting import RealTimeCLI


def main():
    connector = ConnectorCLI()
    connector.connect()
    interface = DBInterface(connector.user, connector.password, connector.host, connector.database)
    RealTimeCLI().run(interface)

 
if "__main__" == __name__:
    Initializer()
    main()
