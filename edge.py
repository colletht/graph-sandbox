EDGE_THICKNESS = 3
EDGE_FILL_COLOR = 'white'
EDGE_ACTIVE_FILL_COLOR = 'red'

from element import Element
from vertex import VERTEX_RADIUS

ARC_RADIUS = VERTEX_RADIUS

class Edge(Element):
    def __init__(self, id, canvas, startVertex, endVertex = None):
        Element.__init__(self, id)
        self.cid = None
        self.canvas = canvas
        self.start = startVertex
        self.end = endVertex
        self.isLoop = self.end is None or self.end == self.start

        self.offsetStartPoint = None
        self.offsetEndPoint = None

        if self.isLoop and self.end is None:
            self.end = self.start

        #add to edge list of vertex
        self.start.addEdge(self)

        if not self.isLoop:
            self.end.addEdge(self)

    def __str__(self):
        return "Edge(id: {}, cid: {}, start: {}, end: {}, isLoop: {})".format(self.id, self.cid, self.start, self.end, self.isLoop)

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
                self.start.center.x if self.offsetStartPoint is None else self.offsetStartPoint.x,
                self.start.center.y if self.offsetStartPoint is None else self.offsetStartPoint.y,
                self.end.center.x if self.offsetEndPoint is None else self.offsetEndPoint.x,
                self.end.center.y if self.offsetEndPoint is None else self.offsetEndPoint.y,
                fill=EDGE_FILL_COLOR,
                activefill=EDGE_ACTIVE_FILL_COLOR,
                width=EDGE_THICKNESS
            )

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
                self.start.center.x if self.offsetStartPoint is None else self.offsetStartPoint.x,
                self.start.center.y if self.offsetStartPoint is None else self.offsetStartPoint.y,
                self.end.center.x if self.offsetEndPoint is None else self.offsetEndPoint.x,
                self.end.center.y if self.offsetEndPoint is None else self.offsetEndPoint.y
            )

    def initiateDelete(self, vertexInitiated = None):
        if vertexInitiated is self.start:
            self.end.delEdge(self)
        elif vertexInitiated is self.end:
            self.start.delEdge(self)
        else:
            self.start.delEdge(self)
            self.end.delEdge(self)

