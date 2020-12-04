from element import Element

class Label(Element):
    def __init__(
        self,
        id,
        labelText,
        point
    ):
        Element.__init__(self, id)
        self.cid = None
        self.labelText = labelText
        self.color = 'green'
        self.point = point

    def draw(self, canvas):
        canvas.delete(self.cid)
        self.cid = canvas.create_text(
            self.point.x,
            self.point.y,
            text=self.labelText,
            fill=self.color
        )

    def update(self, canvas):
        canvas.itemconfigure(
            self.cid,
            text=self.labelText
        )
        canvas.coords(
            self.cid,
            self.point.x,
            self.point.y
        )



