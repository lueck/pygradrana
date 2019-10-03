from collections import UserString

class Stumm(UserString):
    """Konstruktor fuer nicht weiter spezifizierten stummen Text."""

class Rollenname(UserString):
    """Konstruktor fuer Text, der zum Rollennamen gehoert."""

class Rede(UserString):
    """Konstruktor fuer Text, der zur Personenrede gehoert."""

class Buehne(UserString):
    """Konstruktor fuer Text, der zu einer Buehnenanweisung gehoert."""
    

class Personenrede(object):
    """Klasse fuer Personenrede-Objekte. Eine Personenrede besteht im
    wesentlichen aus einer Liste von Textstuecken, die in einer
    Personenrede vorkommen. Dieses koennen unterschiedlichen Typs sein:
    der Rollenname, die Rede, Buehnenanweisungen."""

    def __init__(self, name, kuerzel, beitrag):
        """Konstruktor fuer Personenrede-Objekte."""
        self.name = name
        self.kuerzel = kuerzel
        self.beitrag = beitrag

    def __str__(self):
        """Gibt String-Repraesentation des gesamten Objects zurueck."""
        rc = str(self.name)
        for b in self.beitrag:
            rc += str(b)
        return rc

    def spricht(self):
        """Gibt Liste der tatsaechlich gesprochenen Textstuecke
        zurueck. Rollenname, Buehnenanweisungen u. dergl. werden also
        herausgefiltert."""
        rc = "".join([str(b) for b in self.beitrag if type(b)==Rede])
        rc = rc.lstrip(" \n\t.,:;")
        rc = rc.rstrip(" \n\t")
        return rc
    
    def __len__(self):
        """Gibt die Laenge des tatsaechlich gesprochenen Textes in Zeichen an."""
        return len(self.spricht())
