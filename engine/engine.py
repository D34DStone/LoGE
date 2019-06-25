import functools
from .object import *

class Cell(object):
    pass


class Task(object):
    
    foo = lambda:None 

    def __init__(self, foo):
        self.foo = foo

    def run(self):
        self.foo()


class Engine(object):

    objects = dict()
    objects_counter = 0
    tasks_queue = list()
    ais = dict()
    field = list()

    def __init__(self, width=512, height=512):
        self.width = width
        self.height = height
        for _ in range(width):
            self.field.append([Cell() for _ in range(height)])

    def get_cell(self, x, y):
        if x < -self.width / 2 or x > self.width / 2 or y < -self.height / 2 or y > self.height / 2:
            raise ValueError("Coords value out of field range")

        return self.field[x + self.width / 2][y + self.height / 2]

    def add_object(self, obj, x, y):
        cell = self.get_cell(x, y)
        cell.object = obj
        obj.x, obj.y = x, y
        obj.id = self.objects_counter
        self.objects_counter += 1
        self.objects[obj.id] = obj
        print("Object was created!")
    
    def suspend(f):
        @functools.wraps(f)
        def wrapper():
            engine.tasks_queue.append(Task(f))

        return wrapper

    @suspend 
    def create_player(self, uid):
        p = Player(uid)
        self.add_object(p, 0, 0)

    def iterate_world(self):
        print("WORLD ITERATED!")
        for t in self.tasks_queue:
            t.run()

        self.tasks_queue = []
    
