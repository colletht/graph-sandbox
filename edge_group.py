from element import Element
from point import Point
from edge import Edge

EDGE_OFFSET = 10

class EdgeGroup(Element):
    '''
    Class for orginizing and displaying parallel edges
    edges contained in the groups list will all have the
    same start and end vertexes as the group. The group will
    then dictate how the edges are displayed and edited along
    with deleted
    '''
    def __init__(self, id, startVertex, endVertex, canvas):
        Element.__init__(self, id)

        self.start = startVertex
        self.end = endVertex
        self.canvas = canvas
        self.orthUnitVect = None
        self.isLoop = self.start is self.end
        self.edges = []

        self.updateOrthogonalLines()

    def edge_cids(self):
        return list(filter(lambda x: x is not None, [e.cid for e in self.edges]))

    def updateOrthogonalLines(self):
        if self.isLoop:
            return

        self.orthUnitVect = Point(
            self.end.center.y - self.start.center.y,
            self.start.center.x - self.end.center.x
        ).getUnitVector()

    def edgeBelongsInGroup(self, edge):
        return (edge.start is self.start and edge.end is self.end) or (edge.start is self.end and edge.end is self.start)

    def redistributeEdges(self):
        if self.isLoop or len(self.edges) <= 1:
            return

        self.updateOrthogonalLines()
        edge_count = len(self.edges)

        offset_start = -(edge_count*EDGE_OFFSET)/2

        for i in range(0, edge_count):
            tmp_edge = self.edges[i]
            tmp_edge.setOffset(
                self.orthUnitVect.scalar(offset_start),
                self.orthUnitVect.scalar(offset_start)
            )

            offset_start += EDGE_OFFSET


    def addEdge(self, edge):
        if not self.edgeBelongsInGroup(edge):
            return False
        
        self.edges.append(edge)

        self.redistributeEdges()
        return True

    def delEdge(self, edge):
        for e in self.edges:
            if e.cid == edge.cid:
                self.edges.remove(e)
                e.delete()
                return True
        return False

    def draw(self):
        for edge in self.edges:
            if edge.cid is None:
                edge.draw()
            else:
                edge.update()
        
    def update(self):
        self.redistributeEdges()

        for edge in self.edges:
            if edge.cid is None:
                edge.draw()
            else:
                edge.update()

    def delete(self, vertexInitiated):
        Element.delete(self, self.canvas)
        for edge in self.edges:
            edge.arrowhead.delete()
            edge.delete()
            if vertexInitiated is edge.start:
                edge.end.delEdge(edge)
            else:
                edge.start.delEdge(edge)
        
        if vertexInitiated is self.start:
            edge.end.delGroup(self)
        else:
            edge.start.delGroup(self)

    