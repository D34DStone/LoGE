class Cell(object):
    obj = None 
    coords = (None, None)


class World(object):

    width = None
    height = None
    field = None

    def __init__(self, width=512, height=512):
        self.field = list()
        for i in range(height):
            self.field.append([] for i in range(width))


    def add_object(self, obj, pos):
        pass


