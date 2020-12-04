EDGE_THICKNESS = 3
EDGE_FILL_COLOR = 'white'
EDGE_ACTIVE_FILL_COLOR = 'red'

from element import Element
from vertex import VERTEX_RADIUS

ARC_RADIUS = VERTEX_RADIUS

class Edge(Element):
    def __init__(self, id, startVertex, endVertex = None):
        Element.__init__(self, id)
        self.start = startVertex
        self.end = endVertex
        self.isLoop = self.end is None or self.end == self.start

        if self.isLoop and self.end is None:
            self.end = self.start

        #add to edge list of vertex
        self.start.edges.append(self)
        self.end.edges.append(self)

    def __str__(self):
        return "Edge(id: {}, cid: {}, start: {}, end: {}, isLoop: {})".format(self.id, self.cid, self.start, self.end, self.isLoop)

    def draw(self, canvas):
        canvas.delete(self.cid)
        if self.isLoop:
            self.cid = canvas.create_arc(
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
            self.cid = canvas.create_line(
                self.start.center.x,
                self.start.center.y,
                self.end.center.x,
                self.end.center.y,
                fill=EDGE_FILL_COLOR,
                activefill=EDGE_ACTIVE_FILL_COLOR,
                width=EDGE_THICKNESS
            )

    def update(self, canvas):
        if self.isLoop:
            canvas.coords(
                self.cid,
                self.start.center.x - ARC_RADIUS*3,
                self.start.center.y - ARC_RADIUS*3,
                self.end.center.x,
                self.end.center.y
            )
        else:
            canvas.coords(
                self.cid,
                self.start.center.x,
                self.start.center.y,
                self.end.center.x,
                self.end.center.y
            )