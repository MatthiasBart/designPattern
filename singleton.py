class Singleton(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)
        return cls.instance
    
class Auto_Singleton(Singleton):
    def __init__(self):
        self.farbe = "Rot"
        self.reifen = "Michelin"

auto1 = Auto_Singleton()
auto2 = Auto_Singleton()

print(auto1.farbe)
print(auto2.farbe)
auto1.farbe = "Schwarz"
print(auto1.farbe)
print(auto2.farbe)