
from element import Element
from point import Point
from edge import EDGE_ACTIVE_FILL_COLOR, EDGE_FILL_COLOR, EDGE_THICKNESS
from vertex import VERTEX_RADIUS

ARROWHEAD_FILL_COLOR = EDGE_FILL_COLOR
ARROWHEAD_ACTIVE_FILL_COLOR = EDGE_ACTIVE_FILL_COLOR
ARROWHEAD_LENGTH = EDGE_THICKNESS*3

class ArrowHead(Element):
    def __init__(self, canvas, start, end, offset_point = Point(0,0)):
        Element.__init__(self, 0)
        self.canvas = canvas
        self.start = start
        self.end = end
        self.offset_point = offset_point
        self.unit_vector = self.__unit_vector()
        self.points = self.__points()

    def __isloop(self):
        return self.start is self.end

    def __unit_vector(self):
        if self.__isloop():
            return Point(1, 0)
        else:
            return (self.end.center - self.start.center).getUnitVector()

    def __points(self):
        point_list = []

        #tip of arrow
        if self.__isloop():
            tip = self.end.center + Point(-VERTEX_RADIUS, 0)
        else:
            #need to reduce magnitude slightly so tip is on edge of vertex not center
            tip = self.end.center - self.unit_vector.scalar(VERTEX_RADIUS) + self.offset_point

        #back center
        back_center = tip - self.unit_vector.scalar(ARROWHEAD_LENGTH)
        
        #right corner
        right_corner = back_center + self.unit_vector.rotate(135).scalar(ARROWHEAD_LENGTH)

        #left corner
        left_corner = back_center + self.unit_vector.rotate(-135).scalar(ARROWHEAD_LENGTH)

        point_list.append(back_center.x)
        point_list.append(back_center.y)
        point_list.append(left_corner.x)
        point_list.append(left_corner.y)
        point_list.append(tip.x)
        point_list.append(tip.y)
        point_list.append(right_corner.x)
        point_list.append(right_corner.y)

        return point_list

    def draw(self):
        self.canvas.delete(self.cid)
        self.cid = self.canvas.create_polygon(
            self.points,
            fill=ARROWHEAD_FILL_COLOR,
            activefill=ARROWHEAD_ACTIVE_FILL_COLOR
        )


    def update(self):
        self.unit_vector = self.__unit_vector()
        self.points = self.__points()
        if (self.cid == None):
            self.draw()
            return
        self.canvas.coords(
            self.cid,
            self.points
        )


    def delete(self):
        Element.delete(self, self.canvas)
        self.cid = None