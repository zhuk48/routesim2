from simulator.node import *

class Distance_Vector_Node(Node):
    def __init__(self, id, sim):
        super().__init__(id, sim)
        self.table = Distance_Vector_Table()

    # Return a string
    def __str__(self):
        pass

    # Fill in this function
    def link_has_been_updated(self, neighbor, latency):
        pass

    # Fill in this function
    def process_incoming_routing_message(self, m):
        pass

    # Return a neighbor
    def get_next_hop(self, destination):
        return 0

    # Return a Table()
    def get_routing_table(self):
        return self.table


class Distance_Vector_Message(Message):
    # Return a string
    def __str__(self):
        pass


class Distance_Vector_Table(Table):
    # Return a string
    def __str__(self):
        pass