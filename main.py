import pygame
from random import randint
from scene import Menu, Level1, Level2, GameStateManager
from player import Player
from settings import *



class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption(WINDOW_NAME)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        self.player = pygame.sprite.GroupSingle()
        self.player.add(Player())

       

        self.gameStateManager = GameStateManager('menu')
        self.menu = Menu(self.screen, self.gameStateManager)
        self.level1 = Level1(self.screen, self.gameStateManager)
        self.level2 = Level2(self.screen, self.gameStateManager)

        self.level1.set_player(self.player)
        self.level2.set_player(self.player)


        self.states = {
                'menu': self.menu,
                'level1': self.level1,
                'level2': self.level2
                }

        self.current_state = self.gameStateManager.get_state()
        self.states[self.current_state].start_music()   

    def run(self) -> None:
        while True:

            new_state = self.gameStateManager.get_state()
            self.states[new_state].is_line = self.states[self.current_state].is_line
            
            # Transport score from level1 to menu
            if self.states[self.current_state].get_score():
                self.states[new_state].set_score(self.states[self.current_state].get_score())

            if new_state != self.current_state:
                # Change music between scene
                self.states[self.current_state].stop_music()
                self.states[new_state].start_music()
                # Make score to 0 at new game
                self.states[new_state].start_time = pygame.time.get_ticks()
                self.current_state = new_state

            # Run scene
            self.states[self.current_state].run()

            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()

