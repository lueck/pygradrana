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

    def __init__(self, name, kuerzel, beitrag):
        self.name = name
        self.kuerzel = kuerzel
        self.beitrag = beitrag

    def __str__(self):
        rc = str(self.name)
        for b in self.beitrag:
            rc += str(b)
        return rc

    def spricht(self):
        rc = "".join([str(b) for b in self.beitrag if type(b)==Rede])
        rc = rc.lstrip(" \n\t.,:;")
        rc = rc.rstrip(" \n\t")
        return rc
    
    def __len__(self):
        return len(self.spricht())
