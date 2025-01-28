import pygame

class Text:
    def __init__(self, text: str, font_size: int, color: str | tuple, position: tuple, font_path=None):
        self.text = text
        self.font_size = font_size
        self.color = color
        self.position = position
        self.font = pygame.font.Font(font_path, font_size)
        self.rendered_text = self.font.render(self.text, False, self.color)
        self.rendered_text_rect = self.rendered_text.get_rect(center = self.position)

    def draw(self, surface):
        surface.blit(self.rendered_text, self.rendered_text_rect)

    def update_text(self, new_text):
        self.text = new_text
        self.rendered_text = self.font.render(self.text, False, self.color)

    def set_position(self, new_position):
        self.position = new_position

    def set_color(self, new_color):
        self.color = new_color
        self.rendered_text = self.font.render(self.text, False, self.color)

