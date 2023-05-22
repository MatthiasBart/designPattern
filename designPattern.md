# 4 Design Pattern in Python 
Im Rahmen des 2.Semesters der Leherveranstaltung Software Developement, wurde als Kompensation die Auflistung und Betrachtung von 4 Design Pattern gewählt, die so auch in Python umzusetzen sind. 

Die folgende Auflistung besteht aus den folgenden kurz angeführten Design Patterns:
1. Factory Method/Fabrikmethode
2. Singleton
3. Multiton
4. Erbauer

## Fabrikmethode 
### Überblick 
Das Design Pattern "Factroy Method" bzw "Fabrikmethode" zählt zu den Erzeugungsmustern und ist demnach für die Erstellung neuer Objekte zuständig. 
Dieses Muster wird meist mit als "Factory Class" bzw Erzeugerklasse umgesetzt. 
Deswegen kommen dabei 2 Veerbungshierarchien zu Stande, eine der Fabriken/Erzeuger und eimal der Produkte. Dabei wird zu allererst vom Erzeuger und vom Produkt eine abstrakte Basisklasse erstellt, gegen deren Interfaces in der Anwendung programmiert wird. Deswegen ist es wichtig, dass sich die einzelnen Produkte sehr ähnlich sind. Da dieses Entwurfsmuster sehr viel Denk- und Schreibarbeit erfordert richtig umgestetzt zu werden sind viele Abwandlungen davon verbreitet und wahrscheinlich sogar sinnvoller als die origanlen Gedanken dazu. 

Dieses Muster führt zu den folgenden Vorteilen:
- Die konkreten Objekte sind bequem erweiterbar 
- Die konkreten Objekte sind zur Entwicklungszeit nicht bekannt und dennoch kann gegen die Basisklasse programmiert werden 

Bilderbuch Beispiel: 
-
Eine abstrakte Mahlzeit(Produkt), ein abstrakter Kellner(Erzeuger).
Die Mahlzeit hat Eigenschaften wie Kalorien, Name, ...
Der Kellner hat die Eigenschaft mahlzeit und die Methoden Aufnehmen(), Liefern() und Zubereiten(), wobei dabei die Methode Zubereiten() die abstrakte Factorymethode ist. Von der abstrakten Klasse Mahlzeit erben wir nun die Klassen Pizza und Bratwurst ab. Von der abstrakten Klasse Kellner leiten wir die Klassen PizzeriaKellner und BratwurstKellner ab, welche deren eigene Zubereiten() implementieren. Jetzt können Instanzen der konkreten Kellner erstellt werden und gegen das Interface der abstrakten Klasse Kellner implementiert werden. Egal ob ein PizzeriaKellner oder ein BratwurstKellner erstellt wird man kann deren Methoden Aufnehmen(), Zubereiten() und Liefern() aufrufen, ohne dabei konkreteres über deren Implementierung wissen zu müssen.

**Da das obige Beispiel nicht ganz realitätsnah ist und dies auch nach längerer Recherche doch das naheliegendste war und zumal die Implementierung wie schon oben angedeutet oft Abgewandelt aussieht möchte ich unten noch ein anderes Beispiel anführen, welches auch anschließend in der Implementierung zu finden sein wird.**

Praxisnäheres Beispiel:
-
Wir schreiben ein Framework zu Erstellung von SQL-Datenbank Connections. Die einzelnen ConnectionKlassen und deren spezifische Implementierung (OracleDb, MircosoftDb) soll dem Nutzer nicht zur verfügung stehen, sondern gegen ein Interface/abstrakte Basisklasse `Database` programmiert werden. Dazu wird eine Klasse `ConnectionCreator` erstellt, welches die Methode `build_connection` implementiert. Je nach übergabe Parameter wird dann die benötigte konkrete `Database` Klasse returned, die sich nur durch deren Überschreibungen der in der Basisklasse definierten abstrakten Methoden unterscheidet. Demnach wird vom Benutzer ständig nur gegen das Interface der abstrakten Basisklasse programmiert.

### Implementierung 
```
# Factory-Class-Beispiel

# Connection-Klassen:
from abc import abstractmethod

class Database():
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
```

führt zu folgendem Output

