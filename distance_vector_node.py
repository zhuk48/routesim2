from operator import ne
from simulator.node import Node
import copy
import json

#Why doesn't Python have structs like C???
# self.dist:
# b : {DV}
# DV list:
# [cost_ab, path_ab , seq]

class Distance_Vector_Node(Node):
    def __init__(self, id):
        super().__init__(id)
        self.dist = {} # dictionary to hold distances and paths to given node

    # Return a string
    def __str__(self):
        return "Rewrite this function to define your node dump printout"

    # Fill in this function
    def link_has_been_updated(self, neighbor, latency):
        if neighbor in self.dist.keys(): #link already exists, updating value
            # latency = -1 if delete a link
            if latency == -1:
                del self.dist[neighbor]
            else:
                change = self.dist[neighbor][0] - latency
                # only update if change
                if change != 0:
                    # recalculate DV's
                    # specfically recalculate DV's for any path that travels through updated node
                    for key in self.dist:
                        if neighbor in self.dist[key][1]: # nodes where the updated link is incl in path
                            self.dist[key][0] = self.dist[key][0] - change
                            self.dist[key][2] += 1
            self.broadcast_change()
                     
        else: #link DNE, create new one
            self.dist[neighbor] = []
            self.dist[neighbor][0] = latency 
            self.dist[neighbor][1] = [self.id, neighbor]
            self.dist[neighbor][2] = 0
            self.broadcast_change()

    def process_incoming_routing_message(self, m):
        n = m.loads(m)[0]
        new_table = m.loads(m)[1]
        if not self.dist == new_table:
            ## NEED TO DO
            pass



    # Return a neighbor, -1 if no path to destination
    def get_next_hop(self, destination):
        temp_set = frozenset(self.id, destination)
        if temp_set in self.dist.keys():
            return self.dist[temp_set][1]
        else:
            return -1
    

    def broadcast_change(self):
        m = json.dumps(self.id, self.dist)
        self.send_to_neighbors(m)
