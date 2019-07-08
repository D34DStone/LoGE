import asyncio
from protocol import creature_pb2
from protocol import change_log_pb2
from protocol import world_pb2

class Engine:

    id_counter = 0
    creatures = dict()
    statics = dict()
    tasks = list()
    change_logs = list()
    config = None

    def __init__(self, config):
        self.config = config

    async def run():
        running = True
        while running:
            for t in tasks:
                t()

            await asyncio.sleep(self.config.ENGINE_ITER_INTERVAL)

    def add_creature(self, creature):
        creature = self.id_counter
        self.id_counter += 1
        self.creatures[creature.id] = creature

        creature_schema = Engine._dump_creature(creature)
        create_log_schema = change_log_pb2.CreateLog()
        create_log_schema.creature = creature_schema
        change_log_schema = change_log_pb2.ChangeLog()
        change_log_schema.create_log = create_log_schema
        self.change_logs.append(change_log_schema)

    def move_creature(self, creature, dx, dy):
        creature.x += dx
        creature.y += dy

        move_log_schmea = change_log_pb2.MoveLog()
        move_log_schmea.creature_id = creature.id
        move_log_schmea.x = creature.x
        move_log_schema.y = creature.y        
        change_log_schema = change_log_pb2.ChangeLog()
        change_log_schema.move_log = move_log_schema
        self.change_logs.append(change_log_schema)

    def _dump_world(self):
        world_schema = world_pb2.World()
        for c in self.creatures:
            world_schema.creatures.add(Engine._dump_creature(c))

        return world_schema

    @staticmethod
    def _dump_creature(creature):
        creature_schema = creature_pb2.Creature()
        creature_schema.id = creature.id
        creature_schema.name = creature.name
        creature_schema.level = creature.level
        creature_schema.x = creature.x
        creature_schema.y = creature.y
        return creature_schema
