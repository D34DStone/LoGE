import functools
from .object import *
from .changes import *
from .commit_container import CommitContainer


class Task(object):
    """Suspended function.
    """
    foo = None

    def __init__(self, foo):
        self.foo = foo

    def run(self):
        self.foo()


class Engine(object):

    objects_counter = 0
    objects = dict()  # dict where key is object id and value is obj
    players = dict()  # dict where key is user addr and value is it's player obj
    ais = dict()
    tasks_queue = list()

    def __init__(self):
        self.commit_container = CommitContainer()

    def add_object(self, obj, x, y):
        obj.x, obj.y = x, y
        obj.id = self.objects_counter
        self.objects_counter += 1
        self.objects[obj.id] = obj
        self.commit_container.append_change(CreateChange(object=obj))

    def move_object(self, obj, x, y):
        obj.x, obj.y = x, y
        change = MoveChange(obj.id, x, y)
        self.commit_container.append_change(change)

    def iterate_world(self):
        print(f"Iteration: task queue size: {len(self.tasks_queue)}")
        for t in self.tasks_queue:
            t.run()

        self.tasks_queue = []
        self.commit_container.push()
