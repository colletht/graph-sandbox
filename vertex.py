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
        canvas,
        color = VERTEX_FILL_COLOR
    ):
        Element.__init__(self, id)
        self.center = center
        self.color = color
        self.canvas = canvas
        self.degree = 0
        self.edgeCids = []
        self.label = Label(id, id, Point(center.x + VERTEX_RADIUS, center.y - VERTEX_RADIUS))

    def __str__(self):
        #return "Vertex(id: {}, cid: {}, center: {}, degree: {}, color: {}, edges: {})".format(self.id, self.cid, self.center, self.degree, self.color, self.edgeCids)
        return str(self.id)

    def setId(self, newId):
        self.id = newId
        self.label.labelText = newId

    def draw(self):
        self.canvas.delete(self.cid)
        self.cid = self.canvas.create_oval(
            self.center.x - VERTEX_RADIUS,
            self.center.y - VERTEX_RADIUS,
            self.center.x + VERTEX_RADIUS,
            self.center.y + VERTEX_RADIUS,
            fill=self.color,
            activefill=CIRCLE_ACTIVE_FILL_COLOR
        )
        self.label.draw(self.canvas)

    def update(self):
        self.canvas.coords(
            self.cid,
            self.center.x - VERTEX_RADIUS,
            self.center.y - VERTEX_RADIUS,
            self.center.x + VERTEX_RADIUS,
            self.center.y + VERTEX_RADIUS
        )
        self.label.point = Point(self.center.x + VERTEX_RADIUS, self.center.y - VERTEX_RADIUS)
        self.label.update(self.canvas)
        
    def delete(self):
        Element.delete(self, self.canvas)
        self.label.delete(self.canvas)