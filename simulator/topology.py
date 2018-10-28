import sys
import networkx as nx

class Topology:

    def __init__(self):
        self.__g = nx.Graph()
        self.node_list = []


    def add_node(self, node):
        # TODO: Introduce Node Here, however, polymorphism is a little difficult
        self.__g.add_node(node)


    def add_link(self, node1, node2, latency):
        # TODO: Introduce Node Here, however, polymorphism is a little difficult
        if latency < 0:
            sys.stderr.write("Latency of a link cannot be negative.")
            sys.exit(-1)
        self.__g.add_edge(node1, node2, latency = latency)

    # TODO: DELETE_NODE = "DELETE_NODE"
    # TODO: DELETE_LINK = "DELETE_LINK"
    # TODO: CHANGE_LINK = "CHANGE_LINK"
    # TODO: PRINT = "PRINT"
    # TODO: DRAW_TOPOLOGY = "DRAW_TOPOLOGY"
    # TODO: DRAW_PATH = "DRAW_PATH"
    # TODO: DUMP_TABLE = "DUMP_TABLE"


    def __str__(self):
        ans = ""
        for node in self.__g.nodes:
            ans += "node " + str(node) + ": "
            ans += str(self.__g[node])
            ans += "\n"
        return ans

