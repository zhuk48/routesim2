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
        if latency == -1 and neighbor in self.neighbors:

            self.neighbors.remove(neighbor)
        else:
            self.neighbors.append(neighbor)
            # self.send_to_neighbors(Generic_Message())
            self.send_to_neighbor(neighbor, Generic_Message())

        self.logging.debug('link update, neighbor %d, latency %d, time %d' % (neighbor, latency, self.get_time()))

    def process_incoming_routing_message(self, m):
        self.logging.debug("receive a message at Time %d. " % self.get_time() + str(m))

    # Return a neighbor, -1 if no path to destination
    def get_next_hop(self, destination):
        if self.neighbors != []:
            return self.neighbors[0]
        return -1

    def get_routing_table(self):
        return self.table


class Generic_Message(Message):
    def __str__(self):
        return "A Generic Message"


class Generic_Table(Table):
    def __str__(self):
        return "A Generic Table, very cute (●ˇ∀ˇ●)"
