#!PYTHON

#TODO: Create individual event bindings for each object so as to greatly reduce complexity
#TODO: Fix label inconsistencies upon deletion

BACKGROUND_COLOR = 'black'

from tkinter import *
from point import Point
from vertex import Vertex
from edge import Edge
from graph import Graph

class GraphSandbox:
    def __init__(self, root, canvas, text):
        self.root = root
        self.canvas = canvas
        self.text = text
        self.graph = Graph()
        self.vertices = []
        self.edges = []

        #status variables
        self.startVertex = None
        self.vertexToMove = None

        root.title('Graph Sandbox') #adds title to the window

        self.updateAnalytics()
        self.text.pack(fill=X)

        self.canvas.bind('<Button-1>', self.handleLeftClick) #Handle left click
        self.canvas.bind('<Button-2>', None) #Handle center click
        self.canvas.bind('<Button-3>', self.handleRightClick) #Handle right click
        self.canvas.bind('<B1-Motion>', self.handleLeftClickDrag)
        self.canvas.bind('<ButtonRelease-1>', self.handleLeftClickRelease)
        self.canvas.pack(fill=BOTH, expand=1)

    def SearchElementsByCid(self, cid):
        for vertex in self.vertices:
            if vertex.cid == cid:
                return vertex

        for edge in self.edges:
            if edge.cid == cid:
                return edge

        return None

    def DeleteElement(self, cid):
        for vertex in self.vertices:
            if vertex.cid == cid:
                self.graph.delVertex(vertex.id)
                self.vertices.remove(vertex)
                vertex.delete()

        for edge in self.edges:
            if edge.cid == cid:
                self.graph.delEdge(edge.start.id, edge.end.id)
                edge.initiateDelete()
                self.edges.remove(edge) 

    def handleLeftClick(self, event):
        '''
        Handles a left click on the canvas. Does some decision making in terms of what to do
        on a left click. If the left click is on an empty spot, it will create a new circle
        if it is on an existing circle it will enter line drawing mode and will draw a line
        starting at the given circle and ending at whatever vertex is drawn next.
        '''
        if self.vertexToMove:
            return

        overlapping = canvas.find_overlapping(event.x, event.y, event.x, event.y)

        if overlapping and not self.startVertex:
            #no start point yet, make this the start point
            self.startVertex = self.SearchElementsByCid(overlapping[0])

            if type(self.startVertex) is not Vertex:
                self.startVertex = None

        elif overlapping and self.startVertex:
            #starting point is already there make this the endpoint
            self.endVertex = self.SearchElementsByCid(overlapping[0])
            
            if type(self.endVertex) is not Vertex:
                self.endVertex = None
                return #must be a vertex to connect an edge

            self.addEdge(event)

        elif not overlapping:
            self.addVertex(event)

        print(self.graph)
                
        self.updateAnalytics()

    def handleRightClick(self, event):
        overlapping = canvas.find_overlapping(event.x, event.y, event.x, event.y)

        if overlapping:
            for cid in overlapping:
                self.DeleteElement(cid)
        print(self.graph)
                
        self.updateAnalytics()

    def handleLeftClickDrag(self, event):
        #if we are already moving then dont search for the vertex again
        if self.vertexToMove:
            self.vertexToMove.center = Point(event.x, event.y)
            self.vertexToMove.update()
        else:
            overlapping = canvas.find_overlapping(event.x, event.y, event.x, event.y)
            print(str(overlapping))

            if overlapping:
                self.vertexToMove = self.SearchElementsByCid(overlapping[0])
                
                if type(self.vertexToMove) is not Vertex:
                    return
                
                self.vertexToMove.center = Point(event.x, event.y)
                self.vertexToMove.update()

        self.updateAnalytics()

    def handleLeftClickRelease(self, event):
        if self.vertexToMove:
            #mitigate accidental line creation
            self.startVertex = None
            self.vertexToMove = None

    def addVertex(self, event):
        vId = self.graph.addVertex()

        newVertex = Vertex(
            vId,
            Point(event.x, event.y),
            self.canvas
        )

        self.vertices.append(newVertex)
        newVertex.draw()
    
    def addEdge(self, event):
        self.graph.addEdge(self.startVertex.id, self.endVertex.id)
        newEdge = Edge(
            -1,
            canvas,
            self.startVertex,
            self.endVertex
        )

        self.edges.append(newEdge)

        newEdge.draw()

        #reset start vertex for next run
        self.startVertex = None
        self.endVertex = None

    def updateAnalytics(self):
        readings = dict()
        readings['count_v'] = self.graph.count_vertices()
        readings['count_e'] = self.graph.count_edges()

        self.text.delete('1.0',END)
        self.text.insert(INSERT, "vertices: {}, edges: {}".format(readings['count_v'], readings['count_e']))

root = Tk()
text = Text(root, height=1, bg=BACKGROUND_COLOR, fg='red')
canvas = Canvas(root, background=BACKGROUND_COLOR)
GraphSandbox(root, canvas, text)
root.mainloop() #to keep the window up