from simulator.node import Node, Message, Table

class Generic_Node(Node):
    def __init__(self, id):
        super().__init__(id)
        self.table = Generic_Table()
        self.logging.debug("new node %d" % self.id)

    def __str__(self):
        return "A Generic Node: " + str(self.id) + "\n"

    def link_has_been_updated(self, neighbor, latency):
        # latency = -1 if delete a link
        if latency == -1:
            self.neighbors.remove(neighbor)
        else:
            self.neighbors.append(neighbor)
        self.logging.debug('link update, neighbor %d, latency %d, time %d' % (neighbor, latency, self.get_time()))


    def process_incoming_routing_message(self, m):
        self.send_to_neighbors(m)

    def get_next_hop(self, destination):
        if self.neighbors != []:
            return self.neighbors[0]
        return -1

    def get_routing_table(self):
        return self.table


class Generic_Message(Message):
    def __str__(self):
        return "A Generic Message\n"


class Generic_Table(Table):
    def __str__(self):
        return "A Generic Table\n"