import pygame
import sys
from random import randint

from pygame.mixer_music import play
from text import Text
from arrows import Obstacle


class BaseScene:
    def __init__(self, music_file=None):
        self.music_file = music_file
        self.score = None

    def start_music(self):
        if self.music_file:
            pygame.mixer.music.load(self.music_file)
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)

    def stop_music(self):
        pygame.mixer.music.stop()

    def set_score(self, score):
        self.score = score

    def get_score(self):
        return self.score

    def run(self):
        pass


class Menu(BaseScene):
    def __init__(self, display, gameStateManager) -> None:
        super().__init__('data/music/menu_music.mp3')
        self.display = display
        self.gameStateManager = gameStateManager
        self.is_line = False

        # Text
        self.boom_text = Text(
                text="BOOM!",
                font_size=150,
                color=(250, 250, 250),
                position=(self.display.get_width()/2, 70)
                )

        self.enter_text = Text(
                text="Please, press enter to Start!",
                font_size=50,
                color=(250, 250, 250),
                position=(self.display.get_width()/2, self.display.get_height()-70)
                )

        # Player Front
        self.player_front_surf = pygame.image.load('data/playersamgs/amg_front.png').convert_alpha()
        self.player_front_rect = self.player_front_surf.get_rect(center = (self.display.get_width()/2, self.display.get_height()/2))
     

    def run(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 550 <= event.pos[0] <= 725 and 225 <= event.pos[1] <= 320:
                    if self.is_line:
                        self.is_line = False
                    else:
                        self.is_line = True


        self.display.fill('red')

        if self.score:
            score_text = Text(
                text=f"Your score: {self.score}",
                font_size=150,
                color=(250, 250, 250),
                position=(self.display.get_width()/2, 70)
                )
            score_text.draw(self.display)
        else:
            self.boom_text.draw(self.display)


        self.enter_text.draw(self.display)
        self.display.blit(self.player_front_surf, self.player_front_rect)

        if self.is_line:
            pygame.draw.line(self.display, 'gold', (0, 0), (self.display.get_width()/2, self.display.get_height()/2-80), 40)
            pygame.draw.line(self.display, 'gold', (self.display.get_width(), 0), (self.display.get_width()/2, self.display.get_height()/2-80), 40)
            pygame.draw.line(self.display, 'gold', (0, self.display.get_height()), (self.display.get_width()/2, self.display.get_height()/2-80), 40)
            pygame.draw.line(self.display, 'gold', (self.display.get_width(), self.display.get_height()), (self.display.get_width()/2, self.display.get_height()/2-80), 40)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            self.gameStateManager.set_state('level1')



class Level1(BaseScene):
    def __init__(self, display, gameStateManager) -> None:
        super().__init__('data/music/game_music.mp3')
        self.display = display
        self.gameStateManager = gameStateManager

        self.is_line = False
        self.start_time = 0
        self.player = None
        self.score_rect = None


        self.obstacle_group = pygame.sprite.Group()

        self.difficult = 700
        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer, self.difficult)

        
        # Background
        self.sky = pygame.image.load('data/background/sky.png')
        self.sky = pygame.transform.scale(self.sky, (self.display.get_width(), self.display.get_height()))

        self.ground = pygame.image.load('data/background/ground.png')
        self.ground = pygame.transform.scale(self.ground, (self.display.get_width(), 250))

    def run(self) -> None:
        # Make Level1 here

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.player:
                    if self.player.sprite.rect.collidepoint(event.pos):
                        self.player.sprite.gravity = -20
                        self.player.sprite.play_jump_sound()
                        
            if event.type == self.obstacle_timer:
                self.obstacle_group.add(Obstacle(randint(0, 3)))


        self.display.fill('green')
        self.display.blit(self.sky, (0, 0))
        self.display.blit(self.ground, (0, self.display.get_height()-100))

        # Score
        if self.score_rect:
            pygame.draw.rect(self.display, 'pink', self.score_rect, 0, 6)
        score = self.display_score()

        # Player
        if self.player:
            self.player.draw(self.display)
            self.player.update()

        if self.player and self.score_rect:
            if self.player.sprite.rect.colliderect(self.score_rect):
                self.player.sprite.rect.bottom = self.score_rect.top


        self.obstacle_group.draw(self.display)
        self.obstacle_group.update()



        if self.is_line:
            pygame.draw.line(self.display, 'gold', (0, 0), (self.player.sprite.rect.topright[0]-15, self.player.sprite.rect.topright[1]+20), 10)
            pygame.draw.line(self.display, 'gold', (self.display.get_width(), 0), (self.player.sprite.rect.topright[0]-15, self.player.sprite.rect.topright[1]+20), 10)
            pygame.draw.line(self.display, 'gold', (0, self.display.get_height()), (self.player.sprite.rect.topright[0]-15, self.player.sprite.rect.topright[1]+20), 10)
            pygame.draw.line(self.display, 'gold', (self.display.get_width(), self.display.get_height()), (self.player.sprite.rect.topright[0]-15, self.player.sprite.rect.topright[1]+20), 10)

        
        if self.player:
            if pygame.sprite.spritecollide(self.player.sprite, self.obstacle_group, False):
                self.obstacle_group.empty()
                self.player.sprite.new_game()
                self.set_score(score)
                self.gameStateManager.set_state('menu')
         

        if self.player:
            if self.player.sprite.rect.bottom < -10:
                self.obstacle_group.empty()
                self.player.sprite.rect = self.player.sprite.image.get_rect(midbottom = (self.display.get_width()/2, self.display.get_height()-50))
                self.set_score(score)
                self.gameStateManager.set_state('level2')
            
    

    def set_player(self, player):
        self.player = player

    
    def display_score(self):
        currect_time = pygame.time.get_ticks() - self.start_time
        score_surf = Text(
                text=f"Score: {int(currect_time/1000)}",
                font_size=50,
                color=(64, 64, 64),
                position=(self.display.get_width()/2, 100)
                )
        self.display.blit(score_surf.rendered_text, score_surf.rendered_text_rect)
        self.score_rect = score_surf.rendered_text_rect
        return int(currect_time/1000)


