import networkx as nx
import matplotlib.pyplot as plt

from gradrana.graph import ConfigurationGraph


class DramaVisualization(ConfigurationGraph):

    def __init__(self,
                 outfile = None,
                 missing_value = " ",
                 weighted_nodes = True,
                 weighted_edges = True,
                 **kwargs):
        super(DramaVisualization, self).__init__(**kwargs)
        self.outfile = outfile
        self.missing_value = missing_value
        self.weighted_nodes = weighted_nodes
        self.weighted_edges = weighted_edges

    def __call__(self, scenes, persons):
        super(DramaVisualization, self).__call__(scenes, persons)
        self.visualize()

    def visualize(self):
        G = nx.Graph()
        for k, v in self.nodes.items():
            if self.weighted_nodes:
                w = v
            else:
                w = 1
            name = list(self.kuerzel[k].values())[0]
            G.add_node(k, weight=w, label=k)
        for k, v in self.edges.items():
            if self.weighted_edges:
                w = v
            else:
                w = 1
            pre, n1, n2 = k.split("|")
            G.add_edge(n1, n2, weight=w)
        edge_weights = [G[u][v]["weight"] for u, v in G.edges()]
        if self.weighted_edges:
            max_weight = max(edge_weights)
            edge_weights = [ 10 * w / max_weight for w in edge_weights]
        # plot
        nx.draw(G, with_labels=True, font_weight="normal", width=edge_weights)
        if self.outfile:
            plt.savefig(self.outfile)
        else:
            plt.show()
