import pygame
from support import import_folder


class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self):
        self.frames = {
            # magic
            "flame": import_folder("../images/graphics/particles/flame/frames"),
            "aura": import_folder("../images/graphics/particles/aura"),
            "heal": import_folder("../images/graphics/particles/heal/frames"),
            # attacks
            "claw": import_folder("../images/graphics/particles/claw"),
            "slash": import_folder("../images/graphics/particles/slash"),
            "sparkle": import_folder("../images/graphics/particles/sparkle"),
            "leaf_attack": import_folder("../images/graphics/particles/leaf_attack"),
            "thunder": import_folder("../images/graphics/particles/thunder"),
            # monster deaths
            "squid": import_folder("../images/graphics/particles/smoke_orange"),
            "raccoon": import_folder("../images/graphics/particles/raccoon"),
            "spirit": import_folder("../images/graphics/particles/nova"),
            "bamboo": import_folder("../images/graphics/particles/bamboo"),
            # leafs
            "leaf": (
                import_folder("../images/graphics/particles/leaf2"),
                import_folder("../images/graphics/particles/leaf1"),
                import_folder("../images/graphics/particles/leaf3"),
                import_folder("../images/graphics/particles/leaf4"),
                import_folder("../images/graphics/particles/leaf5"),
                import_folder("../images/graphics/particles/leaf6"),
                self.reflect_images(import_folder("../images/graphics/particles/leaf1")),
                self.reflect_images(import_folder("../images/graphics/particles/leaf2")),
                self.reflect_images(import_folder("../images/graphics/particles/leaf3")),
                self.reflect_images(import_folder("../images/graphics/particles/leaf4")),
                self.reflect_images(import_folder("../images/graphics/particles/leaf5")),
                self.reflect_images(import_folder("../images/graphics/particles/leaf6")),
            ),
        }

    def reflect_images(self):

    def __init__(self, pos, animation_frames, groups):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.image.get_rect[self.frame_index]

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self):
        self.animate()