class Level2(BaseScene):
    def __init__(self, display, gameStateManager) -> None:
        super().__init__('data/music/level2.wav')
        self.display = display
        self.gameStateManager = gameStateManager
        
        self.player = None
        self.is_line = None
        
        self.backroom = pygame.image.load('data/background/backroom.png').convert_alpha()
        self.backroom_walls = pygame.image.load('data/background/backroom_walls.png').convert_alpha()
        self.screamer_bg = pygame.image.load('data/background/screamer.png')

        self.screamer_timer = pygame.USEREVENT + 2
        pygame.time.set_timer(self.screamer_timer, 5000)
        self.screamer = False
 


    def run(self) -> None:
        if self.player:
            self.player.sprite.level2 = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == self.screamer_timer:
                if self.screamer:
                    pygame.quit()
                    sys.exit()
                self.screamer = True
                pygame.mixer.music.load('data/music/screamer.mp3')
                pygame.mixer.music.set_volume(2)
                pygame.mixer.music.play()

        self.display.fill('pink')

        self.display.blit(self.backroom, (0, 0))

        
        if self.player:
            self.player.draw(self.display)
            self.player.update()

        self.display.blit(self.backroom_walls, (0, 0))

        if self.screamer:
            self.display.blit(self.screamer_bg, (0, 0))



    def set_player(self, player):
        self.player = player
        self.player.sprite.collision_mask = pygame.image.load("data/background/collision_mask.png").convert()
        self.player.sprite.collision_mask = pygame.Surface.copy(self.player.sprite.collision_mask).convert_alpha()




class GameStateManager:
    def __init__(self, currentState) -> None:
        self.currentState = currentState

    def get_state(self):
        return self.currentState

    def set_state(self, state):
        self.currentState = state
 
