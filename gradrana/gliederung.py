class Gliederung(object):
    """Analyse-Klasse fuer Gliederung. """

    def __init__(self, treppe=False, erste_rede=False):
        """Konstruktor fuer Gliederung-Analyse. 

        Parameter: 

        treppe: Falls True, dann wird eine Ausgabe mit Einrueckungen
        erzeugt.

        erste_rede: Falls True, dann wird die erste Personenrede einer
        Szene ausgegeben. Das kann zu Pruefzwecken sinnvoll sein.

        """
        self.treppe = treppe
        self.erste_rede = erste_rede

    def __call__(self, szenen, personen):
        """Erzeugt eine einfache Übersicht über die Gliederung in Akte, Szenen
        usw. Als Parameter szenen wird eine Liste von potentiell
        verschachtelten Listen erwartet.
        """
        self.__gliederung(szenen)

    def __gliederung(self, szenen, nummer = 1, praefix = "", einzug = ""):
        """Gibt die Gliederung eines Stückes aus."""
        if szenen:
            szene = szenen.pop()
            if self.treppe:
                print(einzug + str(nummer))
            if type(szene) == list and len(szene) > 0 and type(szene[0]) == list:
                ## Rekursion
                self.__gliederung(szene, 1, praefix + str(nummer) + ".", einzug + "\t")
            elif type(szene) == list:
                if self.treppe:
                    print("\t" + einzug + str(len(szene)) + " Reden")
                else:
                    print(praefix + str(nummer) + "\tReden: " + str(len(szene)))
                if self.erste_rede and len(szene) > 0:
                    print(einzug + "\t" + str(szene[0]) + "\n")
            else:
                print("Unbekannt")
            ## weitere ausgeben
            self.__gliederung(szenen, nummer + 1, praefix, einzug)
