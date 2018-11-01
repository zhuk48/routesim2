import networkx as nx
import matplotlib.pyplot as plt
# import numpy as np

Matrix = [
        [0, 1, 1, 1, 1, 1, 0, 0],  # a
        [0, 0, 1, 0, 1, 0, 0, 0],  # b
        [0, 0, 0, 1, 0, 0, 0, 0],  # c
        [0, 0, 0, 0, 1, 0, 0, 0],  # d
        [0, 0, 0, 0, 0, 1, 0, 0],  # e
        [0, 0, 1, 0, 0, 0, 1, 1],  # f
        [0, 0, 0, 0, 0, 1, 0, 1],  # g
        [0, 0, 0, 0, 0, 1, 1, 0]  # h
        ]

G = nx.Graph()


for i in range(len(Matrix)):
    for j in range(len(Matrix)):
        if Matrix[i][j] == 1:
            G.add_edge(i, j)

node_labels = {node: name for (node, name) in zip(G.nodes(), ["a", "b", "c", "d", "e", "f", "g", "h"])}
node_color = [1, 2, 3, 1, 2, 3, 1, 2]

edge_color = []
edge_labels = {}
for index, edge in enumerate(G.edges()):
    if index % 2 == 0:
        edge_color.append('k')
        edge_labels[edge] = "label"
    else:
        edge_color.append('r')

# position = nx.circular_layout(G)
position = nx.spring_layout(G)

nx.draw_networkx_nodes(G, position, node_size=500, node_color=node_color)  #with_labels=True
nx.draw_networkx_labels(G, position, labels=node_labels)

nx.draw_networkx_edges(G, position, edge_color=edge_color)
nx.draw_networkx_edge_labels(G, position, edge_labels=edge_labels)

plt.axis('off')
plt.show()
plt.savefig('routing.png')

class Test_Graph:
    def __init__(self):
        self.__g = nx.Graph()

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


child_method = getattr(self, 'out')
"""

