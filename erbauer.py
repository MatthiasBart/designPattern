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