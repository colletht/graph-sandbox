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
        self.edgeGroups = []
        self.label = Label(id, id, Point(center.x + VERTEX_RADIUS, center.y - VERTEX_RADIUS))
        self.degree = 0
        self.degreeLabel = Label(id, self.degree, Point(center.x - VERTEX_RADIUS, center.y - VERTEX_RADIUS), 'red')

    def __str__(self):
        #return "Vertex(id: {}, cid: {}, center: {}, degree: {}, color: {}, edges: {})".format(self.id, self.cid, self.center, self.degree, self.color, self.edgeCids)
        return str(self.id)

    def setId(self, newId):
        self.id = newId
        self.label.labelText = newId
        
    def setDegree(self, newDegree):
        self.degree = newDegree
        self.degreeLabel.labelText = newDegree

    def addEdge(self, edge):
        for group in self.edgeGroups:
            if group.addEdge(edge):
                return
        
        newGroup = EdgeGroup(0, edge.start, edge.end, self.canvas)
        newGroup.addEdge(edge)

        self.edgeGroups.append(newGroup)

        if edge.isLoop:
            self.setDegree(self.degree+2)
        else:
            self.setDegree(self.degree+1)

        self.update()

    def delEdge(self, edge):
        for group in self.edgeGroups:
            if group.delEdge(edge):
                print("succesfully deleted edge. VertexId: {} Degree: {}".format(self.id, self.degree))
                if edge.isLoop:
                    self.setDegree(self.degree-2)
                else:
                    self.setDegree(self.degree-1)

                print("new degree: {}".format(self.degree))

                self.update()
                return True

        return False

    def delGroup(self, group):
        for g in self.edgeGroups:
            if (g.start is group.start and g.end is group.end) or (g.start is group.end and g.end is group.start) and len(g.edges) == 0:
                self.edgeGroups.remove(g)

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
        self.degreeLabel.draw(self.canvas)
        for group in self.edgeGroups:
            group.draw()

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
        self.degreeLabel.point = Point(self.center.x - VERTEX_RADIUS, self.center.y - VERTEX_RADIUS)
        self.degreeLabel.update(self.canvas)
        for group in self.edgeGroups:
            group.update()
        
    def delete(self):
        Element.delete(self, self.canvas)
        self.label.delete(self.canvas)
        self.degreeLabel.delete(self.canvas)
        for group in self.edgeGroups:
            group.delete(self)