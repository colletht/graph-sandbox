import bisect

class Graph:
    def __init__(self, isDirected = False):
        self.graph = dict()
        self.availableIds = []
        self.isDirected = isDirected
    
    def __str__(self):
        print(self.edges())
        print(self.degree())
        print(self.degree(1))
        outStr = "{\n"
        for key in self.graph:
            outStr += "  {}: [".format(key)
            for edge in self.graph[key]:
                outStr += " {},".format(edge)
            outStr += "],\n"
        outStr += "}\n"
        return outStr

    def addVertex(self):
        v = self.__getNewVertexId()
        self.graph[v] = []
        return v

    def delVertex(self, vertex):
        if vertex in self.graph:
            del self.graph[vertex]
            for key in self.graph:
                self.graph[key] = list(filter((vertex).__ne__, self.graph[key]))
            bisect.insort(self.availableIds, vertex)
            return True
        return False

    def addEdge(self, start, end):
        if start in self.graph and end in self.graph:
            if self.isDirected:
                #if directed then direction matters so only add to the start edge array
                self.graph[start].append(end)
            else:
                #otherwise we add to both
                self.graph[start].append(end)

                if start != end:
                    self.graph[end].append(start)
            return True
        return False

    def delEdge(self, start, end):
        if start in self.graph and end in self.graph:
            if self.isDirected:
                #if directed only delete this specific order
                self.graph[start].remove(end)
            else:
                #else remove both orders in graph
                print("removing {} from {}".format(end, start))
                self.graph[start].remove(end)
                if end != start:
                    self.graph[end].remove(start)
            return True
        return False

    def vertices(self):
        return list(self.graph.keys())
    
    def count_vertices(self):
        return len(self.vertices())

    def edges(self):
        eDict = dict()
        for key in self.graph:
            for vertex in self.graph[key]:
                if self.isDirected:
                    if (key, vertex) not in eDict:
                        eDict[(key, vertex)] = 1
                    else:
                        eDict[(key, vertex)] += 1
                else:
                    p1 = (key, vertex) in eDict
                    p2 = (vertex, key) in eDict
                    if not p1 and not p2:
                        eDict[(key,vertex)] = 1
                    else:
                        if p1:
                            eDict[(key, vertex)] += 1
        return eDict
    
    def count_edges(self):
        e = self.edges()
        return sum(item[-1] for item in e.items())

    def degree(self, vertex = None):
        if vertex:
            return self.__singleDegree(vertex)
        else:
            return self.__totalDegree()
    
    def __singleDegree(self, vertex):
            #vertex specified, find degree of specific vertex
            if vertex not in self.graph:
                return False

            deg = 0

            for key in self.graph:
                incr = self.graph[key].count(vertex)
                if key == vertex:
                    #account for loops. count twice towards degree
                    incr *= 2
                deg += incr
            
            return deg

    def __totalDegree(self):
            #vertex unspecified return the total degree of the graph
            deg = 0

            for key in self.graph:
                deg += self.__singleDegree(key)
            
            return deg

    def __getNewVertexId(self):
        if len(self.availableIds) > 0:
            return self.availableIds.pop(0)
        else:
            return len(self.graph.keys())