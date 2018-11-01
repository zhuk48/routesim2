from simulator.node import Node, Message, Table

class Distance_Vector_Node(Node):
    def __init__(self, id):
        super().__init__(id)
        self.table = Distance_Vector_Table()

    # Return a string
    def __str__(self):
        pass

    # Fill in this function
    def link_has_been_updated(self, neighbor, latency):
        # latency = -1 if delete a link
        pass

    # Fill in this function
    def process_incoming_routing_message(self, m):
        pass

    # Return a neighbor, -1 if no path to destination
    def get_next_hop(self, destination):
        return -1

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