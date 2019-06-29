import sys
import pygame
import asyncio
pygame.init()

class Creature(object):

    rect = None
    color = None

    def __init__(self, x, y, width=50, height=50, color=(255, 255, 255)):
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)

    def move(self, v):
        self.rect = self.rect.move(v)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)


class Game(object):

    config = None 
    client = None
    screen_size = None 
    screen = None

    def __init__(self, config, client):
        self.config = config
        self.client = client
        self.screen_size = (config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
        self.screen = pygame.display.set_mode(self.screen_size)

    def draw_object(self, screen, obj):
        rect = pygame.Rect((obj["x"] + 12) * 20, (obj["y"] + 12) * 20, 20, 20)
        color = 255, 255, 255
        pygame.draw.rect(screen, color, rect)

    async def run(self):

        player = Creature(100, 100)

        while 1:
            await asyncio.sleep(self.config.REDRAW_INTERVAL_S)

            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
   
                if event.type == pygame.KEYDOWN:
                    move_map = {
                                'w' : (0, -1),
                                'a' : (-1, 0),
                                's' : (0, 1),
                                'd' : (1, 0)
                            }
                    try: 
                        v = move_map[chr(event.key)]
                    except:
                        pass
                    else:
                        await self.client.handle_move(v)

            if not self.client.game_running:
                continue

            objects = self.client.get_objects()

            self.screen.fill(self.config.BACKGROUND_COLOR)
            for obj in objects:
                self.draw_object(self.screen, obj)

            pygame.display.flip()
            
