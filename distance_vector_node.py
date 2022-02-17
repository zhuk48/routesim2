from simulator.node import Node

#Why doesn't Python have structs like C???
#DV list:
# [cost, next_hop, timestamp]

class Distance_Vector_Node(Node):
    def __init__(self, id):
        super().__init__(id)
        self.dist = {} # dictionary to hold distances and paths to given node
        self.links = {} # dictionary containing all linkes connected to given node

    # Return a string
    def __str__(self):
        return "Rewrite this function to define your node dump printout"

    # Fill in this function
    def link_has_been_updated(self, neighbor, latency):
        # latency = -1 if delete a link
        self.recalculate_dist(neighbor, latency)
        pass

    # Fill in this function
    def process_incoming_routing_message(self, m):
        pass

    # Return a neighbor, -1 if no path to destination
    def get_next_hop(self, destination):
        temp_set = frozenset(self.id, destination)
        if temp_set in self.dist.keys():
            return self.dist[temp_set]
        else:
            return -1

    # recalculates distances to all nodes after reciving new information
    def recalculate_dist(self, updated_link, updated_lat):
        pass