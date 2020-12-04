#!PYTHON

#TODO: Create individual event bindings for each object so as to greatly reduce complexity
#TODO: Fix label inconsistencies upon deletion

BACKGROUND_COLOR = 'black'

from tkinter import *
from point import Point
from vertex import Vertex
from edge import Edge

class GraphSandbox:
    def __init__(self, root, canvas):
        self.root = root
        self.canvas = canvas
        self.vertices = []
        self.edges = []

        #status variables
        self.startVertex = None
        self.vertexToMove = None

        root.title('Graph Sandbox') #adds title to the window

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

    def AddElement(self, element):
        if type(element) is Vertex:
            newId = 0 if len(self.vertices) == 0 else self.vertices[-1].id + 1
            element.id = newId
            element.label.labelText = newId
            self.vertices.append(element)

        elif type(element) is Edge:
            newId = 0 if len(self.edges) == 0 else self.edges[-1].id + 1
            element.id = newId
            self.edges.append(element)

    def DeleteElement(self, cid):
        for vertex in self.vertices:
            if vertex.cid == cid:
                self.vertices.remove(vertex)
                vertex.delete(self.canvas)
                self.FixVertexIds()

        for edge in self.edges:
            if edge.cid == cid:
                self.edges.remove(edge)
                edge.delete(self.canvas)

    def FixVertexIds(self):
        i = 0
        for vertex in self.vertices:
            vertex.id = i
            vertex.label.labelText = i
            vertex.update(self.canvas)
            i+=1
        

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
            endVertex = self.SearchElementsByCid(overlapping[0])
            
            if type(endVertex) is not Vertex:
                return #must be a vertex to connect an edge

            newEdge = Edge(
                -1,
                self.startVertex,
                endVertex
            )

            self.AddElement(newEdge)

            newEdge.draw(self.canvas)
            
            #reset start vertex for next run
            self.startVertex = None
        elif not overlapping:
            newVertex = Vertex(
                -1,
                Point(event.x, event.y),
                0
            )

            self.AddElement(newVertex)

            newVertex.draw(self.canvas)

    def handleRightClick(self, event):
        overlapping = canvas.find_overlapping(event.x, event.y, event.x, event.y)

        if overlapping:
            for cid in overlapping:
                self.DeleteElement(cid)

    def handleLeftClickDrag(self, event):
        #if we are already moving then dont search for the vertex again
        if self.vertexToMove:
            self.vertexToMove.center = Point(event.x, event.y)
            self.vertexToMove.update(canvas)
        else:
            overlapping = canvas.find_overlapping(event.x, event.y, event.x, event.y)
            print(str(overlapping))

            if overlapping:
                self.vertexToMove = self.SearchElementsByCid(overlapping[0])
                
                if type(self.vertexToMove) is not Vertex:
                    return
                
                self.vertexToMove.center = Point(event.x, event.y)
                self.vertexToMove.update(canvas)

    def handleLeftClickRelease(self, event):
        if self.vertexToMove:
            #mitigate accidental line creation
            self.startVertex = None
            self.vertexToMove = None

root = Tk()
canvas = Canvas(root, background=BACKGROUND_COLOR)
GraphSandbox(root, canvas)
root.mainloop() #to keep the window up