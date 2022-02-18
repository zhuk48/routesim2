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
                change = self.dist[neighbor].cost - latency
                # only update if change
                if change != 0:
                    self.dist[neighbor].cost = latency
                    self.dist[neighbor].seq += 1
                    # recalculate DV's
                    # specfically recalculate DV's for any path that travels through updated node
                    for key in self.dist:
                        print("path for node #" + str(self.id) + " for key " + str(key) + ":")
                        print(self.dist[key].path)
                        if neighbor in self.dist[key].path: # nodes where the updated link is incl in path
                            self.dist[key].cost = self.dist[key].cost - change
            self.broadcast_change()
                     
        else: #link DNE, create new one
            self.dist[neighbor] = dv(latency, 0, [self.id, neighbor])
            self.broadcast_change()

    def process_incoming_routing_message(self, m):
        n, new_table = json.loads(m)
        new_table = json.loads(new_table)
        # converting json back to class
        print("INCOMING TABLE from node" + str(n))
        for key in new_table:
            new_table[key] = dv(new_table[key]['cost'], new_table[key]['seq'], new_table[key]['path'])
            print(new_table[key].cost)
            print(new_table[key].path)
            #if not new_table[key].path:
                #print("PATH IS NONE")
        #print(new_table)
        print("CURRENT TABLE for node " + str(self.id))
        for key in self.dist:
            print(self.dist[key].cost)
            print(self.dist[key].path)

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
                # link in current table, need to update
                if self.dist[key].cost > self.dist[n].cost + new_table[key].cost:
                    dv_updated = True
                    self.dist[key] = copy.deepcopy(new_table[key])
                    self.dist[key].cost += self.dist[n].cost
                    self.dist[key].path.insert(0,self.id)
        if dv_updated == True:
            self.broadcast_change()

    # Return a neighbor, -1 if no path to destination
    def get_next_hop(self, destination):
        if destination in self.dist:
            return self.dist[destination].cost
        else:
            return -1
    
    def to_json(self, obj):
        return json.dumps(obj, default=lambda obj: obj.__dict__)

    def broadcast_change(self):
        dict_json = self.to_json(self.dist)
        m = json.dumps((self.id, dict_json))
        self.send_to_neighbors(m)
