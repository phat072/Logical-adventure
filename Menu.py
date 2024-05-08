import pygame
import sys
from Game import Game
class Monitor:
    """Tạo màn hình khi khởi chạy game"""
    def __init__(self, screen):
        self.screen = screen
        self.WIDTH = screen.get_width()
        self.HEIGHT = screen.get_height()
        self.BG = pygame.image.load(r'./Graphics/background.jpg')
        self.play_button = pygame.image.load(r'./Graphics/playbutton.PNG')
        self.play_button = pygame.transform.scale(self.play_button, (300, 230))
        self.play_rect = self.play_button.get_rect(center=(500, 300))
        pygame.display.set_caption('Wumpus World')


    def run(self):
        running = True
        while running:
            self.screen.blit(self.BG, (0, 0))
            self.screen.blit(self.play_button, self.play_rect)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if self.play_rect.collidepoint(x, y):  # Check if the click was within the play button
                        menu = Menu(self.screen)
                        menu.run()
            pygame.display.flip()
        pygame.quit()


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.WIDTH = screen.get_width()
        self.HEIGHT = screen.get_height()
        self.BG = pygame.image.load(r'./Graphics/background.jpg')
        self.WHITE = (255, 255, 255)
        self.GRAY = (150, 150, 150)
        self.hover = (200,200,200)
        self.FONT = pygame.font.SysFont(None, 42)
        self.bigFONT = pygame.font.SysFont(None, 72)
        self.clock = pygame.time.Clock()
        self.levels = [
            {"name": "Level 1", "file": "tests/test1.txt"},
            {"name": "Level 2", "file": "tests/test2.txt"},
            {"name": "Level 3", "file": "tests/test3.txt"},
            {"name": "Level 4", "file": "tests/test4.txt"},
            {"name": "Level 5", "file": "tests/test5.txt"},
            {"name": "Level 6", "file": "tests/test6.txt"},
            {"name": "Level 7", "file": "tests/test7.txt"},
            {"name": "Level 8", "file": "tests/test8.txt"},
            {"name": "Level 9", "file": "tests/test9.txt"},
            {"name": "Level 10","file": "tests/test10.txt"},
        ]

    def draw_text(self, text, font, color, x, y):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(topleft=(x, y))
        self.screen.blit(text_surface, text_rect)
        
    def run(self):
        x, y = None, None
        while True:
            self.screen.blit(self.BG, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                        
            for i, level in enumerate(self.levels):
                level_name = level["name"]
                level_rect = pygame.Rect(50, 50 + 50 * i, 200, 40)
                color = self.WHITE 
                if level_rect.collidepoint(pygame.mouse.get_pos()):
                    color = self.hover 
                self.draw_text(f"{level_name}", self.FONT, color, 50, 50 + 50 * i)
                if x is not None and y is not None and level_rect.collidepoint(x, y): 
                    game = Game(level["file"])
                    game.run()  
            pygame.display.flip()