EDGE_THICKNESS = 3
EDGE_FILL_COLOR = 'white'
EDGE_ACTIVE_FILL_COLOR = 'red'

from element import Element
from vertex import VERTEX_RADIUS
from arrowhead import ArrowHead
from point import Point

ARC_RADIUS = VERTEX_RADIUS

class Edge(Element):
    def __init__(self, id, canvas, startVertex, endVertex = None, directed = False):
        Element.__init__(self, id)
        self.cid = None
        self.canvas = canvas
        self.start = startVertex
        self.end = endVertex
        self.isLoop = self.end is None or self.end == self.start
        self.directed = directed
        self.arrowhead = ArrowHead(self.canvas, self.start, self.end)

        self.offsetStartPoint = Point(0,0)
        self.offsetEndPoint = Point(0,0)

        if self.isLoop and self.end is None:
            self.end = self.start

        #add to edge list of vertex
        self.start.addEdge(self)

        if not self.isLoop:
            self.end.addEdge(self)

    def __str__(self):
        return "Edge(id: {}, cid: {}, start: {}, end: {}, isLoop: {})".format(self.id, self.cid, self.start, self.end, self.isLoop)

    def setDirected(self, directed):
        self.directed = directed
        if self.directed:
            self.arrowhead.update()
        else:
            self.arrowhead.delete()

    def setOffset(self, offset_start, offset_end):
        self.offsetStartPoint = offset_start
        self.offsetEndPoint = offset_end

        self.arrowhead.offset_point = offset_end

    def draw(self):
        self.canvas.delete(self.cid)
        if self.isLoop:
            self.cid = self.canvas.create_arc(
                self.start.center.x - ARC_RADIUS*3,
                self.start.center.y - ARC_RADIUS*3,
                self.start.center.x,
                self.start.center.y,
                start=0,
                extent=270,
                style='arc',
                outline=EDGE_FILL_COLOR,
                activeoutline=EDGE_ACTIVE_FILL_COLOR,
                width=EDGE_THICKNESS
            )
        else:
            self.cid = self.canvas.create_line(
                self.start.center.x + self.offsetStartPoint.x,
                self.start.center.y + self.offsetStartPoint.y,
                self.end.center.x + self.offsetEndPoint.x,
                self.end.center.y + self.offsetEndPoint.y,
                fill=EDGE_FILL_COLOR,
                activefill=EDGE_ACTIVE_FILL_COLOR,
                width=EDGE_THICKNESS
            )
        if self.directed:
            self.arrowhead.draw()
            

    def update(self):
        if self.isLoop:
            self.canvas.coords(
                self.cid,
                self.start.center.x - ARC_RADIUS*3,
                self.start.center.y - ARC_RADIUS*3,
                self.end.center.x,
                self.end.center.y
            )
        else:
            self.canvas.coords(
                self.cid,
                self.start.center.x + self.offsetStartPoint.x,
                self.start.center.y + self.offsetStartPoint.y,
                self.end.center.x + self.offsetEndPoint.x,
                self.end.center.y + self.offsetEndPoint.y
            )
        if self.directed:
            self.arrowhead.update()

    def delete(self):
        self.arrowhead.delete()
        Element.delete(self, self.canvas)

    def initiateDelete(self, vertexInitiated = None):
        self.arrowhead.delete()
        if vertexInitiated is self.start:
            self.end.delEdge(self)
        elif vertexInitiated is self.end:
            self.start.delEdge(self)
        else:
            self.start.delEdge(self)
            self.end.delEdge(self)

