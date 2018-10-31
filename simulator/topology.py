import sys
import networkx as nx
import logging
import traceback

from simulator.config import *
from simulator.event import Event
from simulator.event_queue import Event_Queue


class Topology:

    Nodes = {}

    def __init__(self, algorithm):
        self.__g = nx.Graph()
        self.node_cls = ROUTE_ALGORITHM_NODE[algorithm]
        self.logging = logging.getLogger('Topology')
        Topology.Nodes = {}


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
        if (latency != -1):
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






    # TODO: DELETE_NODE = "DELETE_NODE"
    # TODO: DELETE_LINK = "DELETE_LINK"
    # TODO: PRINT = "PRINT"
    # TODO: DRAW_TOPOLOGY = "DRAW_TOPOLOGY"
    # TODO: DRAW_PATH = "DRAW_PATH"
    # TODO: DUMP_TABLE = "DUMP_TABLE"





def Send_To_Neighbors(node, m):
    pass


def Get_Time():
    return Event_Queue.Current_Time