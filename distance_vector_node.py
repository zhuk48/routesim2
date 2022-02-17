from simulator.node import Node

#Why doesn't Python have structs like C???
#DV list:
# [cost, next_hop, seq]

class Distance_Vector_Node(Node):
    def __init__(self, id):
        super().__init__(id)
        self.dist = {} # dictionary to hold distances and paths to given node

    # Return a string
    def __str__(self):
        return "Rewrite this function to define your node dump printout"

    # Fill in this function
    def link_has_been_updated(self, neighbor, latency):
        # latency = -1 if delete a link

        # recalculating distance:
        temp_set = frozenset(self.id, neighbor)
        if temp_set in self.dist.keys():
            self.dist[temp_set][0] = latency 
            self.dist[temp_set][1] = neighbor
            self.dist[temp_set][2] += 1
        else:
            self.dist[temp_set][0] = latency 
            self.dist[temp_set][1] = neighbor
            self.dist[temp_set][2] = 0
    # Fill in this function
    def process_incoming_routing_message(self, m):
        pass

    # Return a neighbor, -1 if no path to destination
    def get_next_hop(self, destination):
        temp_set = frozenset(self.id, destination)
        if temp_set in self.dist.keys():
            return self.dist[temp_set][1]
        else:
            return -1
            
    # recalculate all DVs after a link update or when routing message is recieved
    def recalculate_dv():
        pass
