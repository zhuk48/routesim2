from simulator.node import *

class Generic_Node(Node):
    def __init__(self, id, sim):
        super().__init__(id, sim)
        self.table = Generic_Table()

    def __str__(self):
        return "A Generic Node: " + str(self.id) + "\n"

    def link_has_been_updated(self, neighbor, latency):
        pass

    def process_incoming_routing_message(self, m):
        self.send_to_neighbors(m)

    def get_next_hop(self, destination):
        if self.get_neighbors() != None:
            return self.get_neighbors()[0]
        return -1

    def get_routing_table(self):
        return self.table


class Generic_Message(Message):
    def __str__(self):
        return "A Generic Message\n"


class Generic_Table(Table):
    def __str__(self):
        return "A Generic Table\n"