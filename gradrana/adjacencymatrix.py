import os.path

from gradrana.graph import ConfigurationGraph


html_template = os.path.join(os.path.dirname(__file__),
                             "table.html")


class HtmlAdjacencyMatrix(ConfigurationGraph):

    pre_head = "<thead><tr>"
    post_head = "</tr></thead>\n"
    pre_head_first = "<th>"
    post_head_first = "</th>"
    pre_head_person = "<th>"
    post_head_person = "</th>"
    pre_head_degree = "<th>"
    post_head_degree = "</th>"
    pre_body = "<tbody>\n"
    post_body = "</tbody>"
    pre_row = "<tr>"
    post_row = "</tr>\n"
    pre_person = "<td>"
    post_person = "</td>"
    pre_weight = "<td>"
    post_weight = "</td>"
    pre_degree = "<td>"
    post_degree = "</td>"

    def __init__(self,
                 template = html_template,
                 degree_label = "DEGREE",
                 avg_degree_label = "AVG DEGREE=",
                 missing_value = " ",
                 outfile = None,
                 weighted_nodes = True, # only for viz
                 weighted_edges = True, # only for viz
                 **kwargs):
        super(HtmlAdjacencyMatrix, self).__init__(**kwargs)
        self.template = template
        self.degree_label = degree_label
        self.avg_degree_label = avg_degree_label
        self.missing_value = missing_value
        self.outfile = outfile

    def __call__(self, scenes, persons):
        super(HtmlAdjacencyMatrix, self).__call__(scenes, persons)
        if self.outfile:
            print(self.format_matrix(), file=open(self.outfile, "w"))
        else:
            print(self.format_matrix())

    def format_matrix(self):
        with open(self.template, "r") as f:
            t = f.read()
            return t.format(self.generate_matrix())
        
    def generate_matrix(self):
        names_in_order = list(reversed(sorted(self.degrees, key=self.degrees.get)))
        rc = self.pre_head
        rc += self.pre_head_first
        rc += self.avg_degree_label
        rc += str(round(self.avg_degree, 2))
        rc += self.post_head_first
        rc += self.pre_head_degree
        rc += self.degree_label
        rc += self.post_head_degree
        for name in names_in_order:
            rc += self.pre_head_person
            rc += self.format_name(name)
            rc += self.post_head_person
        rc += self.post_head
        rc += self.pre_body
        for name1 in names_in_order:
            rc += self.pre_row
            rc += self.pre_person
            rc += self.format_name(name1)
            rc += self.post_person
            rc += self.pre_degree
            rc += str(self.degrees[name1])
            rc += self.post_degree
            for name2 in names_in_order:
                n1, n2 = sorted([name1, name2])
                rc += self.pre_weight
                rc += str(self.edges.get(self.edge_name(n1, n2), self.missing_value))
                rc += self.post_weight
            rc += self.post_row
        rc += self.post_body
        return rc

    def format_name(self, s):
        return str(s).strip('#')


latex_template = os.path.join(os.path.dirname(__file__),
                              "table.tex")


class LatexAdjacencyMatrix(HtmlAdjacencyMatrix):
    
    pre_head = ""
    post_head = "\\\\\\hline\n"
    pre_head_first = "\multicolumn{1}{|c|}{"
    post_head_first = "}"
    pre_head_person = "&\\rot{"
    post_head_person = "}"
    pre_head_degree = "&\\rot{"
    post_head_degree = "}"
    pre_body = ""
    post_body = ""
    pre_row = ""
    post_row = "\\\\\\hline\n"
    pre_person = ""
    post_person = ""
    pre_weight = "&"
    post_weight = ""
    pre_degree = "&"
    post_degree = ""

    def __init__(self,
                 template = latex_template,
                 avg_degree_label = "$\\overline{deg}=$",
                 **kwargs):
        super(LatexAdjacencyMatrix, self).__init__(**kwargs)
        self.template = template
        self.avg_degree_label = avg_degree_label
    
    def format_matrix(self):
        with open(self.template, "r") as f:
            t = f.read()
            return t.format(self.generate_table_format(),
                            self.generate_matrix())

    def generate_table_format(self):
        rc = "{|l|r||"
        i = 0
        l = len(self.degrees)
        while i < l:
            rc += "r|"
            i += 1
        rc += "}"
        return rc

    def format_name(self, s):
        return str(s).strip('#').replace("_", "\\_")