```
connect to Oracle
disconnect from Oracle
connect to Microsoft
disconnect from Microsoft
```
### Hürden/Abgrenzungen 
Bei diesem Entwurfsmuster ist es schwer das ursprüngliche Konzept in der Praxis anzuwenden, wodurch sehr viele Abwandlungen existieren die sich häufig besser integriert haben. Dennoch ist es vorteilhaft sich an diesem Konzept ab und an zu bedienen, da es das Verständnis oft vereinfacht oder zu kompakteren Interfaces führt. 

## Singleton 
### Überblick 
Zweck dieses Musters ist es sicherzustellen, dass in einer Anwendung immer nur ein Object dieser Klasse initialisiert wird. Dazu wird in Java ähnlichen Programmiersprachen einfach der Initializer bzw. Konstruktor mit dem Keyword private versehen, wodurch die Klasse nur innerhalb der Klasse initialisiert werden kann. Um dennoch die Funktionen der Klasse nutzen zu können, wird eine statische Eigenschaft der Klasse mit dem einem Object des eigenen Typs initialisiert. Danach kann über die statische Eigenschaft auf alle public Methoden und Eigenschaften der Klasse zugegriffen werden, allerdings keine zusätzliche Instanz erzeugt werden.
### Implementierung 
Die Implementierung in Python weist einige Hürden auf, zumal es keine Schlüsselwörter wie private gibt, die einen Konstruktor von außen unzugänglich machen könnten. Weiters kann man den Konstruktor auch nicht mit der in Python eigenen private Nomenklatur, dem "__" vesehen, da dieser sowieso private ist und vom Interpreter selbst nach der Erzeugung eines Objects aufgerufen wird. 

Um das Singelton Muster umzusetzen kommt die statische `__new__` Methode ins Spiel welche bei jeder Object Erstellung einer Class aufgerufen wird. Sie weist die folgende Signatur auf:

`object.__new__(class, *args, **kwargs)`

Die Übergabeparameter sind an die des Initialisers/Konstruktors anzupassen. 

> Initilaisieren wir ein Beispielobjekt wie folgt,  `Person('John')` so werden eigentlich folgende Methoden aufgerufen: 

```
person = object.__new__(Person, 'John')
person.__init__('John')
```
Also wird in der `__new__` Methode einfach eine statische Eigenschaft angelegt, die bei jeder neuen Initalisierung der Klasse das Singelton zuruückgibt.
```
class Singleton(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)
        return cls.instance
```
Vorteilhaft ist es die Singleton Klasse einmal zu definieren und anschließend diese Funktionalität an Implementierungen des Singleton Musters in Klassen abzuerben.
```
class Auto_Singleton(Singleton):
    def __init__(self, *args):
        # Dies wird nur einmal, bei der Erstellung des Singletons ausgeführt
```
und der code
```
auto1 = Auto_Singleton()
auto2 = Auto_Singleton()

print(auto1.farbe)
print(auto2.farbe)
auto1.farbe = "Schwarz"
print(auto1.farbe)
print(auto2.farbe)
```
führt zu folgendem Output
```
Rot
Rot
Schwarz
Schwarz
```
### Hürden/Abgrenzungen 
Implemntieren wir dieses Verhalten zum Beispiel bei einer Klasse `class Auto():` und initialisieren wir diese an verschiedenen Stellen, ist dem Nutzer unserer Klasse nicht direkt klar, dass es sich dabei um ein Singleton Objekt handelt. Es ist wichtig dies durch die Namensgebung deutlich zu machen. 

## Multiton
### Überblick 
Das Multiton ist eine Abwandlung des Singletons, was aus dem Namen schon klar wird. Wieder ist es Ziel die Anzahl der erzeugten Instanzen zu kontrollieren und deren Anzahl zu begrenzen. Die Begrenzung auf genau eine Instanz, wie beim Singleton ist oft nicht ausreichend.

### Implementierung
Man stelle sich eine Application vor, die auf eine Datenbank zugreifen möchte. Eine einzige Verbindung, wäre zu wenig und für jeden Zugriff eine neue Verbindung zu erstellen wäre aufgrund des Zeitaufwandes für die Connection sehr inperformant. Deswegen stellen wir mit unserem Multiton-Objekt einen Pool von zB 3 Datenbank-Verbindungen zur Verfügung. Dazu wird ein Array unserer Instanzen gehalten, welche die maximale Anzahl nicht überschreiten darf. 

