import pygame
from Object import Cell


class Player(pygame.sprite.Sprite):
    def __init__(self, picture_path, cell: Cell, initial_scale=1.0):
        super().__init__()

        # Set scale
        self.scale = initial_scale

        # Load image
        self.original_image = pygame.image.load(picture_path).convert_alpha()
        self.image = self.original_image

        # Scale the image based on the current zoom level
        new_width = int(self.original_image.get_width() * self.scale)
        new_height = int(self.original_image.get_height() * self.scale)
        self.image = pygame.transform.scale(self.original_image, (new_width, new_height))

        self.rect = self.image.get_rect()
        self.rect.center = cell.rect.center

    def play_path(self, next_cell):
        self.rect.center = next_cell.rect.center
