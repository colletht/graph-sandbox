VERTEX_RADIUS = 20
VERTEX_FILL_COLOR = 'white'
CIRCLE_ACTIVE_FILL_COLOR = 'red'

from element import Element
from label import Label
from point import Point
from edge_group import EdgeGroup

class Vertex(Element):
    def __init__(
        self,
        id,
        center,
        degree,
        canvas,
        color = VERTEX_FILL_COLOR
    ):
        Element.__init__(self, id)
        self.center = center
        self.degree = degree
        self.color = color
        self.edgeGroups = []
        self.canvas = canvas
        self.label = Label(id, id, Point(center.x + VERTEX_RADIUS, center.y - VERTEX_RADIUS))

    def __str__(self):
        return "Vertex(id: {}, cid: {}, center: {}, degree: {}, color: {}, edges: {})".format(self.id, self.cid, self.center, self.degree, self.color, self.edgeGroups)

    def addEdge(self, edge):
        for group in self.edgeGroups:
            if group.addEdge(edge):
                return
        
        newGroup = EdgeGroup(0, edge.start, edge.end)
        newGroup.addEdge(edge)

        self.edgeGroups.append(newGroup)

        self.update(self.canvas)

    def delEdge(self, edge):
        for group in self.edgeGroups:
            if group.delEdge(edge):
                print("succesfully deleted edge")
                self.update(self.canvas)
                return True

        return False

    def draw(self, canvas):
        canvas.delete(self.cid)
        self.cid = canvas.create_oval(
            self.center.x - VERTEX_RADIUS,
            self.center.y - VERTEX_RADIUS,
            self.center.x + VERTEX_RADIUS,
            self.center.y + VERTEX_RADIUS,
            fill=self.color,
            activefill=CIRCLE_ACTIVE_FILL_COLOR
        )
        self.label.draw(canvas)

    def update(self, canvas):
        canvas.coords(
            self.cid,
            self.center.x - VERTEX_RADIUS,
            self.center.y - VERTEX_RADIUS,
            self.center.x + VERTEX_RADIUS,
            self.center.y + VERTEX_RADIUS
        )
        self.label.point = Point(self.center.x + VERTEX_RADIUS, self.center.y - VERTEX_RADIUS)
        self.label.update(canvas)
        for group in self.edgeGroups:
            group.update(canvas)
        
    def delete(self, canvas):
        Element.delete(self, canvas)
        self.label.delete(canvas)
        for group in self.edgeGroups:
            group.delete(canvas)