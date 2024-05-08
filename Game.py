import sys
import tkinter
import tkinter.filedialog

import pygame

import Reward as reward
from Object import Cell
from Object import Object, Wumpus, Arrow
from Player import Player
from Agent import Agent
from Constants import *
from Constants import CELL_SIZE
from Map import Map


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


def Game(filePath):
    agent = Agent()
    # map, agent.agentLoc = input("tests/test"+argv[1]+".txt")
    map, agent.agentLoc = Map.input(filePath)

    loop_n = map.size() + 1  # true loop size, not map's size
    for y in range(loop_n - 1, 0, -1):
        for x in range(1, loop_n):
            print(map[y][x], end=",")
        print()

    # General initializations
    pygame.display.set_caption('Wumpus World')
    pygame.init()
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("freesansbold", 50, bold=True)
    small_font = pygame.font.SysFont("freesansbold", 30, bold=True)

    # Game screen
    screen_width = map.size() * CELL_SIZE
    screen_height = map.size() * CELL_SIZE
    print(screen_width, screen_height)
    screen = pygame.display.set_mode((screen_width, screen_height),
                                     pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)

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

            if 'P' in map[y][x]:
                newPitGroup = pygame.sprite.Group()
                pit = Object("Graphics/trap_arrow.png", new_cell, initial_scale=INIT_ZOOM)
                newPitGroup.add(pit)
                if check_breeze_stench_overwriting(map[y][x - 1]):
                    newPitGroup.add(Object("Graphics/air_magic.png",
                                           cell_center=(pit.rect.center[0] - CELL_SIZE, pit.rect.center[1]),
                                           initial_scale=1.5))
                if check_breeze_stench_overwriting(map[y][x + 1]):
                    newPitGroup.add(Object("Graphics/air_magic.png",
                                           cell_center=(pit.rect.center[0] + CELL_SIZE, pit.rect.center[1]),
                                           initial_scale=1.5))
                if check_breeze_stench_overwriting(map[y - 1][x]):
                    newPitGroup.add(Object("Graphics/air_magic.png",
                                           cell_center=(pit.rect.center[0], pit.rect.center[1] + CELL_SIZE),
                                           initial_scale=1.5))
                if check_breeze_stench_overwriting(map[y + 1][x]):
                    newPitGroup.add(Object("Graphics/air_magic.png",
                                           cell_center=(pit.rect.center[0], pit.rect.center[1] - CELL_SIZE),
                                           initial_scale=1.5))
                pitGroups.add(newPitGroup)

            if 'W' in map[y][x]:
                monster = Wumpus("Graphics/zombie_ogre.png", new_cell, initial_scale=INIT_ZOOM)
                if check_breeze_stench_overwriting(map[y][x - 1]):
                    monster.add_stench(Object("Graphics/cloud_poison_1.png",
                                              cell_center=(monster.rect.center[0] - CELL_SIZE, monster.rect.center[1]),
                                              initial_scale=1.5))
                if check_breeze_stench_overwriting(map[y][x + 1]):
                    monster.add_stench(Object("Graphics/cloud_poison_1.png",
                                              cell_center=(monster.rect.center[0] + CELL_SIZE, monster.rect.center[1]),
                                              initial_scale=1.5))
                if check_breeze_stench_overwriting(map[y - 1][x]):
                    monster.add_stench(Object("Graphics/cloud_poison_1.png",
                                              cell_center=(monster.rect.center[0], monster.rect.center[1] + CELL_SIZE),
                                              initial_scale=1.5))
                if check_breeze_stench_overwriting(map[y + 1][x]):
                    monster.add_stench(Object("Graphics/cloud_poison_1.png",
                                              cell_center=(monster.rect.center[0], monster.rect.center[1] - CELL_SIZE),
                                              initial_scale=1.5))
                monsterGroups.add(monster.group)
                monsters.append(monster)

            if 'G' in map[y][x]:
                newGold = Object("Graphics/chest.png", new_cell, initial_scale=INIT_ZOOM)
                goldGroup.add(newGold)

    # Exit door
    doorGroup = pygame.sprite.Group()
    doorGroup.add(Object("Graphics/closed_door.png", cellGroup.sprites()[getCellIDinGroup(1, 1, map.size())],
                         initial_scale=INIT_ZOOM))

    # Player Group
    playerGroup = pygame.sprite.Group()
    player = Player("Graphics/paladin.png",
                    cellGroup.sprites()[getCellIDinGroup(agent.agentLoc[1], agent.agentLoc[0], map.size())],
                    initial_scale=1.5)
    playerGroup.add(player)
    fogGroup.remove(cellGroup.sprites()[getCellIDinGroup(agent.agentLoc[1], agent.agentLoc[0], map.size())].fog)

    # Arrow Group
    arrowGroup = pygame.sprite.Group()

    # Misc
    pause = True
    fog = True
    isRunning = True

    path = []
    isShooting = False
    waiting_for_arrow = False

    deathfont = pygame.font.SysFont("freesansbold", 50, bold=True)
    death_noti = deathfont.render(f"A G E N T    D I E D", True, (233, 150, 122))
    escape_noti = deathfont.render(f"E S C A P E D", True, (124, 252, 0))
    # Main game loop
    while isRunning:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    # print("pause changed")
                    pause = not pause
                    if not agent.isAlive or (agent.isEscaping and agent.agentLoc[0] == 1 and agent.agentLoc[1] == 1):
                        isRunning = False
                        pause = True
                if event.key == pygame.K_f:
                    fog = not fog
                if event.key == pygame.K_m:
                    f = prompt_file()
                    if len(f) > 0:
                        Game(f)
                        return

        if (agent.isAlive and not agent.isEscaping) or len(path) != 0:
            if not pause:
                if len(path) == 0:
                    # print('===========================', agent.agentLoc)
                    agent.perceiveEnvironment(map)
                    # print('kb: ', agent.kb.clauses)

                    # if (agent.agentLoc[0], agent.agentLoc[1]) == (2, 9):
                    #     o = 0
                    nextRoom = agent.findASafeStep(map.size())
                    isShooting = False
                    if nextRoom == [-1, -1]:
                        nextRoom, isShooting, maybePit = agent.forceAStep(map.size())
                        print('isShooting', isShooting)
                        print('maybePit', maybePit)
                        if maybePit and agent.foundExit:
                            nextRoom = [1, 1]
                            agent.isEscaping = True
                            print('escape')

                    print(nextRoom)
                    path = agent.playPath(nextRoom)
                    if (nextRoom[0], nextRoom[1]) == (2, 9):
                        o = 0

                if len(path) != 0:
                    agent.point += reward.PUNISHMENT_FOR_MOVING
                    nextRoom = path[0]
                    path.pop(0)
                    if len(path) == 0 and isShooting:
                        agent.shoot(nextRoom, map)
                        arrow = Arrow(cellGroup.sprites()[
                                          getCellIDinGroup(agent.agentLoc[1], agent.agentLoc[0], map.size())].rect,
                                      cellGroup.sprites()[getCellIDinGroup(nextRoom[1], nextRoom[0], map.size())])
                        arrowGroup.add(arrow)
                        waiting_for_arrow = True
                    player.play_path(cellGroup.sprites()[getCellIDinGroup(nextRoom[1], nextRoom[0], map.size())])
                    agent.agentLoc = nextRoom
                    fogGroup.remove(
                        cellGroup.sprites()[getCellIDinGroup(agent.agentLoc[1], agent.agentLoc[0], map.size())].fog)

                if not agent.isAlive:
                    print("die")

                pause = not pause

        cellGroup.draw(screen)
        cellGroup.update()

        monsterGroups.draw(screen)
        monsterGroups.update()

        pitGroups.draw(screen)
        pitGroups.update()

        doorGroup.draw(screen)
        doorGroup.update()

        goldGroup.draw(screen)
        goldGroup.update()

        playerGroup.draw(screen)
        playerGroup.update()

        if fog:
            fogGroup.draw(screen)
            fogGroup.update()

        arrowGroup.draw(screen)
        arrowGroup.update()

        if waiting_for_arrow:
            # Check if the arrow has reached the target cell
            if arrowGroup.sprites()[0].reached_target:
                waiting_for_arrow = False
                print("Arrow reached the target cell!")
                for monster in monsters:
                    if monster.check_killed(arrowGroup.sprites()[0]):
                        for sprite in monster.group:
                            monsterGroups.remove(sprite)
                arrowGroup.remove(arrowGroup.sprites()[0])

        # Draw bottom menu
        side_menu_surface.fill(side_menu_color)
        screen.blit(side_menu_surface, (0, screen_height))

        # Draw score on the bottom menu
        score_surface = font.render(f"Score: {agent.point}", True, (0, 0, 0))
        screen.blit(score_surface, (10, screen_height + 20))

        # Draw instructions on the bottom menu
        move_instruction_surface = small_font.render(f"Move: P", True, (0, 0, 0))
        togglefog_instruction_surface = small_font.render(f"Toggle Fog: F", True, (0, 0, 0))
        browse_instruction_surface = small_font.render(f"Browse input map: M", True, (0, 0, 0))

        screen.blit(move_instruction_surface, (10, screen_height + 60))
        screen.blit(togglefog_instruction_surface, (10, screen_height + 90))
        screen.blit(browse_instruction_surface, (10, screen_height + 120))

        # Game over display
        if not agent.isAlive:
            screen.blit(death_noti, (10, screen_height / 2))

        # Game victory display
        if agent.isEscaping and agent.agentLoc[0] == 1 and agent.agentLoc[1] == 1:
            screen.blit(escape_noti, (10, screen_height / 2))

        pygame.display.flip()

        clock.tick(120)


def updateMap(shotRoomCoord):
    pass