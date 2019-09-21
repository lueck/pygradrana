from xml.sax.handler import ContentHandler

from .modell import *


tei_ns = "http://www.tei-c.org/ns/1.0"


class TeiP5Parser(ContentHandler):
    """SAX-Parser fuer in TEI P5 kodierte Theaterstuecke.

    Dieser Parser beachtet Namensraeume, also bitte mit
    feature_namespaces=True verwenden.

    """

    def __init__(self, tei_ns = tei_ns):
        """Konstruktor fuer einen TEI P5 Parser."""
        self.tei_ns = tei_ns
        # Initialisierung der Zustandsvariablen des Parsers
        self.reset()
        # Konstruktor der Superklasse aufrufen
        super(TeiP5Parser, self).__init__()

    def reset(self):
        """Zuruecksetzen der Zustandsvariablen. """
        self.personen = {}
        self.szenen = [[]]
        self.text_konstruktor = [Stumm]
        self.cs = 0
        self.reset_personenrede()

    def reset_personenrede(self):
        """Setzt Variablen zur Aggregation einer Personenrede zurueck."""
        self.person = None
        self.who = None
        self.text = []
        
    def startElementNS(self, name, qname, attrs):
        """Callback-Handler fuer oeffnende Tags. """
        # name ist ein Tupel (uri, localname)
        
        if name == (self.tei_ns, "div"):
            # Neue Szene (Akt)
            self.szenen.append([])
            
        elif name == (self.tei_ns, "sp"):
            # Neue Personenrede
            self.reset_personenrede()
            try:
                self.who = attrs.getValueByQName("who")
            except KeyError:
                pass
            self.text_konstruktor.append(Rede)

        elif name == (self.tei_ns, "speaker"):
            # Name der Personenrede
            self.text_konstruktor.append(Rollenname)
            
        elif name == (self.tei_ns, "stage"):
            # Neue Buehnenanweisung
            self.text_konstruktor.append(Buehne)
            

    def endElementNS(self, name, qname):
        """Callback-Handler fuer oeffnende Tags. """

        if name == (self.tei_ns, "div"):
            # Szene (Akt) zu Ende
            szene = self.szenen.pop()
            # aber nur, wenn die szene mindestens eine Liste oder
            # mindestens eine Personenrede groß ist.
            if len(szene) > 0:
                self.szenen[-1].append(szene)
            
        elif name == (self.tei_ns, "sp"):
            # Personenrede zu Ende, also Variablen zu Objekt
            # zusammenfuehren
            pr = Personenrede(self.person, self.who, self.text)
            # und in Szene abspeichern
            self.szenen[-1].append(pr)
            # Variablen zuruecksetzen
            self.reset_personenrede()
            # Textkonstruktor Rede aus dem Keller entfernen
            self.text_konstruktor.pop()

        elif name == (self.tei_ns, "speaker"):
            # Rollenname zu Ende: die zuletzt gelesenen beitraege, die
            # vom Typ Rollenname sind, aus beitraege entfernen und in
            # Liste speichern
            person_teile = []
            while self.text and type(self.text[-1]) == Rollenname:
                person_teile.append(self.text.pop())
            # Die Liste mit Bestandteilen des Rollennamens ist jetzt
            # verkehrt herum. Umdrehen und alles zum Rollennamen
            # zusammenfuegen:
            self.person = "".join([str(teil) for teil in reversed(person_teile)])
            # Textkonstruktor fuer Rollenname entfernen
            self.text_konstruktor.pop()

        elif name == (self.tei_ns, "stage"):
            # Buehnenanweisung zu Ende
            self.text_konstruktor.pop()

    def characters(self, content):
        """Callback-Handler fuer character data, also Textknoten."""
        self.text.append(self.text_konstruktor[-1](content))
        self.cs += 1

    def endDocument(self):
        """Callback-Handler, der am Ende des Dokuments aufgerufen wird."""
        # die interne Keller-Struktur der Variablen self.szenen ist
        # fuer Zugriff von außen nicht hilfreich
        self.szenen = list(self.szenen[-1])
