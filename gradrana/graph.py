from gradrana.konfiguration import *

def sum_min_edge_weight(acc, w1, w2):
    return acc + min(w1, w2)


class ConfigurationGraph(Konfigurationsmatrix):

    def __init__(self,
                 sum_edge_weight = sum_min_edge_weight,
                 initial_edge_weight = 0,
                 sum_node_weight = sum,
                 **kwargs):
        super(ConfigurationGraph, self).__init__(**kwargs)
        self.sum_edge_weight = sum_edge_weight
        self.initial_edge_weight = initial_edge_weight
        self.sum_node_weight = sum_node_weight
        self.nodes = {}
        self.edges = {}
        self.degree_dict = {}
        self.degrees = {}
        self.avg_degree = None
    
    def __call__(self, scenes, persons):
        super(ConfigurationGraph, self).__call__(scenes, persons)
        self.generate_graph()
        self.generate_degrees()
        
    def generate_graph(self):
        """Generate the graph. """
        for scene in self.szenennummern:
            # get names of personal present in a szene
            names = [k for k, v in self.konfiguration.items() if scene in v]
            # generate combinations, without permutations
            combinations = [(a, b) for a in names for b in names if a < b]
            for (name1, name2) in combinations:
                # update degree_dict
                if not name1 in self.degree_dict:
                    self.degree_dict[name1] = set()
                self.degree_dict[name1].add(name2)
                if not name2 in self.degree_dict:
                    self.degree_dict[name2] = set()
                self.degree_dict[name2].add(name1)
                # generate edge with weight
                edge = self.edge_name(name1, name2)
                self.edges[edge] = self.sum_edge_weight(
                    self.edges.get(edge, self.initial_edge_weight),
                    self.konfiguration[name1][scene],
                    self.konfiguration[name2][scene])
        # generate node with weight
        for name, d in self.kuerzel.items():
            self.nodes[name] = self.sum_node_weight([v for v in d.values()])

    def edge_name(self, name1, name2):
        return "e|" + name1 + "|" + name2

    def generate_degrees(self):
        i = 0
        total = 0
        for k, v in self.degree_dict.items():
            deg = len(v)
            self.degrees[k] = deg
            total += deg
            i += 1
        self.avg_degree = total / i
