from gradrana.modell import Personenrede

def praesenz(acc, rede):
    return 1

def beitrags_anzahl(acc, rede):
    return acc + 1

def beitrags_laenge(acc, rede):
    # FIXME: misst laenge der liste von Userstrings
    return acc + len(rede)


class Konfigurationsmatrix(object):
    """Erstellt eine Konfigurationsmatrix nach Solomon Marcus. """

    def __init__(self, auswert_funktion = praesenz):
        self.konfig = {}
        self.auswert_funktion = auswert_funktion

    def __call__(self, szenen, personen):
        self.__konfiguration(szenen, personen)
        print(self.konfig)

    def __konfiguration(self, szenen, personen, nummer = 1, praefix = ""):
        if szenen:
            szene = szenen.pop()
            praefix_neu = praefix + str(nummer) + "."
            if type(szene) == list:
                ## Rekursion
                konfig = self.__konfiguration(szene, personen, 1, praefix_neu)
            elif type(szene) == Personenrede:
                if szene.kuerzel:
                    name = szene.kuerzel
                elif szene.name:
                    name = szene.name
                else:
                    raise Exception("Anonyme Rede: " + praefix_neu)
                if name not in self.konfig:
                    self.konfig[name] = {}
                bisher = self.konfig.get(name, {}).get(praefix, 0)
                self.konfig[name][praefix] = self.auswert_funktion(bisher, szene.beitrag)
            else:
                raise Exception("unerwarteter Datentyp")
            self.__konfiguration(szenen, personen, nummer + 1, praefix)
