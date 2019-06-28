import functools
from engine.engine import Task
from .schemas import WorldSchema


class API:

    engine = None

    def __init__(self, engine):
        self.engine = engine

    def get_world_dump(self):
        return {
            'last_commit_id': self.engine.commit_container.last_commit_id,
            'objects': list(self.engine.objects.values())
        }

    def get_commits(self, start_from=0):
        return {
            'commits':
            self.engine.commit_container.get_commit_range(start_from)
        }

    def get_last_commit_id(self):
        return self.engine.commit_container.get_last_commit_id()

    def suspend(f):
        @functools.wraps(f)
        def wrapper(self, *args, **argv):
            task = Task(lambda: f(self, *args, **argv))
            self.engine.tasks_queue.append(task)

        return wrapper

    @suspend
    def add_object(self, obj):
        self.engine.add_object(obj, 11, 12)
