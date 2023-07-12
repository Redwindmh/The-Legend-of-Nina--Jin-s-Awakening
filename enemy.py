import pygame
from settings import *
from entity import Entity
from support import *


class Enemy(Entity):
    def __init__(self, enemy_name, pos, groups, obstacle_sprites, damage_player, trigger_death_particles, add_exp):

        # General setup
        super().__init__(groups)
        self.sprite_type = "enemy"

        # Graphics setup
        self.import_graphics(enemy_name)
        self.status = "idle"
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.mask = pygame.mask.from_surface(self.image)

        # Movement
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)
        self.obstacle_sprites = obstacle_sprites

        # Stats
        self.enemy_name = enemy_name
        enemy_info = enemy_data[self.enemy_name]
        self.health = enemy_info["health"]
        self.exp = enemy_info["exp"]
        self.speed = enemy_info["speed"]
        self.attack_damage = enemy_info["damage"]
        self.resistance = enemy_info["resistance"]
        self.attack_radius = enemy_info["attack_radius"]
        self.notice_radius = enemy_info["notice_radius"]
        self.attack_type = enemy_info["attack_type"]

        # Interaction with player
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 1500 / self.speed
        self.damage_player = damage_player
        self.trigger_death_particles = trigger_death_particles
        self.add_exp = add_exp

        # Hit timer
        self.vulnerable = True
        self.hit_time = None
        self.invincibility_duration = 300

        # Sound setup
        self.attack_sound = pygame.mixer.Sound(enemy_info["attack_sound"])
        self.damage_sound = pygame.mixer.Sound("./audio/hit.wav")
        self.death_sound = pygame.mixer.Sound("./audio/death.wav")
        self.damage_sound.set_volume(0.2)
        self.death_sound.set_volume(0.2)
        self.attack_sound.set_volume(0.3)

    def import_graphics(self, name):
        self.animations = {"idle": [], "move": [], "attack": []}
        main_path = f"./images/graphics/monsters/{name}/"
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)

    def get_player_distance_direction(self, player):
        enemy_vector = pygame.math.Vector2(self.rect.center)
        player_vector = pygame.math.Vector2(player.rect.center)
        distance = (player_vector - enemy_vector).magnitude()

        if distance > 0:
            direction = (player_vector - enemy_vector).normalize()
        else:
            direction = pygame.math.Vector2()

        return (distance, direction)

    def get_status(self, player):
        distance = self.get_player_distance_direction(player)[0]

        if distance <= self.attack_radius and self.can_attack:
            if self.status != "attack":
                self.frame_index = 0
            self.status = "attack"
        elif distance <= self.notice_radius:
            self.status = "move"
        else:
            self.status = "idle"

    def actions(self, player):
        if self.status == "attack":
            self.attack_time = pygame.time.get_ticks()
            self.damage_player(self.attack_damage,self.attack_type)
        elif self.status == "move":
            self.direction = self.get_player_distance_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()

    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == "attack":
                self.attack_sound.play()
                self.can_attack = False
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        # Flicker on damage
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
            # self.image.fill("red")
        else:
            self.image.set_alpha(255)

    def hit_cooldown(self):
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True

        if not self.vulnerable:
            if current_time - self.hit_time >= self.invincibility_duration:
                self.vulnerable = True

    def get_damage(self, player, attack_type):
        if self.vulnerable:
            self.direction = self.get_player_distance_direction(player)[1]
            # Weapon damage
            if attack_type == "weapon":
                self.health -= player.get_full_weapon_damage()
                self.damage_sound.play()
            else:
                # Magic damage
                self.health -= player.get_full_magic_damage()
                self.damage_sound.play()
            self.hit_time = pygame.time.get_ticks()
            self.vulnerable = False

    def check_death(self):
        if self.health <= 0:
            self.trigger_death_particles(self.rect.center,self.enemy_name)
            self.kill()
            self.death_sound.play()
            self.add_exp(self.exp)

    def hit_reaction(self):
        if not self.vulnerable:
            self.direction *= -self.resistance

    def update(self):
        self.hit_reaction()
        self.move(self.speed)
        self.animate()
        self.hit_cooldown()

    def enemy_update(self, player):
        self.get_status(player)
        self.actions(player)
        self.check_death()