In der unteren Darstellung wurde das Design Pattern des Multitons aufs 2 verschiedene Weisen implementiert. Einmal mit einer Factory Class die den Überblick über unsere Connections hät und das Locking managed. Diese Implemntierung ist voll funktionsfähig und funktioniert wie gewollt. 

```
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
# False True True None

db4 = dbPool.get_connection("path", "user", "key")

# weil db1 nicht auf None gesetzt wurde halten db1 und db4 jetzt die gleichen Refernzen

print(db1, db2, db3, db4)

# <__main__.DatabaseConnection object at 0x100d5ef70>
# <__main__.DatabaseConnection object at 0x100d5ed30> 
# <__main__.DatabaseConnection object at 0x100d5eca0>
# <__main__.DatabaseConnection object at 0x100d5ef70>
```

Die zweite Implementierung ist leider etwas hacky und nicht ganz verständlich, und zusätzlich nicht vollständig getestet also ohne Gewährleistung ob diese Methode die Refernzen auch richtig beibehält. Außerdem ist sie nicht so elegant und verständlich und was nicht elegant und einfach funktioniert ist meistens auch nicht gut zu warten und hat in Programmen nichts verloren. Dennoch stellt es eine Möglichkeit dar mit der `__new__` Methode, wie auch schon beim Singleton, die Anzahl der Instanzen zu kontrollieren.

```
########################################################
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

```

printet folgende Ausgabe: 

```
True True True None

True <__main__.DatabaseConn object at 0x1049c2eb0> True <__main__.DatabaseConn object at 0x1049c2eb0>
```

Hier noch mal in abstrahierter Form:
```
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
```
führt zu Output, wo man sehen kann dass m1 zuerst die selbe Signatur hat wie m4 danach: 
```
<__main__.Multiton object at 0x100e9ed90> <__main__.Multiton object at 0x100e9ed30> <__main__.Multiton object at 0x100e9ecd0> None

None <__main__.Multiton object at 0x100e9ed30> <__main__.Multiton object at 0x100e9ecd0> <__main__.Multiton object at 0x100e9ed90>
```
### Hürden/Abgrenzungen 
Es ist wieder schwer dies über eine statische Methode zu implementieren, da das verhalten eines privaten Konstruktors nicht einfach umzusetzen ist. 

## Erbauer
### Überblick 
Die Erbauer Klasse ist sinnvoll zu implementieren, sollten wir viele Überladungen des Konstruktors einer bestimmten Klasse haben. Ziel dieses Musters ist es Daten nach und nach hinzuzufügen und aus diesen anschließend ein Produkt zu bauen. Dazu werden folgende Akteure verwendet:

- Direktor: ist für die Konstruktion des Produkts zuständig und hält die Daten
- Erbauer: ist für die Umsetzung der Konstruktion verantwortlich und wird als abstrakte Basisklasse implementiert welche eine abstrakte Methode "erbaue" in dem Fall `render` aufweist
- Konkreter Erbauer: ist für die konkrete Umsetzung der Konstruktion verantwortlich und implementiert die `render` Methode
- Produkt: ist das gewünschte Ergebnis des Bauvorgangs 

### Implementierung 
Bei der Implementierung orientiere ich mich stark an einem Beispiel, welches als Direktor den `LayoutManager`, als Erbauer den `WidgetManager`, als konkrete Erbauer die Klassen `BorderLayoutWidgetManager`,  `BoxLayoutWidgetManager`  und `FlowLayoutWidgetManager` und als Produkt, das Ergebnis die Klasse `HTMLPage`.

