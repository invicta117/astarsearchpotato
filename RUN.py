from ASTAR import run_astar
from ASTAR import  NoOpenNodes
import pygame
import math

#initialize some of the pygame options
pygame.init()
win = pygame.display.set_mode([755, 755])
pygame.display.set_caption("A*")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 25)

# set up the colours that will be used
BLACK = (0, 0, 0)
GRAY = (20, 20, 20)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PINK = (255,20,147)

# create start and end nodes
START = (0,0)
FINISH = (9, 9)

#set the WIDTH HEIGHT and space for the grid
TILE_W = 70
TILE_H = 70
SPACE = 5

# create the grid
MAZE = [[0 for i in range(10)] for j in range(10)]

#set the final path to the end as enpty
PATH = []
YIELD = None

#create lists of zeros for the closed and open nodes as well as the F values, G values and H nodes
C =  O =  F =  G =  H = [[0 for i in range(10)] for j in range(10)]

#set quit option for the while loop
QUIT = False

def MouseClick(click, MAZE):
    row = click[0] // (TILE_W + SPACE)
    col = click[1] // (SPACE + TILE_H)
    if (row, col) != START or (row, col) != FINISH:
        MAZE[col][row] = 1
    return MAZE

def DisplayTiles(row, col, MAZE, C, O, PATH):
    tile_colour = WHITE
    # set walls with the colour black
    if MAZE[row][col] == 1:
        tile_colour = BLACK
    # set closed tiles as red
    if C[row][col] == 1:
        tile_colour = RED
    # set open tiles as green
    if O[row][col] == 1:
        tile_colour = GREEN
    # colour the final path to blue
    for p in PATH:
        if row == p[0] and column == p[1]:
            tile_colour = BLUE
    # change the colour of the start and finish cells as pink
    if (row, column) == START or (row, column) == FINISH:
        tile_colour = PINK
    pygame.draw.rect(win, tile_colour, [SPACE + ((SPACE + TILE_W) * col), SPACE + ((SPACE + TILE_W) * row), TILE_W, TILE_H])




while not QUIT:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            QUIT = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click = pygame.mouse.get_pos()
            MAZE = MouseClick(click, MAZE)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                QUIT = True
                pygame.quit()
                quit()
                break
            if event.key == pygame.K_SPACE:
                if YIELD == None:
                    YIELD = run_astar(MAZE, START, FINISH)
                try:
                    PATH, C, O, F, G, H = next(YIELD)
                except StopIteration:
                    print("Quitting the A* program....")
                    QUIT = True
                except NoOpenNodes:
                    print("There does not appear to be a solution!!")
                    QUIT = True


    clock.tick(60)
    # Set the background
    win.fill(GRAY)


    for row in range(10):
        for column in range(10):
            DisplayTiles(row, column, MAZE, C, O, PATH)


    for row in range(10):
        for column in range(10):
            # fill in values for the F, G and H in the output grid
            text1 = font.render(str(G[column][row]), 1, BLACK)
            align1 = text1.get_width()
            win.blit(text1, (20 + (row * 75) - int(align1 / 2), 20 + column * 75))

            text2 = font.render(str(F[column][row]), 1, BLACK)
            align2 = text2.get_width()
            win.blit(text2, (40 + row * 75 - int(align2 / 2), 50 + column * 75))

            text3 = font.render(str(H[column][row]), 1, BLACK)
            align3 = text3.get_width()
            win.blit(text3, (58 + row * 75 - int(align3 / 2), 20 + column * 75))

    pygame.display.flip()

pygame.quit()