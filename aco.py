
import random 
import copy

class Edge:
    def __init__(self, vertex1, vertex2):       
        self.vertex1 = vertex1
        self.vertex2 = vertex2
        self.weight = 0
        self.pher_amt = 0
        self.prob = 0
    
class Ant:
    def __init__(self, ant): #ant is a list
        self.ant = ant
        self.curr_vertex = None
        self.visted_vertex = []
           
class Vertex:
    def __init__(self, vertex):
        self.vertex = vertex
        self.neighbour = []

        
class Graph:
    def __init__(self):
        self.vertices = []
        self.edges = []
  
    def add_vertex(self, vertex):
        v = Vertex(vertex)
        self.vertices.append(v)

    def add_edge(self, vertex1, vertex2):
        if vertex1 in self.vertices and vertex2 in self.vertices:
            edge1 = Edge(vertex1, vertex2)
            edge2 = Edge(vertex1, vertex2)
            self.edges.append(edge1)
            self.edges.append(edge2)
            vertex1.neighbour.append(vertex2)
            vertex2.neighbour.append(vertex1)
        
    def add_weight(self, vertex1, vertex2, weight_val):
        edge = Edge(vertex1, vertex2)
        if edge in self.edges:
            edge.weight = weight_val

    def update_prob(self, vertex1, vertex2, prob_val):
        edge = Edge(vertex1, vertex2)
        if edge in self.edges:
            edge.prob = prob_val

    def add_phermone(self, vertex1, vertex2, phermone_amt):
        edge = Edge(vertex1, vertex2)
        if edge in self.edges:
            edge.pher_amt = phermone_amt

    def calculate_tour_length(self, tour):
        length = 0
        for i in range(len(tour) - 1):
            length += self.get_edge_weight(tour[i], tour[i + 1])
        return length  

    def get_edge_weight(self, vertex1, vertex2):
        for edge in self.edges:
            if (edge.vertex1 == vertex1 and edge.vertex2 == vertex2) or (edge.vertex1 == vertex2 and edge.vertex2 == vertex1):
                return edge.weight
        return float('inf')  

    def calulate_prob(self, edge_to_take, alpha, beta):
        edge_visibility = 1/edge_to_take.weight
        numerator = (edge_to_take.pher_amt**alpha) * (edge_visibility**beta)

        summation_denominator = 0
        for edge in self.edges:
            e_visibility = 1/edge.weight
            summation_denominator += (edge.pher_amt**alpha) * (e_visibility**beta)
        
        transition_prob = numerator/summation_denominator
        return transition_prob
    

    def optmization(self, Q, alpha, beta , ants): #ants is a list of ant instance 
        shortest_path = None
        shortest_path_length = float('inf')
        shuffled_towns = copy.deepcopy(self.vertices)
        random.shuffle(shuffled_towns)

        for ant in ants:
            if self.vertices:
                curr_vertex = shuffled_towns.pop()
                ant.visited_vertex.append(curr_vertex) 
                ant.curr_vertex = curr_vertex 

        for v in range(len(self.vertices)):
            for ant in ants:
                curr_vertex = ants.curr_vertex  #get the current vertex so that we can get its neighbors and respective probalities of going to a neighbor
            
                greatest_prob = 0
                edge_to_take = None
                vertex_to_go = None
                potential_edges = []

                for neighbor in curr_vertex.neighbour: #getting the neighbour town: thi
                    if neighbor not in ant.visited_vertex: #if that town has not been visited
                        e = Edge(curr_vertex, neighbor)
                        potential_edges.append(e)
                    else: #check this
                        e = Edge(curr_vertex, neighbor)
                        e.pher_amt = e.pher_amt + Q/e.weight  #collect trail(pher amt) left by ant on that particular edge
                        e.prob = self.calulate_prob(e, alpha, beta) #change the prob of that edge after the ant has left trail (pher amt)
           
                for edge in potential_edges:
                    if edge.prob > greatest_prob:
                        greatest_prob = edge.prob
                        edge_to_take = edge
                        vertex_to_go = edge.vertex2

                ants.current_vertex = vertex_to_go
                ants.visted_vertex.append(vertex_to_go)


                edge_to_take.pher_amt = 0.5*edge_to_take.pher_amt + Q/edge_to_take.weight  #collect trail(pher amt) left by ant on that particular edge
                edge_to_take.prob = self.calulate_prob(edge_to_take, alpha, beta) #change the prob of that edge after the ant has left trail (pher amt)

                # Checking if the current tour is shorter than the globally based shortest path
                tour_length = self.calculate_tour_length(ant.visited_vertex)
                if tour_length < shortest_path_length:
                    shortest_path = ant.visited_vertex[:]
                    shortest_path_length = tour_length

        return shortest_path, shortest_path_length







            
                




                









