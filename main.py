import pygame
from Menu import Monitor



def main():
    pygame.init()
    screen = pygame.display.set_mode((1000, 600))
    monitor  = Monitor(screen)
    monitor.run()
    pygame.quit()
    
if __name__ == '__main__':
    main()  