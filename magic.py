import pygame
from settings import *
from random import randint

class PlayerMagic:
    def __init__(self,animation_player):
        self.animation_player = animation_player
        self.magic_sound_heal = pygame.mixer.Sound(magic_data["heal"]["sound"])
        self.magic_sound_fire = pygame.mixer.Sound(magic_data["flame"]["sound"])

    def heal(self, player, strength, cost, groups):
        if player.energy >= cost:
            player.health += strength
            player.energy -= cost
            if player.health >= player.stats["health"]:
                player.health = player.stats["health"]
            self.animation_player.create_particles('aura',player.rect.center,groups)
            self.animation_player.create_particles('heal',player.rect.center,groups)
            self.magic_sound_heal.play()

    def flame(self,player,cost,groups):
        if player.energy >= cost:
            player.energy -= cost

            if player.status.split('_')[0] == 'right':
                direction = pygame.math.Vector2(1,0)
            elif player.status.split('_')[0] == 'left':
                direction = pygame.math.Vector2(-1,0)
            elif player.status.split('_')[0] == 'down':
                direction = pygame.math.Vector2(0,1)
            else:
                direction = pygame.math.Vector2(0,-1)

            # self.sounds['fire'].play()
            self.magic_sound_fire.play()

            for i in range(1,6):
                if direction.x: # Horizontal
                    offset_x = (direction.x * i) * TILESIZE
                    x = player.rect.centerx + offset_x + randint(-TILESIZE // 3, TILESIZE // 3)
                    y = player.rect.centery + randint(-TILESIZE // 3, TILESIZE // 3)
                    self.animation_player.create_particles('flame',(x,y),groups)
                else: # Vertical
                    offset_y = (direction.y * i) * TILESIZE
                    x = player.rect.centerx + randint(-TILESIZE // 3, TILESIZE // 3)
                    y = player.rect.centery + offset_y + randint(-TILESIZE // 3, TILESIZE // 3)
                    self.animation_player.create_particles('flame',(x,y),groups)