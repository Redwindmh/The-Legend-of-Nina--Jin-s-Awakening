import pygame
from settings import *
from entity import Entity


class Enemy(Entity):
    def __init__(self, enemy_name, pos, groups):

        # General setup
        super().__init__(groups)
        self.sprite_type = "enemy"

        # Graphics setup
        self.import_graphics(enemy_name)
        self.image = pygame.Surface((64, 64))
        self.rect = self.image.get_rect(topleft=pos)

    def import_graphics(self, name):
        self.animations = {"idle": [], "move": [], "attack": []}
