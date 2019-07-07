import functools
from engine.engine import Task
from .schemas import WorldSchema


class API:
    """Class that provides access to engine functionality. 

    All communications between client between game and engine should go througth
    this api.
    """

    engine = None

    def __init__(self, engine):
        self.engine = engine

    def get_world_dump(self) -> dict:
        """Returns dict with dump of world corresponds to `engine.api.schemas.WorldSchema`
        """
        return {
            'last_commit_id': self.engine.commit_container.last_commit_id,
            'objects': list(self.engine.objects.values())
        }

    def get_commits(self, start_from=0) -> dict:
        """Returns dict with all commits since commit with id `start_from` corresponds to
        `engine.api.schemas.CommitRangeSchema`.

        TODO: There is a bug so I can't serialize commit_range into dict in some game method. Fix it
        """
        return {
            'commits':
            self.engine.commit_container.get_commit_range(start_from)
        }

    def get_last_commit_id(self) -> int:
        return self.engine.commit_container.get_last_commit_id()

    def get_player_id(self, addr) -> int:
        return self.engine.players[addr].id

    def suspend(f):
        """Decorator to add wrapper function to engine tasks to do it later.
        """
        @functools.wraps(f)
        def wrapper(self, *args, **argv):
            task = Task(lambda: f(self, *args, **argv))
            self.engine.tasks_queue.append(task)

        return wrapper

    @suspend
    def add_object(self, obj) -> None:
        """Debug task which creates object in random coord.
        """
        from random import randint
        from functools import partial
        rng = partial(randint, -12, 12)
        self.engine.add_object(obj, rng(), rng())

    @suspend
    def add_player(self, addr, obj):
         self.engine.players[addr] = obj
         self.add_object(obj)

    @suspend
    def move_object(self, oid, x, y):
        """Change objects coords, move them on vector (x, y).
        """
        obj = self.engine.objects[oid]
        self.engine.move_object(obj, obj.x + x, obj.y + y) 

    @suspend
    def move_object_ip(self, oid, x, y) -> None:
        """Move object to (x, y) coordinats.
        """
        obj = self.engine.objects(oid)
        self.engine.move_object(obj, x, y)
