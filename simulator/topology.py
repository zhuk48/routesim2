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

    def test(self):
        self.__g.add_node(1)
        self.__g.add_node(2, time = "2ms")
        self.__g.add_node(3)
        self.__g.add_node(4)

        self.__g.add_edge(1, 2, weight = 10)
        # error: self.__g[1][2] = {3: 3}
        self.__g.add_edge(1, 3)
        self.__g.add_edge(1, 4)
        self.__g.add_weighted_edges_from([(1,3, 78)])

        print(self.__g.edges)
        print(self.__g.edges())

        print(self.__g.nodes)
        print(self.__g[2])
        print(self.__g.node)
        print(self.__g[1][2])

        self.__g.remove_node(4)
        print(self.__g.nodes)
        print(self.__g[1])

        self.__g.add_edge(1, 4)
        print(self.__g.nodes)
        print(self.__g[1])
        print(self.__g.adj[1])

        #print(self.__g[1][2]['latency'])
        print(self.__g[2][1])

        self.__g[1][3]['latency'] = 3
        print(self.__g[3][1])

        print(self.__g[2]) # get neighbor = {1: {'latency': 10}}
        print(self.__g.nodes[2]) # get node attributes = {'time': '2ms'}


# t = Topology()
# t.test()

"""
g = nx.DiGraph()
>>> G[1]  # same as G.adj[1]
AtlasView({2: {}})
>>> G[1][2]
{}
>>> G.edges[1, 2]
{}

>>> list(G.edges)
[(1, 2), (1, 3), (3, 'm')]
>>> list(G.adj[1])  # or list(G.neighbors(1))
[2, 3]
>>> G.degree[1]  # the number of edges incident to 1
2
G.remove_node(2)
>>> G.remove_edge(1, 3)


for (u, v, wt) in FG.edges.data('weight'):
...     if wt < 0.5: print('(%d, %d, %.3f)' % (u, v, wt))
"""