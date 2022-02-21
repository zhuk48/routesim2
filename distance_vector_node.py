from simulator.node import Node

import copy
import json

## class to hold information about distance vectors
class dv:
    def __init__(self, cost, path):
        self.cost = cost
        self.path = path

    # this method was taken from S.O. because apparently 
    # equality in Python is way more complicated than I ever imagined ¯\_(ツ)_/¯
    def __eq__(self, other):
        if not isinstance(other, dv):
            return NotImplemented
        return self.cost == other.cost and self.path == other.path

class Distance_Vector_Node(Node):
    def __init__(self, id):
        super().__init__(id)
        self.dist = {} # dictionary that takes correspoinding destinations and returns the DV class for that destination node
        self.dist[self.id] = dv(0, [self.id]) # initializing "self" DV
        self.ndist = {} # dictionary that takes a neighboring node and returns its DVs to its known nodes
        self.nseq = {} #  dictionary that holds the timestamp of each neighbors DVs
        self.direct_costs = {} # dictionary that holds node's neighbors and direct path costs to those neighbors (not neccisarily the fastest, but the one hop cost)
        # ^^ was told this would be helpful in OH

    # Return a string
    def __str__(self):
        o = "Node: " + str(self.id) + "DV: " + str(self.dist) 
        return o

    # Fill in this function
    def link_has_been_updated(self, neighbor, latency):
        if neighbor in self.direct_costs: #link already exists, updating/deleting value
            # latency = -1 if delete a link
            if latency == -1:
                del self.direct_costs[neighbor]
                del self.ndist[neighbor]
                del self.nseq[neighbor]
            else:
                self.direct_costs[neighbor] = latency
                self.dist[neighbor].cost = latency
                self.dist[neighbor].path = [self.id, neighbor]
            
        else: #link DNE, create new one
            self.direct_costs[neighbor] = latency
            self.dist[neighbor] = dv(latency, [self.id, neighbor])

        self.recalculate_dist()

    # Fill in this function
    def process_incoming_routing_message(self, m):
        n, t, new_table = json.loads(m) 
        new_table = json.loads(new_table)
        # n = the neighbor packet is being received from
        # t = the timestamp of the incoming packet
        
        # if incoming packet is older than current info
        if n in self.ndist and t <= self.nseq[n]:
            pass
        else:
            # "unpacking" the JSON into a dict
            for key in new_table:
                new_table[key] = dv(new_table[key]['cost'], new_table[key]['path'])
            # JSONs suck and this line converts keys in new_table from strings to ints
            # this line was taken from stack overflow
            new_table = {int(key):value for key, value in new_table.items()}

            self.ndist[n] = new_table
            self.nseq[n] = t

            self.recalculate_dist()

    # Return a neighbor, -1 if no path to destination
    def get_next_hop(self, destination):
        if destination in self.dist:
            print("next hops")
            print(self.dist[destination].path)
            return self.dist[destination].path[0]
        else:
            return -1

    def recalculate_dist(self):
        new_dv = {}
        # checking for faster paths via neighbors's neighbors
        for n in self.ndist:
            for dnode in self.ndist[n]:
                if self.id not in self.ndist[n][dnode].path: # avoids loops and counting to infinity
                    if dnode not in new_dv: # new node
                        new_dv[dnode] = copy.deepcopy(self.ndist[n][dnode])
                        new_dv[dnode].path.insert(0, n)
                        new_dv[dnode].cost += self.direct_costs[n]
                    else: # new node found
                        if new_dv[dnode].cost > self.ndist[n][dnode].cost + self.direct_costs[n]:
                            new_dv[dnode] = copy.deepcopy(self.ndist[n][dnode])
                            new_dv[dnode].path.insert(0, n)
                            new_dv[dnode].cost += self.direct_costs[n]
                        

        # checking for faster paths via direct connections
        for neighbor in self.direct_costs:
            if neighbor not in new_dv:
                new_dv[neighbor] = dv(self.direct_costs[neighbor], [neighbor])
            else:
                if new_dv[neighbor].cost > self.direct_costs[neighbor]:
                    new_dv[neighbor].cost = self.direct_costs[neighbor]
                    new_dv[neighbor].path = [neighbor]
                    

        # only broadcast if self.dist was updated
        # equality in python is more complicated than what meets the eye, man this bug took like 3 hours to figure out
        if (not new_dv == self.dist):
            self.dist = new_dv 
            self.broadcast_change(0)

    # json.dumps can't handle classes by default, so this helper function (found online) was written to faciliate that
    def to_json(self, obj):
        return json.dumps(obj, default=lambda obj: obj.__dict__)

    # if n = 0, broadcast to all, else broadcast to neighbor n
    def broadcast_change(self, n):
        dict_json = self.to_json(self.dist)
        m = json.dumps((self.id, self.get_time(), dict_json))
        if n == 0:
            self.send_to_neighbors(m)
        else:
            self.send_to_neighbor(n, m)