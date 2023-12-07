from mydbaids.initializer import Initializer
from mydbaids.db.interface import DBInterface
from mydbaids.cli.connect import ConnectorCLI
from mydbaids.cli.scripting import RealTimeCLI


def main():
    connector = ConnectorCLI()
    connector.connect()
    interface = DBInterface(connector.user, connector.password, connector.host, connector.database)
    RealTimeCLI().run(interface)

 
if "__main__" == __name__:
    Initializer()
    main()
