#########################################################
#           Implemntierung mit einer Factory class      #
#########################################################

class DatabaseConnection():
    def __init__(self, path, user, key):
        self.path = path
        self.user = user
        self.key = key
        self.lock = True

class DatabasePool():
    def __init__(self, max):
        self.instances = []
        self.max = max

    def get_connection(self, path, user, key) -> DatabaseConnection or None:
        # check for unlocked Connection
        for instance in self.instances:
            if instance.lock == False:
                instance.lock = True
                return instance
        # check if connections can be created
        if len(self.instances) < self.max:
            newDb = DatabaseConnection(path, user, key)
            self.instances.append(newDb)
            return newDb
        # if all 10 connections are used
        else:
            return None
        
    def unlock_conn(self, db: DatabaseConnection):
        for (index, instance) in enumerate(self.instances):
            if instance == db: 
                self.instances[index].lock = False

    
dbPool = DatabasePool(3)
db1 = dbPool.get_connection("path", "user", "key")
db2 = dbPool.get_connection("path", "user", "key")
db3 = dbPool.get_connection("path", "user", "key")
db4 = dbPool.get_connection("path", "user", "key")


dbPool.unlock_conn(db1)
# db1 = None 
# hier sollt man die Referenz auflösen aber aus anschauungszwecken wird die Ref beibehalten
print(db1.lock, db2.lock, db3.lock, db4)

db4 = dbPool.get_connection("path", "user", "key")

print(db1, db2, db3, db4)


#########################################################
#           Implmentierung mit __new__                  #
# folgende Ausführung ist nicht ganz funktionsfühig     #
#########################################################
class DatabaseConn():
    instances = []
    def __new__(cls, path, user, key):
        #check if unlocked connection is available
        for instance in cls.instances:
            if instance.lock == False:
                return instance
        # check if connections can be created   
        if len(cls.instances) < 3:
            obj = super().__new__(cls)
            return obj
        else: 
            return None
        
    def __init__(self, path, user, key):
        #check if self already exists
        if self in type(self).instances: 
            self.lock = True
            return
        
        self.path = path
        self.user = user
        self.key = key
        self.lock = True
        type(self).instances.append(self)

    def discard(self):
        for (index, instance) in enumerate(type(self).instances):
            if instance == self: 
                type(self).instances[index].lock = False           


db1 = DatabaseConn("path", "user", "key")
db2 = DatabaseConn("path", "user", "key")
db3 = DatabaseConn("path", "user", "key")
db4 = DatabaseConn("path", "user", "key")

print(db1.lock, db2.lock, db3.lock, db4)

##close the second one and open a 4th
db2.discard() # setzt lock auf false und macht connection frei 
# Referenz sollte aufgelöst werden aber unten sieht man das db2 gleich db4 ist
# d2 = None 

db4 = DatabaseConn("path", "user", "key")

print(db1.lock, db2, db3.lock, db4)


# Abstrahierte Multiton Basisklasse
class Multiton():
    instances = []
    def __new__(cls):
        #check if unlocked connection is available
        for instance in cls.instances:
            if instance.lock == False:
                return instance
        # check if connections can be created   
        if len(cls.instances) < 3: # Anzahl vielleicht global mit einem ALIAS/DEFINE definieren
            obj = super().__new__(cls)
            return obj
        else: 
            return None
        
    def __init__(self):
        #check if self already exists
        if self in type(self).instances: 
            self.lock = True
            return
        self.lock = True
        type(self).instances.append(self)
        
    def discard(self):
        for (index, instance) in enumerate(type(self).instances):
            if instance == self: 
                type(self).instances[index].lock = False

m1 = Multiton()
m2 = Multiton()
m3 = Multiton()
m4 = Multiton()

print(m1, m2, m3, m4)

m1.discard()
m1 = None 

m4 = Multiton()
print(m1, m2, m3, m4)
