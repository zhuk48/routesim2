
from simulator.node import Node
import copy
import json
import math

## class to hold information about distance vectors
class dv:
    def __init__(self, cost, seq, path=[]):
        self.cost = cost
        self.path = path
        self.seq = seq

class Distance_Vector_Node(Node):
    def __init__(self, id):
        super().__init__(id)
        self.dist = {} # dictionary that takes correspoinding destinations and returns the DV class for that destination node
        self.dist[self.id] = dv(0, 0, [self.id]) # initializing "self" DV
        self.ndist = {} # dictionary that takes a neighboring node and returns its dictionary of DVs
        self.direct_costs = {} # dictionary that holds node's neighbors and direct path costs to those neighbors (not neccisarily the fastest, but the one hop cost)
        # ^^ was told this would be helpful in OH

    # Return a string
    def __str__(self):
        o = "Node: " + str(self.id) + "DV: " + str(self.dv) 
        return o

    def link_has_been_updated(self, neighbor, latency):
        if neighbor in self.dist: #link already exists, updating value
            # latency = -1 if delete a link
            if latency == -1:
                self.direct_costs[neighbor] = math.inf
                del self.ndist[neighbor]

                for key in self.dist:
                    if neighbor in self.dist[key].path:
                        self.dist[key].cost = math.inf
                        self.dist[key].seq += 1
                        self.dist[key].path.clear()
            else:
                self.direct_costs[neighbor] = latency
                self.dist[neighbor].seq += 1
                self.dist[neighbor].cost = latency
                self.dist[neighbor].path = [neighbor]

        else: #link DNE, create new one
            self.direct_costs[neighbor] = latency  
            self.dist[neighbor] = dv(latency, 0, [neighbor])

        self.broadcast_change()
        #self.recalculate_dist()
        
    def process_incoming_routing_message(self, m):
        n, new_table = json.loads(m)
        new_table = json.loads(new_table)
        # converting json back to class


        for key in new_table:
            new_table[key] = dv(new_table[key]['cost'], new_table[key]['seq'], new_table[key]['path'])

        # JSONs suck and this line converts keys in new_table from strings to ints
        # this line was taken from stack overflow
        new_table = {int(key):value for key, value in new_table.items()}

        self.ndist[n] = new_table
        self.recalculate_dist()
        #self.broadcast_change(0)

    # Return a neighbor, -1 if no path to destination
    def get_next_hop(self, destination):
        if destination in self.dist:
            return self.dist[destination].path[0]
        else:
            return -1

    def recalculate_dist(self):
        dv_updated = False

        #print("old dv at node " + str(self.id))
        #for key in self.dist:
        #    print(key, self.dist[key].cost, self.dist[key].path)

        # checking for faster path via direct connections
        for neighbor in self.direct_costs:
            if neighbor not in self.dist:
                dv_updated = True
                self.dist[neighbor] = dv(self.direct_costs[neighbor], [neighbor])
            elif self.dist[neighbor].cost > self.direct_costs[neighbor]:
                dv_updated = True
                self.dist[neighbor].cost = self.direct_costs[neighbor]
                self.dist[neighbor].path = [neighbor]

        # checking for faster paths via neighbors
        for n in self.ndist:
            for nkey in self.ndist[n]:
                if nkey not in self.dist: # found new node
                    dv_updated = True
                    self.dist[nkey] = copy.deepcopy(self.ndist[n][nkey])
                    self.dist[nkey].cost += self.direct_costs[n]
                    self.dist[nkey].path.insert(0,n)
                else:
                    if self.ndist[n][nkey].seq > self.dist[nkey].seq:
                        dv_updated = True
                        self.dist[nkey] = copy.deepcopy(self.ndist[n][nkey])
                        self.dist[nkey].cost += self.direct_costs[n]
                        self.dist[nkey].path.insert(0,n)
                        
                    if self.id not in self.ndist[n][nkey].path: # avoids loops: 
                        if self.dist[nkey].cost > self.direct_costs[n] + self.ndist[n][nkey].cost:
                            dv_updated = True
                            self.dist[nkey] = copy.deepcopy(self.ndist[n][nkey])
                            self.dist[nkey].cost += self.direct_costs[n]
                            self.dist[nkey].path.insert(0,n)

        if dv_updated == True:
            self.broadcast_change()
        
    
    # json.dumps can't handle classes by default, so this helper function (found online) was written to faciliate that
    def to_json(self, obj):
        return json.dumps(obj, default=lambda obj: obj.__dict__)

    # when n=0, broadcast to all neighbors, else n is specific neighbor to broadcast to
    def broadcast_change(self):
        dict_json = self.to_json(self.dist)
        m = json.dumps((self.id, dict_json))
        self.send_to_neighbors(m)
