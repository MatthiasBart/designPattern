# Factory-Class-Beispiel

# Connection-Klassen:
from abc import ABC, abstractmethod

class Database(ABC):
    def __init__(self, path):
        self.path = path
        self.conn()

    @abstractmethod
    def conn(self):
        pass

    @abstractmethod
    def disconn(self):
        pass

class OracleDatabase(Database):

    def __init__(self, path):
        super().__init__(path)

    def conn(self):
        print("connect to Oracle")

    def disconn(self):
        print("disconnect from Oracle")

class MicrosoftDatabase(Database):

    def __init__(self, path):
        super().__init__(path)

    def conn(self):
        print("connect to Microsoft")
    
    def disconn(self):
        print("disconnect from Microsoft")

# Factory-Klasse:

class ConnectionCreator():

    def __init__(self):
        pass

    @staticmethod
    def build_connection(connection_type, path):

        if connection_type == "Oracle":
            return OracleDatabase(path)

        elif connection_type == "Microsoft":
            return MicrosoftDatabase(path)

        else:
              return None
        
    
oracleConnection = ConnectionCreator.build_connection("Oracle", "path")
oracleConnection.disconn()

microsoftConnection = ConnectionCreator.build_connection("Microsoft", "path")
microsoftConnection.disconn()