Das Ziel ist es (man kann den LayoutManager auch als Singleton implementieren) einen LayoutManager zu haben, der sich um die Konstruktion der HTMLPage kümmert. Dazu hält er das Material, Daten oder in diesem Fall Wigets die er auszulegen hat. Ich als Client der Anwendung möchte ihm mitteilen, wie er diese Widgets auszulegen hat und sage ihm, welchen `WidgetManager` er zu nutzen hat. Dieser weiß genau wie er den HTMLCode zu gernerieren hat um die Widgets gewünscht auszulegen, damit der allgemeine LayoutManager diese als Paket/Baustein weiterverarbteien kann, in diesem Fall zeigt er nur diese Widgets an. Damit hält der Direktor die Daten, konstruiert mit dem konkreten Erbauer das Produkt und ist gleichzeitig auch der Abnehmer des Produktes. Implementiert sieht es circa wie folgt aus:
```
# Direktor 
class LayoutManager():
    def __init__(self, widgets) -> None:
        self.htmlPage = HTMLPage()
        self.widgets = widgets

    def doLayout(self, widgetManager):
        widgetManager.addWidgets(self.widgets)
        widgetManager.render()
        self.htmlPage = widgetManager.getHtmlPage()

    def addWidget(self, widget):
        self.widgets.append(widget)
    
    def addWidgets(self, widgets):
        self.widgets.append(widgets)

    def printHtmlCode(self):
        print(self.htmlPage)

# Abstrakter Erbauer 
from abc import ABC, abstractmethod

class WidgetManager(ABC):
    def __init__(self):
        self.htmlPage = HTMLPage()
        self.widgets = []

    @abstractmethod
    def getHtmlPage(self):
        pass
    
    @abstractmethod
    def addWidget(self, widget):
        pass
    
    @abstractmethod
    def addWidgets(self, widgets):
        pass

    @abstractmethod
    def render(self):
        pass

    
# Konkrete Erbauer

class BorderLayoutWidgetManager(WidgetManager):
    def __init__(self):
        self.htmlPage = HTMLPage()
        self.widgets = []
        
    def getHtmlPage(self):
        return self.htmlPage
    
    def addWidget(self, widget):
        self.widgets.append(widget)
    
    def addWidgets(self, widgets):
        self.widgets.append(widgets)

    def render(self):
        self.getHtmlPage().htmlCode = self.renderHtmlFromWidgets()

    def renderHtmlFromWidgets(self):
        # render HtmlCode from widgets and return
        return "<h1> Hello Widgtes im Border Layout <\h1>"
    
class BoxLayoutWidgetManager(WidgetManager):
    def __init__(self):
        self.htmlPage = HTMLPage()
        self.widgets = []
        
    def getHtmlPage(self):
        return self.htmlPage
    
    def addWidget(self, widget):
        self.widgets.append(widget)
    
    def addWidgets(self, widgets):
        self.widgets.append(widgets)

    def render(self):
        self.getHtmlPage().htmlCode = self.renderHtmlFromWidgets()

    def renderHtmlFromWidgets(self):
        # render HtmlCode from widgets and return
        return "<h1> Hello Widgtes im Box Layout <\h1>"

class FlowLayoutWidgetManager(WidgetManager):
    pass

# Produkt 

class HTMLPage():
    def __init__(self) -> None:
        self.htmlCode = ""

# LayoutManager könnte auch als Singleton implementiert sein, da es davon in meiner Anwendung nur einen gibt 
# default sind 2 widgets im layout Manager 

layoutManager = LayoutManager(["widget1", "widget2"])
layoutManager.doLayout(BorderLayoutWidgetManager())

# die ersten 2 sollen im BorderLayout Modus implementiert werden
htmlPage = layoutManager.htmlPage
print(htmlPage.htmlCode)
# jetzt sollen 2 weitere hinzugefügt werden und das BoxLayout verwendet werden 
layoutManager.addWidgets(["widget3", "widget4"])
layoutManager.doLayout(BoxLayoutWidgetManager())

htmlPage = layoutManager.htmlPage
print(htmlPage.htmlCode)
```
und der Output sieht wie folgt aus:
```
<h1> Hello Widgtes im Border Layout <\h1>
<h1> Hello Widgtes im Box Layout <\h1>
```
### Überlegungen
Dieses Muster ist wie eingangs schon erwähnt sehr von Nutzen wenn viele Überladungen des Konstruktors existieren. Hier in diesem Fall wäre das der WidgetManager (besser wahrscheinlich WidgetLayoutManager genannt) welcher seine überladenen Konstruktoren in verschieden Unterklassen aufgeteilt, und so auch die verschiedene Funktionalität zur Erstellung der verschiedenen Layouts. 

