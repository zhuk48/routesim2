import math
from simulator.node import Node
import heapq
import json
class Graph:
    def __init__(self):
        self.graph = {}
    def add_edge(self, n1, n2, latency):
        if n1 not in self.graph: #pretty sure this code only needs 1 if/else statement
            self.graph[n1] = [[n2, latency]]
        else:
            self.graph[n1].append([n2, latency])
        if n2 not in self.graph:
            self.graph[n2] = [[n1, latency]]
        else:
            self.graph[n2].append([n1, latency])

    def find_neighbor(self, n1, n2): #get index of neighbor in list of neighbors
        if n1 in self.graph:
            neighbor = self.graph[n1]
            for i in range(len(neighbor)):
                if neighbor[i][0] == n2:
                    return i
            return None
        else:
            return None

    def remove_edge(self, n1, n2):
        index1 = self.find_neighbor(n1, n2)
        if index1 is not None:
            index2 = self.find_neighbor(n2, n1)
            del self.graph[n1][index1]
            del self.graph[n2][index2]

    def update_edge(self, n1, n2, latency):
        index1 = self.find_neighbor(n1, n2)
        if index1 is not None:
            index2 = self.find_neighbor(n2, n1)
            self.graph[n1][index1][1] = latency
            self.graph[n2][index2][1] = latency
    def get_neighbors(self, n1):
        return self.graph[n1]

    def dijkstra(self, start):
        vis = {}
        prev = {}
        dist = {}
        for key in self.graph:
            vis[key] = False
            prev[key] = None
            dist[key] = math.inf
        dist[start] = 0
        pq = []
        heapq.heappush(pq, (0, start))
        while pq:
            minCost, node = heapq.heappop(pq)
            vis[node] = True
            if dist[node] < minCost:
                continue
            for neighbor in self.graph[node]:
                if vis[neighbor[0]] == True:
                    continue
                newDist = dist[node] + neighbor[1]
                if newDist < dist[neighbor[0]]:
                    prev[neighbor[0]] = node
                    dist[neighbor[0]] = newDist
                    heapq.heappush(pq, (newDist, neighbor[0]))
        return dist, prev

class Link_State_Node(Node):
    def __init__(self, id):
        super().__init__(id)
        self.graph = Graph()
        self.seq_n = {}
        self.path = {}
    # Return a string
    def __str__(self):
        return f"<Node {self.id}, Reachable Nodes and next hops: {self.path}>"

    # Fill in this function
    def link_has_been_updated(self, neighbor, latency):
        s = frozenset((self.id, neighbor))
        if s not in self.seq_n:
            self.seq_n[s] = 0
        self.seq_n[s] += 1
        # latency = -1 if delete a link
        #only change graph if latency is diffrent for that specefic edge
        # neighbor_index = self.graph.find_neighbor(self.id, neighbor)
        # if self.graph[self.id][neighbor_index][1] == latency: #dont even send msg so just return
        #     return
        if latency == -1:
            self.graph.remove_edge(self.id, neighbor)
        else:
            if self.graph.find_neighbor(self.id, neighbor) is not None: 
                self.graph.update_edge(self.id, neighbor, latency)
            else:
                self.graph.add_edge(self.id, neighbor, latency)
                #a new edge has been created so u need to make it up to date by giving it information

        distances, prev = self.graph.dijkstra(self.id)
        # print(self.id, self.graph.graph)
        self.path = prev 
        msg = {
            'my_id': self.id,
            'neighbor_id': neighbor,
            'cost': latency,
            'seq_n': self.seq_n[s]
        }
        self.send_to_neighbors(json.dumps(msg))
        #create message include 2 node ids and the cost and the sequence number 
        #share graph with neighbor


    # Fill in this function
    def process_incoming_routing_message(self, m):
        msg = json.loads(m)
        msg = {key: int(value) for key, value in msg.items()} #i want my values to be ints and not strings
        id_of_msg = msg['my_id']
        neighbor_id = msg['neighbor_id']
        cost = msg['cost']
        seq_n = msg['seq_n']
        s = frozenset((neighbor_id, id_of_msg))
        changed = False
        if s in self.seq_n: #seq_n originally just an empty dictionary so gotta check if its a first packet
            if self.seq_n[s] < seq_n:
                if cost == -1:
                    self.graph.remove_edge(id_of_msg, neighbor_id)
                    changed = True
                else:
                    self.graph.update_edge(id_of_msg, neighbor_id, cost)
                    changed = True
            else:
                return #gets an infinite loop highkey if i dont do this 
        else:
            if cost >= 0:
                self.graph.add_edge(id_of_msg, neighbor_id, cost)
                changed = True
        # if changed == True:
        self.seq_n[s] = seq_n
        dist, prev = self.graph.dijkstra(self.id)
        self.path = prev
        self.send_to_neighbors(json.dumps(msg))
        

    # Return a neighbor, -1 if no path to destination
    def get_next_hop(self, destination):
        if destination in self.path:
            curr_node = destination
            #go backwards 
            while self.path[curr_node] != self.id and self.path[curr_node] is not None:
                curr_node = self.path[curr_node]
            if curr_node is not None:
                return curr_node
            else:
                return -1
        else:
            return -1
