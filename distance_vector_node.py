from operator import ne
from simulator.node import Node
import copy
import json

#Why doesn't Python have structs like C???
# self.dist:
# b : {DV}
# DV list:
# [cost_ab, path_ab , seq]

class dv:
    def __init__(self):
        self.cost = 0
        self.path = []
        self.seq = 0

class Distance_Vector_Node(Node):
    def __init__(self, id):
        super().__init__(id)
        self.dist = {} # dictionary to hold distances and paths to given node
        self.dist[self.id] = dv(0, [self.id], 0)

    # Return a string
    def __str__(self):
        return "Rewrite this function to define your node dump printout"

    # Fill in this function
    def link_has_been_updated(self, neighbor, latency):
        if neighbor in self.dist: #link already exists, updating value
            # latency = -1 if delete a link
            if latency == -1:
                del self.dist[neighbor]
            else:
                change = self.dist[neighbor].cost - latency
                # only update if change
                if change != 0:
                    # recalculate DV's
                    # specfically recalculate DV's for any path that travels through updated node
                    for key in self.dist:
                        if neighbor in self.dist[key][1]: # nodes where the updated link is incl in path
                            self.dist[key].cost = self.dist[key].cost - change
                            self.dist[key].seq += 1
            self.broadcast_change()
                     
        else: #link DNE, create new one
            self.dist[neighbor] = dv(latency, [self.id, neighbor], 0)
            self.broadcast_change()

    def process_incoming_routing_message(self, m):
        n, new_table = m.loads(m)
        if not self.dist == new_table:
            for key in new_table:
                if key not in self.dist:
                    # link in incoming message not in current table
                    # add to current table
                    self.dist[key] = dv(self.dist[n].cost + new_table[key].cost,
                                        new_table[key].path.insert(0,self.id),
                                        new_table[key].seq)
                else:
                    # link in current table, need to update
                    if self.dist[key].cost > self.dist[n].cost + new_table[key].cost:
                        self.dist[key].cost = self.dist[n].cost + new_table[key].cost
                        self.dist[key].path = new_table[key].path.insert(0,self.id)
                        self.dist[key].seq = new_table[key].seq
            self.broadcast_change()

    # Return a neighbor, -1 if no path to destination
    def get_next_hop(self, destination):
        if destination in self.dist:
            return self.dist[destination].cost
        else:
            return -1
    

    def broadcast_change(self):
        m = json.dumps((self.id, self.dist))
        self.send_to_neighbors(m)
