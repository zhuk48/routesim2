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

    # Return a string
    def __str__(self):
        return "Rewrite this function to define your node dump printout"

    # Fill in this function
    def link_has_been_updated(self, neighbor, latency):
        #print(self.dist)
        #for key in self.dist:
            #print(self.dist[key].path)
        if neighbor in self.dist: #link already exists, updating value
            # latency = -1 if delete a link
            if latency == -1:
                del self.dist[neighbor]
            else:
                if self.dist[neighbor].cost > latency:
                    #self.dist[neighbor].cost = latency
                    #self.dist[neighbor].path = [self.id, neighbor]
                    #self.dist[neighbor].seq += 1
                    # RECALCULATE DV! HOW???
                    self.broadcast_change(0)
                elif latency > self.dist[neighbor].cost:
                    self.dist[neighbor].cost = latency
                    self.dist[neighbor].path = []
                    self.dist[neighbor].seq += 1
                    self.broadcast_change(0)
                     
        else: #link DNE, create new one
            self.dist[neighbor] = dv(latency, 0, [self.id, neighbor])
            self.broadcast_change(0)

    def process_incoming_routing_message(self, m):
        num, new_table = json.loads(m)
        n = int(num)
        new_table = json.loads(new_table)
        # converting json back to class
        print("INCOMING TABLE from node" + str(n))
        for key in new_table:
            new_table[key] = dv(new_table[key]['cost'], new_table[key]['seq'], new_table[key]['path'])
            print(key)
            print(new_table[key].cost)
            print(new_table[key].path)
            print(new_table[key].seq)
        #print(new_table)

        # JSONs suck and this line converts keys in new_table from strings to ints
        new_table = {int(key):value for key, value in new_table.items()}

        print("CURRENT TABLE for node " + str(self.id))
        for key in self.dist:
            print(key)
            print(self.dist[key].cost)
            print(self.dist[key].path)
            print(self.dist[key].seq)

        dv_updated = False   
        for key in new_table:
            if key not in self.dist:
                dv_updated = True
                # link in incoming message not in current table
                # add to current table
                self.dist[key] = copy.deepcopy(new_table[key])
                self.dist[key].path.insert(0, self.id)
                self.dist[key].cost += self.dist[n].cost 
                #print(new_table[key].path)
            else:
                if (new_table[key].seq > self.dist[key].seq) and key != n:
                    dv_updated = True
                    self.dist[key] = copy.deepcopy(new_table[key])
                    self.dist[key].cost += self.dist[n].cost
                    self.dist[key].path.insert(0,self.id)
                # link in current table, need to update
                if self.dist[key].cost > self.dist[n].cost + new_table[key].cost:
                    dv_updated = True
                    self.dist[key] = copy.deepcopy(new_table[key])
                    self.dist[key].cost += self.dist[n].cost
                    self.dist[key].path.insert(0,self.id)

        print("NEW TABLE for node " + str(self.id))
        for key in self.dist:
            print(key)
            print(self.dist[key].cost)
            print(self.dist[key].path)

        if dv_updated == True:
            self.broadcast_change(0)

    # Return a neighbor, -1 if no path to destination
    def get_next_hop(self, destination):
        if destination in self.dist:
            return self.dist[destination].path[1]
        else:
            return -1
    
    def to_json(self, obj):
        return json.dumps(obj, default=lambda obj: obj.__dict__)

    def broadcast_change(self, n):
        dict_json = self.to_json(self.dist)
        m = json.dumps((self.id, dict_json))
        if n == 0:
            self.send_to_neighbors(m)
        else:
            self.send_to_neighbor(n, m)
