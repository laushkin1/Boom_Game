import pygame
from random import randint
from settings import *


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, a: int) -> None:
        super().__init__()
        if a == 0:
            arrow_surf = pygame.image.load('data/arrows/arrow.png').convert_alpha()
            self.arrow = pygame.transform.rotozoom(arrow_surf, 90, 0.25)
        elif a == 1:
            arrow2_surf = pygame.image.load('data/arrows/arrow2.png').convert_alpha()
            self.arrow = pygame.transform.rotozoom(arrow2_surf, 90, 0.25)
        elif a == 2:
            arrow3_surf = pygame.image.load('data/arrows/arrow3.png').convert_alpha()
            self.arrow = pygame.transform.rotozoom(arrow3_surf, 90, 0.25)
        else:
            arrow4_surf = pygame.image.load('data/arrows/arrow4.png').convert_alpha()
            self.arrow = pygame.transform.rotozoom(arrow4_surf, 90, 0.25)


        self.image = self.arrow
        self.rect = self.image.get_rect(midbottom = (randint(SCREEN_WIDTH, SCREEN_WIDTH+100), randint(135, SCREEN_HEIGHT-100)))

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

    def update(self):
        self.rect.x -= 6
        self.destroy()



