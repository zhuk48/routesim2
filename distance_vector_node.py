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
    def __init__(self, cost, seq, path=[]):
        self.cost = cost
        self.path = path
        self.seq = seq

class Distance_Vector_Node(Node):
    def __init__(self, id):
        super().__init__(id)
        self.dist = {} # dictionary to hold distances and paths to given node
        self.dist[self.id] = dv(0, 0, [self.id])
        self.ndist = {} # dictionary to hold DVs of neighbors

    # Return a string
    def __str__(self):
        o = "Node: " + str(self.id) + "DV: " + str(self.dv) 
        return o

    # Fill in this function
    def link_has_been_updated(self, neighbor, latency):
        if neighbor in self.dist: #link already exists, updating value
            # latency = -1 if delete a link
            if latency == -1:
                del self.dist[neighbor]
                del self.ndist[neighbor]
            else:
                self.dist[neighbor].cost = latency
                self.dist[neighbor].seq += 1
                     
        else: #link DNE, create new one
            self.dist[neighbor] = dv(latency, 0, [self.id, neighbor])
        
        self.recalculate_dist()
        self.broadcast_change(0)

    def process_incoming_routing_message(self, m):
        n, new_table = json.loads(m)
        new_table = json.loads(new_table)
        # converting json back to class
        for key in new_table:
            new_table[key] = dv(new_table[key]['cost'], new_table[key]['seq'], new_table[key]['path'])

        # JSONs suck and this line converts keys in new_table from strings to ints
        # this line was taken from stack overflow
        new_table = {int(key):value for key, value in new_table.items()}
        
        # updating incoming neighbor DV in self.ndist
        self.ndist[n] = new_table

        if self.recalculate_dist() == True:
            self.broadcast_change(0)

    # Return a neighbor, -1 if no path to destination
    def get_next_hop(self, destination):
        if destination in self.dist:
            return self.dist[destination].path[1]
        else:
            return -1

    def recalculate_dist(self):
        dv_updated = False

        print("old dv at node " + str(self.id))
        for key in self.dist:
            print(key)
            print(self.dist[key].cost)
            print(self.dist[key].path)

        for key in self.dist: # loop through all current entries in DV
            curr_best = self.dist[key].cost

            # checking for updated distances
            for neighbor in self.ndist: # checking all neighbors' DVs
                if key in self.ndist[neighbor] and key != neighbor: # if this neighbor has a path to the destination
                    # we also don't want to copy the "identification entry in DV" (cost of n to n is 0)
                    if curr_best > self.ndist[neighbor][key].cost + self.dist[neighbor].cost: # quicker path to mykey via neighbor
                        dv_updated = True
                        self.dist[key] = copy.deepcopy(self.ndist[neighbor][key])
                        self.dist[key].cost += self.dist[neighbor].cost
                        self.dist[key].path.insert(0,self.id)
        

        print("NEW dv at node " + str(self.id))
        for key in self.dist:
            print(key)
            print(self.dist[key].cost)
            print(self.dist[key].path)

        return dv_updated
        
    
    # json.dumps can't handle classes by default, so this helper function (found online) was written to faciliate that
    def to_json(self, obj):
        return json.dumps(obj, default=lambda obj: obj.__dict__)

    # when n=0, broadcast to all neighbors, else n is specific neighbor to broadcast to
    def broadcast_change(self, n):
        dict_json = self.to_json(self.dist)
        m = json.dumps((self.id, dict_json))
        if n == 0:
            self.send_to_neighbors(m)
        else:
            self.send_to_neighbor(n, m)
