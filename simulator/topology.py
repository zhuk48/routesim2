import sys
import networkx as nx

class Topology:

    def __init__(self):
        self.__g = nx.Graph()
        self.node_list = []


    def add_node(self, node):
        # if

        self.__g.add_node(node)


    def add_link(self, node1, node2, latency):
        if latency < 0:
            sys.stderr.write("Latency of a link cannot be negative.")
            sys.exit(-1)
        self.__g.add_edge(node1, node2, latency = latency)


    def __str__(self):
        ans = ""
        for node in self.__g.nodes:
            ans += "node " + str(node) + ": "
            ans += str(self.__g[node])
            ans += "\n"

        return ans

