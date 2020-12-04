
class Element:
    def __init__(self, id):
        self.cid = None
        self.id = id

    def __str__(self):
        return "Element(id: {}, cid: {})".format(self.id, self.cid)

    def delete(self, canvas):
        canvas.delete(self.cid)