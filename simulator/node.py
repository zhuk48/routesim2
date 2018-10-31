import logging

class Node:
    def __init__(self, id):
        self.id = id
        self.table = Table()
        self.neighbors = []
        self.logging = logging.getLogger('Node %d' % self.id)

    def __str__(self):
        pass

    def link_has_been_updated(self, neighbor, latency):
        pass

    def process_incoming_routing_message(self, m):
        pass

    def get_next_hop(self, destination):
        pass

    def get_routing_table(self):
        pass

    def send_to_neighbors(self, m):
        from simulator.topology import Send_To_Neighbors
        Send_To_Neighbors(self, m)

    def get_time(self):
        from simulator.topology import Get_Time
        return Get_Time()


class Message:
    def __str__(self):
        pass

class Table:
    def __str__(self):
        pass

class Link:
    def __init__(self, node1, node2, latency):
        self.node1 = node1
        self.node2 = node2
        self.latency = latency

    def __str__(self):
        return "Link: " + str(self.node1) + " " + str(self.node2) + " Latency: " + str(self.latency) + "\n"

