import os.path

from gradrana.modell import Personenrede


def praesenz(acc, rede):
    return 1

def beitragsanzahl(acc, rede):
    return acc + 1

def beitragslaenge(acc, rede):
    return acc + len(rede)

def beitragswoerter(acc, rede):
    return acc + len(rede.spricht().split())


class Konfigurationsmatrix(object):
    """Erstellt eine Konfigurationsmatrix nach Solomon Marcus. """

    def __init__(self,
                 auswertfunktion = praesenz,
                 anfangswert = 0,
                 ignoriere_in_name = " \n\t.,:;"):
        self.auswertfunktion = auswertfunktion
        self.anfangswert = anfangswert
        self.ignoriere_in_name = ignoriere_in_name
        self.konfiguration = {}
        self.szenennummern = []
        self.personen = {}
        self.kuerzel = {}

    def __call__(self, szenen, personen):
        self.erstelle_dramatis_personae(szenen)
        self.erstelle_konfiguration(szenen, personen)
 
    def erstelle_konfiguration(self, szenen, personen, praefix = ""):
        i = 1
        szenennummer_hinzugefuegt = False
        for szene in szenen:
            if type(szene) == list:
                ## Rekursion
                self.erstelle_konfiguration(szene, personen, praefix + str(i) + ".")
            elif type(szene) == Personenrede:
                if not szenennummer_hinzugefuegt:
                    self.szenennummern.append(praefix)
                    szenennummer_hinzugefuegt = True
                namen = self.bestimme_namen(szene.name, szene.kuerzel, personen)
                for name in namen:
                    if name not in self.konfiguration:
                        self.konfiguration[name] = {}
                    bisher = self.konfiguration[name].get(praefix, self.anfangswert)
                    self.konfiguration[name][praefix] = self.auswertfunktion(bisher, szene)
            else:
                raise Exception("unerwarteter Datentyp")
            i += 1

    def erstelle_dramatis_personae(self, szenen):
        for szene in szenen:
            if type(szene) == list:
                self.erstelle_dramatis_personae(szene)
            elif type(szene) == Personenrede:
                ## Mit Namensschluessel in self.person ablegen
                
                #name = szene.name
                #kuerzel = szene.kuerzel
                if type(szene.name) == list:
                    for name in szene.name:
                        name = name.strip(self.ignoriere_in_name)
                        if not name in self.personen:
                            for kuerzel in szene.kuerzel:
                                self.personen[name] = {kuerzel : self.auswertfunktion(
                                    self.anfangswert,
                                    szene)}
                        else:
                            for kuerzel in szene.kuerzel:
                                self.personen[name][kuerzel] = self.auswertfunktion(
                                    self.personen[name].get(kuerzel, self.anfangswert),
                                    szene)
                else:
                    name = szene.name.strip(self.ignoriere_in_name)
                    kuerzel = szene.kuerzel
                    if not name in self.personen:
                        self.personen[name] = {kuerzel : self.auswertfunktion(
                            self.anfangswert,
                            szene)}
                    else:
                        self.personen[name][kuerzel] = self.auswertfunktion(
                            self.personen[name].get(kuerzel, self.anfangswert),
                            szene)
                ## Mit Kuerzelschluessel in self.kuerzel ablegen
                if type(szene.kuerzel) == list:
                    for kuerzel in szene.kuerzel:
                        if not kuerzel in self.kuerzel:
                            for name in szene.name:
                                name = name.strip(self.ignoriere_in_name)
                                self.kuerzel[kuerzel] = {name : self.auswertfunktion(
                                    self.anfangswert,
                                    szene)}
                        else:
                            for name in szene.name:
                                name = name.strip(self.ignoriere_in_name)
                                self.kuerzel[kuerzel][name] = self.auswertfunktion(
                                    self.kuerzel[kuerzel].get(name, self.anfangswert),
                                    szene)
                else:
                    name = szene.name.strip(self.ignoriere_in_name)
                    kuerzel = szene.kuerzel
                    if not kuerzel in self.kuerzel:
                        self.kuerzel[kuerzel] = {name : self.auswertfunktion(
                            self.anfangswert,
                            szene)}
                    else:
                        self.kuerzel[kuerzel][name] = self.auswertfunktion(
                            self.kuerzel[kuerzel].get(kuerzel, 0),
                            szene)


    def bestimme_namen(self, namen, kuerzel, personen):
        if kuerzel:
            return kuerzel
        elif namen:
            if type(namen) == list:
                for name in namen:
                    name.strip(self.ignoriere_in_name)
                    # FIXME: Ist personen wirklich Name->Kuerzel ?
                    if name in personen:
                        return personen[name]
                    if name in self.personen:
                        ks = self.personen[name]
                        return max(ks, key = ks.get)
                    else:
                        return name
            else:
                name = namen.strip(self.ignoriere_in_name)
                # FIXME: Ist personen wirklich Name->Kuerzel ?
                if name in personen:
                    return personen[name]
                if name in self.personen:
                    ks = self.personen[name]
                    return max(ks, key = ks.get)
                else:
                    return name
        else:
            raise Exception("Anonyme Rede: " + praefix_neu)



