VERTEX_RADIUS = 20
VERTEX_FILL_COLOR = 'white'
CIRCLE_ACTIVE_FILL_COLOR = 'red'

from element import Element
from label import Label
from point import Point

class Vertex(Element):
    def __init__(
        self,
        id,
        center,
        degree,
        color = VERTEX_FILL_COLOR
    ):
        Element.__init__(self, id)
        self.center = center
        self.degree = degree
        self.color = color
        self.edges = []
        self.label = Label(id, id, Point(center.x + VERTEX_RADIUS, center.y - VERTEX_RADIUS))

    def __str__(self):
        return "Vertex(id: {}, cid: {}, center: {}, degree: {}, color: {}, edges: {})".format(self.id, self.cid, self.center, self.degree, self.color, self.edges)

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
        for edge in self.edges:
            edge.update(canvas)
        
    def delete(self, canvas):
        Element.delete(self, canvas)
        self.label.delete(canvas)
        for edge in self.edges:
            edge.delete(canvas)