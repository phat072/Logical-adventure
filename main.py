import tkinter
import tkinter.filedialog
import sys
import os
import pygame
import Agent
from Object import *
from Object import Object
from Player import Player
from Agent import Agent
from Map import Map
from Constants import *
from Constants import CELL_SIZE


def prompt_file():
    """Create a Tk file dialog and cleanup when finished"""
    top = tkinter.Tk()
    top.withdraw()  # hide window
    file_name = tkinter.filedialog.askopenfilename(parent=top)
    top.destroy()
    return file_name


def getCellIDinGroup(pos_x: int, pos_y: int, map_size: int):
    # print(pos_x, pos_y, map_size, pos_x - 1 + (map_size - pos_y) * map_size)
    return pos_x - 1 + (map_size - pos_y) * map_size


def check_breeze_stench_overwriting(cell_info):
    if 'P' in cell_info:
        return False

    return True


def main(filePath):
    AgentWumpus = Agent()
    # Map initialization
    GameMap, AgentWumpus.agentLoc = Map.input(filePath)
    loop_n = GameMap.size() + 1  # true loop size, not map's size
    for y in range(loop_n - 1, 0, -1):
        for x in range(1, loop_n):
            print(GameMap[y][x], end=",")
        print()

    # General initializations
    pygame.display.set_caption('Wumpus World')
    pygame.init()
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("freesansbold", 50, bold=True)
    small_font = pygame.font.SysFont("freesansbold", 30, bold=True)

    # Game screen
    screen_width = GameMap.size() * CELL_SIZE
    screen_height = GameMap.size() * CELL_SIZE
    print(screen_width, screen_height)
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE)

    # Side menu setup
    side_menu_height = 200
    side_menu_color = (200, 200, 200)
    side_menu_surface = pygame.Surface((screen_width, side_menu_height))
    side_menu_rect = side_menu_surface.get_rect()

    screen = pygame.display.set_mode((screen_width, screen_height + side_menu_height),
                                     pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)

    # Pits Group
    pitGroups = pygame.sprite.Group()

    # Monster Group
    monsterGroups = pygame.sprite.Group()
    monsters = []

    # Gold Group
    goldGroup = pygame.sprite.Group()

    # Fog of War Group
    fogGroup = pygame.sprite.Group()

    # Cell Group

    cellGroup = pygame.sprite.Group()
    for y in range(loop_n - 1, 0, -1):
        for x in range(1, loop_n):
            new_cell = Cell(CELL_SIZE * (x - 1), CELL_SIZE * (loop_n - 1 - y), initial_scale=INIT_ZOOM)
            cellGroup.add(new_cell)
            fogGroup.add(new_cell.fog)

            if 'P' in GameMap[y][x]:
                newPitGroup = pygame.sprite.Group()
                pit = Object("Graphics/trap_arrow.png", new_cell, initial_scale=INIT_ZOOM)
                newPitGroup.add(pit)
                if check_breeze_stench_overwriting(GameMap[y][x - 1]):
                    newPitGroup.add(Object("Graphics/air_magic.png",
                                           cell_center=(pit.rect.center[0] - CELL_SIZE, pit.rect.center[1]),
                                           initial_scale=1.5))
                if check_breeze_stench_overwriting(GameMap[y][x + 1]):
                    newPitGroup.add(Object("Graphics/air_magic.png",
                                           cell_center=(pit.rect.center[0] + CELL_SIZE, pit.rect.center[1]),
                                           initial_scale=1.5))
                if check_breeze_stench_overwriting(GameMap[y - 1][x]):
                    newPitGroup.add(Object("Graphics/air_magic.png",
                                           cell_center=(pit.rect.center[0], pit.rect.center[1] + CELL_SIZE),
                                           initial_scale=1.5))
                if check_breeze_stench_overwriting(GameMap[y + 1][x]):
                    newPitGroup.add(Object("Graphics/air_magic.png",
                                           cell_center=(pit.rect.center[0], pit.rect.center[1] - CELL_SIZE),
                                           initial_scale=1.5))
                pitGroups.add(newPitGroup)

            if 'W' in GameMap[y][x]:
                monster = Wumpus("Graphics/zombie_ogre.png", new_cell, initial_scale=INIT_ZOOM)
                if check_breeze_stench_overwriting(GameMap[y][x - 1]):
                    monster.add_stench(Object("Graphics/cloud_poison_1.png",
                                              cell_center=(monster.rect.center[0] - CELL_SIZE, monster.rect.center[1]),
                                              initial_scale=1.5))
                if check_breeze_stench_overwriting(GameMap[y][x + 1]):
                    monster.add_stench(Object("Graphics/cloud_poison_1.png",
                                              cell_center=(monster.rect.center[0] + CELL_SIZE, monster.rect.center[1]),
                                              initial_scale=1.5))
                if check_breeze_stench_overwriting(GameMap[y - 1][x]):
                    monster.add_stench(Object("Graphics/cloud_poison_1.png",
                                              cell_center=(monster.rect.center[0], monster.rect.center[1] + CELL_SIZE),
                                              initial_scale=1.5))
                if check_breeze_stench_overwriting(GameMap[y + 1][x]):
                    monster.add_stench(Object("Graphics/cloud_poison_1.png",
                                              cell_center=(monster.rect.center[0], monster.rect.center[1] - CELL_SIZE),
                                              initial_scale=1.5))
                monsterGroups.add(monster.group)
                monsters.append(monster)

            if 'G' in GameMap[y][x]:
                newGold = Object("Graphics/chest.png", new_cell, initial_scale=INIT_ZOOM)
                goldGroup.add(newGold)

    # Exit door
    doorGroup = pygame.sprite.Group()
    doorGroup.add(Object("Graphics/closed_door.png", cellGroup.sprites()[getCellIDinGroup(1, 1, GameMap.size())],
                         initial_scale=INIT_ZOOM))

    # Player Group
    playerGroup = pygame.sprite.Group()
    player = Player("Graphics/paladin.png",
                    cellGroup.sprites()[getCellIDinGroup(AgentWumpus.agentLoc[1], AgentWumpus.agentLoc[0], GameMap.size())],
                    initial_scale=1.5)
    playerGroup.add(player)
    fogGroup.remove(cellGroup.sprites()[getCellIDinGroup(AgentWumpus.agentLoc[1], AgentWumpus.agentLoc[0], GameMap.size())].fog)

    # Arrow Group
    arrowGroup = pygame.sprite.Group()
    pygame.display.flip()

    clock.tick(120)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        cellGroup.draw(screen)
        pitGroups.draw(screen)
        monsterGroups.draw(screen)
        goldGroup.draw(screen)
        doorGroup.draw(screen)
        playerGroup.draw(screen)
        arrowGroup.draw(screen)
        fogGroup.draw(screen)
        side_menu_surface.fill(side_menu_color)
        screen.blit(side_menu_surface, (0, screen_height))
        move_instruction_surface = small_font.render(f"Move: P", True, (0, 0, 0))
        toggle_instruction_surface = small_font.render(f"Toggle Fog: F", True, (0, 0, 0))
        browse_instruction_surface = small_font.render(f"Browse input map: M", True, (0, 0, 0))
        screen.blit(move_instruction_surface, (10, screen_height + 60))
        screen.blit(toggle_instruction_surface, (10, screen_height + 90))
        screen.blit(browse_instruction_surface, (10, screen_height + 120))
        pygame.display.flip()
        clock.tick(120)

        keys = pygame.key.get_pressed()


def updateMap(shotRoomCoord):
    pass


if __name__ == "__main__":
    main("tests/test1.txt")