html_template = os.path.join(os.path.dirname(__file__),
                             "konfiguration.html")


class HtmlKonfigurationsmatrix(Konfigurationsmatrix):
    """Formatiert die Konfigurationsmatrix als HTML-Dokument."""

    def __init__(self,
                 template = html_template,
                 summen = False,
                 summen_titel = "TOTAL",
                 **kwargs):
        self.template = template
        self.summen = summen
        self.summen_titel = summen_titel
        super(HtmlKonfigurationsmatrix, self).__init__(**kwargs)

    def __call__(self, szenen, personen):
        super(HtmlKonfigurationsmatrix, self).__call__(szenen, personen)
        print(self.formatiere_matrix())
            
    pre_kopf = "<thead><tr>"
    post_kopf = "</tr></thead>\n"
    pre_kopf_person = "<th>"
    post_kopf_person = "</th>"
    pre_kopf_szene = "<th>"
    post_kopf_szene = "</th>"
    pre_body = "<tbody>\n"
    post_body = "</tbody>"
    pre_zeile = "<tr>"
    post_zeile = "</tr>\n"
    pre_person = "<td>"
    post_person = "</td>"
    pre_szene = "<td>"
    post_szene = "</td>"
    pre_summe = "<td>"
    post_summe = "</td>"
    pre_zeile_summe = "<tfoot><tr>"
    post_zeile_summe = "</tr></tfoot>"
            
    def erstelle_matrix(self):
        rc = ""
        rc += self.pre_kopf
        rc += self.pre_kopf_person
        rc += " "
        rc + self.post_kopf_person
        for szene in self.szenennummern:
            rc += self.pre_kopf_szene
            rc += szene
            rc += self.post_kopf_szene
        if self.summen:
            rc += self.pre_summe
            rc += self.summen_titel
            rc += self.post_summe
        rc += self.post_kopf
        rc += self.pre_body
        for person in sorted(self.kuerzel):
            rc += self.pre_zeile
            rc += self.pre_person
            rc += self.person_str(person)
            rc += self.post_person
            total = 0
            for szene in self.szenennummern:
                rc += self.pre_szene
                v = self.konfiguration[person].get(szene, self.anfangswert)
                total += v
                rc += str(v)
                rc += self.post_szene
            if self.summen:
                rc += self.pre_summe
                rc += str(total)
                rc += self.post_summe
            rc += self.post_zeile
        rc += self.post_body
        if self.summen:
            rc += self.pre_zeile_summe
            rc += self.pre_person
            rc += self.summen_titel
            rc += self.post_person
            total = 0
            for szene in self.szenennummern:
                rc += self.pre_szene
                v = sum([v.get(szene, self.anfangswert) for v in self.konfiguration.values()])
                total += v
                rc += str(v)
                rc += self.post_szene
            rc += self.pre_summe
            rc += str(total)
            rc += self.post_summe
            rc += self.post_zeile_summe
        return rc

    def person_str(self, s):
        return str(s).strip('#')
    
    def formatiere_matrix(self):
        with open(self.template, "r") as f:
            t = f.read()
            return t.format(self.erstelle_matrix())
            
    

latex_template = os.path.join(os.path.dirname(__file__),
                              "konfiguration.tex")


class LatexKonfigurationsmatrix(HtmlKonfigurationsmatrix):
    """Formatiert die Konfigurationsmatrix als TeX-Dokument."""

    pre_kopf = ""
    post_kopf = "\\\\\\hline\n"
    pre_kopf_person = ""
    post_kopf_person = ""
    pre_kopf_szene = "&"
    post_kopf_szene = ""
    pre_body = ""
    post_body = ""
    pre_zeile = ""
    post_zeile = "\\\\\n"
    pre_person = ""
    post_person = ""
    pre_szene = "&"
    post_szene = ""
    pre_summe = "&"
    post_summe = ""
    pre_zeile_summe = "\\hline\n"
    post_zeile_summe = "\\\\\n"
            
    def __init__(self, template = latex_template, **kwargs):
        super(LatexKonfigurationsmatrix, self).__init__(**kwargs)
        self.template = template

    def formatiere_matrix(self):
        with open(self.template, "r") as f:
            t = f.read()
            return t.format(self.erstelle_tabellen_format(),
                            self.erstelle_matrix())

    def erstelle_tabellen_format(self):
        rc = "{|l|"
        i = 0
        l = len(self.szenennummern)
        while i < l:
            rc += "r|"
            i += 1
        if self.summen:
            rc += "|r|"
        rc += "}"
        return rc

    def person_str(self, s):
        return str(s).strip('#').replace("_", "\\_")
