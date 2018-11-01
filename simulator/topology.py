import sys
import logging
import traceback
import time
import networkx as nx
import matplotlib.pyplot as plt

from simulator.config import *
from simulator.event import Event
from simulator.event_queue import Event_Queue


class Topology:

    Nodes = {}
    this = None

    def __init__(self, algorithm, step='NORMAL'):
        self.__g = nx.Graph()
        self.node_cls = ROUTE_ALGORITHM_NODE[algorithm]
        self.step = step
        self.logging = logging.getLogger('Sim')
        self.position = None
        Topology.Nodes = {}
        Topology.this = self

    def __str__(self):
        ans = ""
        for node in self.__g.nodes:
            ans += "node " + str(node) + ": "
            ans += str(self.__g[node])
            ans += "\n"
        return ans

    def send_current_links(self):
        for node1, node2 in self.__g.edges:
            self.change_link(node1, node2, self.__g[node1][node2]['latency'])

    def add_node(self, node):
        if node not in Topology.Nodes.keys():
            self.position = None
            Topology.Nodes[node] = self.node_cls(node)
        self.__g.add_node(node)

    def add_link(self, node1, node2, latency):
        if latency < 0:
            sys.stderr.write("Latency of a link cannot be negative.")
            sys.exit(-1)
        self.add_node(node1)
        self.add_node(node2)
        self.__g.add_edge(node1, node2, latency = latency)

    def change_link(self, node1, node2, latency):
        if latency != -1:
            self.add_link(node1, node2, latency)
        self.send_link(Topology.Nodes[node1], node2, latency)
        self.send_link(Topology.Nodes[node2], node1, latency)

    def send_link(self, node, neighbor, latency):
        node.link_has_been_updated(neighbor, latency)

    def delete_link(self, node1, node2):
        if (node1, node2) in self.__g.edges:
            self.__g.remove_edge(node1, node2)
            self.change_link(node1, node2, -1)
        else:
            self.logging.warning("remove link (%d, %d) does not exit" % (node1, node2))

    def delete_node(self, node):
        if node in self.__g.nodes:
            for neighbor in list(self.__g[node].keys()):
                self.delete_link(node, neighbor)
            self.__g.remove_node(node)
            Topology.Nodes.pop(node)
            self.position = None
            self.logging.debug("node %d deleted at time %d" % (node, Get_Time()))
        else:
            self.logging.warning("remove node %d does not exit" % node)

    def dump_table(self, node):
        if (node in self.__g.nodes) and (node in Topology.Nodes.keys()):
            self.logging.info('DUMP_TABLE: ' + str(Topology.Nodes[node].table))
        else:
            self.logging.warning("node %d does not exit" % node)

    def send_to_neighbors(self, node, m):
        for neighbor in list(self.__g[node].keys()):
            self.send_to_neighbor(node, neighbor, m)

    def send_to_neighbor(self, node, neighbor, m):
        if (node, neighbor) not in self.__g.edges:
            return
        Event_Queue.Post(
            Event(
                Get_Time() + int(self.__g[node][neighbor]['latency']),
                EVENT_TYPE.ROUTING_MESSAGE_ARRIVAL,
                self,
                neighbor,
                m
            )
        )

    def routing_message_arrival(self, neighbor, m):
        if neighbor in self.__g.nodes:
            Topology.Nodes[neighbor].process_incoming_routing_message(m)

    def node_labels(self):
        return {node : str(node) for node in self.__g.nodes}

    def edge_labels(self):
        return {(node1, node2) : self.__g[node1][node2]['latency'] for node1, node2 in self.__g.edges}

    def draw_topology(self):
        if self.position == None:
            self.position = nx.spring_layout(self.__g)
        nx.draw_networkx_nodes(self.__g, self.position, node_size=600, node_color='b', alpha=0.7)
        nx.draw_networkx_labels(self.__g, self.position, labels=self.node_labels(), font_size=14, font_color='w')
        nx.draw_networkx_edges(self.__g, self.position, width=2, alpha=0.5)
        nx.draw_networkx_edge_labels(self.__g, self.position, edge_labels=self.edge_labels(), font_size=14)
        plt.axis('off')

        filename = 'Topo_' + time.strftime("%H_%M_%S", time.localtime()) + '_Time_' + str(Get_Time()) + '.png'
        plt.savefig(OUTPUT_PATH + filename) # call savefig before show
        plt.show()
        plt.close(OUTPUT_PATH + filename)
        self.wait()

    def draw_path(self, source, destination):
        user_path = [(0, 1), (1, 3), (3, 4)]
        correct_path = [(0, 1), (1, 2), (2, 3), (3, 4)]

        if self.position == None:
            self.position = nx.spring_layout(self.__g)

        red_nodes = [source, destination]
        blue_nodes = list(self.__g.nodes)
        for node in red_nodes:
            blue_nodes.remove(node)

        nx.draw_networkx_nodes(self.__g, self.position, nodelist=blue_nodes, node_size=600, node_color='b', alpha=0.7)
        nx.draw_networkx_nodes(self.__g, self.position, nodelist=red_nodes, node_size=700, node_color='r', alpha=0.6)
        nx.draw_networkx_labels(self.__g, self.position, labels=self.node_labels(), font_size=14, font_color='w')

        nx.draw_networkx_edges(self.__g, self.position, width=2, alpha=0.5)
        nx.draw_networkx_edges(self.__g, self.position, edgelist=user_path, width=6, edge_color='r', alpha=0.4)
        nx.draw_networkx_edges(self.__g, self.position, edgelist=correct_path, width=3, edge_color='g', alpha=0.8)
        nx.draw_networkx_edge_labels(self.__g, self.position, edge_labels=self.edge_labels(), font_size=14)
        plt.axis('off')

        filename = 'Topo_' + time.strftime("%H_%M_%S", time.localtime()) + '_Time_' + str(Get_Time()) + '.png'
        plt.savefig(OUTPUT_PATH + filename)  # call savefig before show
        plt.show()
        plt.close(OUTPUT_PATH + filename)
        self.wait()


    def wait(self):
        if self.step == STEP_COMMAND[2]:
            return
        input('Press Enter to Continue...')


    def load_command_file(self, file):
        try:
            f = open(file)
            for line in f.readlines():
                line = line.strip()
                if line == "" or line[0] == '#':
                    continue

                items = line.split(' ')
                time_stamp = int(items[0])
                event_type = items[1]

                num_args = len(items) - 2
                if event_type == EVENT_TYPE.PRINT:
                    Event_Queue.Post(Event(time_stamp, event_type, self, "".join(items[2:])))
                elif num_args < 0 or num_args > 3:
                    sys.stderr.write(line)
                    raise BufferError
                elif num_args == 0:
                    Event_Queue.Post(Event(time_stamp, event_type, self))
                elif num_args == 1:
                    Event_Queue.Post(Event(time_stamp, event_type, self, int(items[2])))
                elif num_args == 2:
                    Event_Queue.Post(Event(time_stamp, event_type, self, int(items[2]), int(items[3])))
                elif num_args == 3:
                    Event_Queue.Post(Event(time_stamp, event_type, self, int(items[2]), int(items[3]), int(items[4])))
            f.close()

        except IOError as e:
            print("Can not open file " + file)
            print(e)
            sys.exit(-1)

        except BufferError:
            print("File with wrong format " + file)
            sys.exit(-1)

        except Exception as e:
            print("File with wrong format " + file)
            print(e)
            traceback.print_exc()
            sys.exit(-1)


def Send_To_Neighbors(node, m):
    Topology.this.send_to_neighbors(node.id, m)

def Send_To_Neighbor(node, neighbor, m):
    Topology.this.send_to_neighbor(node.id, neighbor, m)

def Get_Time():
    return Event_Queue.Current_Time