import pygame
from random import randint
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        player_walk_1 = pygame.image.load('data/playersamgs/amg.png').convert_alpha()
        player_walk_1 = pygame.transform.rotozoom(player_walk_1, 0, 0.3)
        player_walk_2 = pygame.image.load('data/playersamgs/amg2.png').convert_alpha()
        player_walk_2 = pygame.transform.rotozoom(player_walk_2, 0, 0.3)

        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0

        self.player_stay = pygame.image.load('data/playersamgs/amg_stay_01.png')
        self.player_stay = pygame.transform.scale_by(self.player_stay, 0.3)

        self.player_jump = pygame.image.load('data/playersamgs/amg_jump.png').convert_alpha()
        self.player_jump = pygame.transform.rotozoom(self.player_jump, 0, 0.3)

        self.image = self.player_stay
        self.rect = self.image.get_rect(midbottom = (200, SCREEN_HEIGHT - 50))
        self.gravity = 0
        self.is_right = True

        self.jump_sound1 = pygame.mixer.Sound('data/music/JumpC_Sounds/jump_c_01.wav')
        self.jump_sound2 = pygame.mixer.Sound('data/music/JumpC_Sounds/jump_c_02.wav')
        self.jump_sound3 = pygame.mixer.Sound('data/music/JumpC_Sounds/jump_c_03.wav')
        self.jump_sound4 = pygame.mixer.Sound('data/music/JumpC_Sounds/jump_c_04.wav')
        self.jump_sound5 = pygame.mixer.Sound('data/music/JumpC_Sounds/jump_c_05.wav')
        self.jump_sound6 = pygame.mixer.Sound('data/music/JumpC_Sounds/jump_c_06.wav')
        self.jump_sound7 = pygame.mixer.Sound('data/music/JumpC_Sounds/jump_c_07.wav')
        self.jump_sound8 = pygame.mixer.Sound('data/music/JumpC_Sounds/jump_c_08.wav')
        self.jump_sound9 = pygame.mixer.Sound('data/music/JumpC_Sounds/jump_c_09.wav')

        self.jump_sound_list = [self.jump_sound1, self.jump_sound2, self.jump_sound3,
                                self.jump_sound4, self.jump_sound5, self.jump_sound6,
                                self.jump_sound7, self.jump_sound8, self.jump_sound9]

        self.game_over_sound = pygame.mixer.Sound('data/music/game-over-arcade.mp3')

        self.level2 = False
        self.collision_mask = None



    def play_jump_sound(self) -> None:
        sound_index = randint(0, len(self.jump_sound_list)-1)
        self.jump_sound_list[sound_index].set_volume(0.4)
        self.jump_sound_list[sound_index].play()


    def player_input(self) -> None:
        keys = pygame.key.get_pressed()
        if not self.level2:
            if keys[pygame.K_SPACE] and self.rect.bottom >= SCREEN_HEIGHT - 100:
                self.gravity = -20
                self.play_jump_sound()


            if keys[pygame.K_a] and self.rect.left > 0:
                self.rect.x -= 5
                self.is_right = False
            if keys[pygame.K_d] and self.rect.right < SCREEN_WIDTH:
                self.rect.x += 5
                self.is_right = True
            if keys[pygame.K_s] and self.rect.bottom < SCREEN_HEIGHT:
                self.rect.y += 5
            if keys[pygame.K_w] and self.rect.top > 0:
                self.rect.y -= 5

        else:
            if self.collision_mask:
                dx, dy = 0, 0
                if keys[pygame.K_a] and self.rect.left > 0:
                    dx -= 5
                    self.is_right = False
                if keys[pygame.K_d] and self.rect.right < SCREEN_WIDTH:
                    dx += 5
                    self.is_right = True
                if keys[pygame.K_s] and self.rect.bottom < SCREEN_HEIGHT:
                    dy += 5
                if keys[pygame.K_w] and self.rect.top > 0:
                    dy -= 5

                new_x, new_y = self.rect.x + dx, self.rect.y + dy
                if self.collision_mask.get_at((new_x + self.rect.width // 2, new_y + self.rect.height // 2)) == (255, 255, 255, 255):
                    self.rect.x, self.rect.y = new_x, new_y


    
    def apply_gravity(self) -> None:
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.y >= SCREEN_HEIGHT - 180:
            self.rect.y = SCREEN_HEIGHT - 180


    def animation_state(self):
        keys = pygame.key.get_pressed()


        if self.rect.bottom < 620 and not self.level2:
            self.image = self.player_jump
            if not self.is_right:
                self.image = pygame.transform.flip(self.image, True, False)
        else:
            if any(keys):
                if keys[pygame.K_a] and self.rect.left > 0:
                    self.move_left()
                if keys[pygame.K_d] and self.rect.right < SCREEN_WIDTH:
                    self.move_right()
                if self.level2:
                    if keys[pygame.K_s] and self.rect.bottom < SCREEN_HEIGHT:
                        if not self.is_right:
                            self.move_left()
                        else:
                            self.move_right()
                    if keys[pygame.K_w] and self.rect.top > 0:
                        if not self.is_right:
                            self.move_left()
                        else:
                            self.move_right()
            else:
                self.stay()


    def update(self) -> None:
        self.animation_state()
        self.player_input()
        if not self.level2: 
            self.apply_gravity()


    def new_game(self) -> None:
        self.game_over_sound.set_volume(0.5)
        self.game_over_sound.play()
        self.rect = self.image.get_rect(midbottom = (200, SCREEN_HEIGHT - 50))

    def move_right(self):
        self.player_index += 0.1
        if self.player_index >= len(self.player_walk):
            self.player_index = 0
        self.image = self.player_walk[int(self.player_index)]


    def move_left(self):
        self.player_index += 0.1
        if self.player_index >= len(self.player_walk):
            self.player_index = 0
        self.image = self.player_walk[int(self.player_index)]
        self.image = pygame.transform.flip(self.image, True, False)

    def stay(self):
        self.image = self.player_stay
        if not self.is_right:
            self.image = pygame.transform.flip(self.image, True, False)

