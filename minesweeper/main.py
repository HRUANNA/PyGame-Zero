#to run this game type the command pgzrun main.py into the terminal whilst in this directory

###########
# Imports #
###########
from random import randint
from math import floor

#imports the top tiles
cover = Actor('cover')
flag  = Actor('flag')

#creates a dictionary that stores all the possible bottom tile types
tiles = {0: Actor('blank'),
         1: Actor('one'),
         2: Actor('two'),
         3: Actor('three'),
         4: Actor('four'),
         5: Actor('five'),
         6: Actor('six'),
         7: Actor('seven'),
         8: Actor('eight'),
         'M': Actor('mine'),
         'R': Actor('red'),
         'X': Actor('wrong')}

##############
# Game Setup #
##############

f     = open('minefield_settings.txt')
data  = f.readline()
data  = data[1:-1].split(', ')
wide  = int(data[0])
tall  = int(data[1])
mines = int(data[2])

won = False
lost = False


##################
# Function Setup #
##################

def setup_empty_grid(wide, tall, filler):
    grid = []
    for y in range(tall):
        row = []
        for x in range(wide):
            row.append(filler)
        grid.append(row)
    return grid

def populate_grid(grid, mines, wide, tall):
    for mine in range(mines):
        x, y = randint(0, wide - 1), randint(0,tall - 1)
        while grid[y][x] == 'M':
            x, y = randint(0, wide - 1), randint(0,tall - 1)
        grid[y][x] = 'M'
    return grid

def count_mines(grid):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] != 'M':
                neighbors = [(x - 1, y - 1), (x    , y - 1), (x + 1, y - 1),
                             (x - 1, y    ),                 (x + 1, y    ),
                             (x - 1, y + 1), (x    , y + 1), (x + 1, y + 1)]
                for nx, ny in neighbors:
                    try:
                        if ny >= 0 and nx >= 0 and grid[ny][nx] == 'M':
                            grid[y][x] += 1
                    except:
                        pass
    return grid

def draw():
    xpos, ypos = -15, -15
    for row in range(len(base_grid)):
        ypos += 30
        xpos = -15
        for col in range(len(base_grid[0])):
            xpos += 30
            gridpos = base_grid[row][col]
            tiles[gridpos].pos = xpos, ypos
            tiles[gridpos].draw()
    xpos, ypos = -15, -15
    for row in range(len(top_grid)):
        ypos += 30
        xpos = -15
        for col in range(len(top_grid[0])):
            xpos += 30
            if top_grid[row][col] == 1:
                cover.pos = xpos, ypos
                cover.draw()
            elif top_grid[row][col] == 'F':
                flag.pos = xpos, ypos
                flag.draw()
    if won:
        screen.draw.text('You Win!', center=[WIDTH/2,  HEIGHT/2], fontname="lcd_solid", fontsize=wide*6, color='yellowgreen', owidth=0.5, ocolor="black", alpha=0.6)
    if lost:
        screen.draw.text('You Lose!', center=[WIDTH/2,  HEIGHT/2], fontname="lcd_solid", fontsize=wide*5, color='red', owidth=0.5, ocolor="black", alpha=0.6)

def check_won():
    uncovered = 0
    for row in range(len(top_grid)):
        for col in range(len(top_grid[0])):
            if top_grid[row][col] == 0:
                uncovered += 1
    if (wide * tall) - mines == uncovered:
        won = True
    else:
        won = False
    return won

def when_lost():
    for row in range(len(top_grid)):
        for col in range(len(top_grid[0])):
            if base_grid[row][col] == 'M' and top_grid[row][col] == 1:
                top_grid[row][col] = 0
            if top_grid[row][col] == 'F' and base_grid[row][col] != 'M':
                top_grid[row][col] = 0
                base_grid[row][col] = 'X'

def on_mouse_down(pos, button):
    global won, lost
    if not won and not lost:
        mousepos = (floor(pos[0]/30), floor(pos[1]/30))
        if button == mouse.LEFT:
            if base_grid[mousepos[1]][mousepos[0]] == 'M':
                base_grid[mousepos[1]][mousepos[0]] = 'R'
                lost = True
                when_lost()
            if top_grid[mousepos[1]][mousepos[0]] != 'F':
                top_grid[mousepos[1]][mousepos[0]] = 0
                if base_grid[mousepos[1]][mousepos[0]] == 0:
                    edge_detection((floor(pos[0]/30), floor(pos[1]/30)), base_grid)
        else:
            if top_grid[mousepos[1]][mousepos[0]] == 1:
                top_grid[mousepos[1]][mousepos[0]] = 'F'
            elif top_grid[mousepos[1]][mousepos[0]] == 'F':
                top_grid[mousepos[1]][mousepos[0]] = 1
        won = check_won()
    else:
        if won:
            print('You Won')
        else:
            print('You Lost')

def edge_detection(gridpos, grid):
    zeros = [gridpos]
    past_zeros = []
    for zero in zeros:
        top_grid[zero[1]][zero[0]] = 0
        x, y = zero
        neighbors = [(x - 1, y - 1), (x    , y - 1), (x + 1, y - 1),
                     (x - 1, y    ),                 (x + 1, y    ),
                     (x - 1, y + 1), (x    , y + 1), (x + 1, y + 1)]
        for nx, ny in neighbors:
            try:
                if ny >= 0 and nx >= 0:
                    if grid[ny][nx] == 0 and top_grid[ny][nx] == 1:
                        if top_grid[ny][nx] != 'F':
                            top_grid[ny][nx] = 0
                        if (nx, ny) not in zeros:
                            zeros.append((nx, ny))
                    else:
                        if top_grid[ny][nx] != 'F':
                            top_grid[ny][nx] = 0

            except:
                pass
    return top_grid

################
# Screen Setup #
################

#creates two variables that define the width and height of the screen
WIDTH = ((wide * 30) + 1) #adapts the screen size to fit the number of tiles chosen
HEIGHT = ((tall * 30) + 1) #adapts the screen size to fit the number of tiles chosen

top_grid  = setup_empty_grid(wide, tall, 1)
base_grid = setup_empty_grid(wide, tall, 0)
base_grid = populate_grid(base_grid, mines, wide, tall)
base_grid = count_mines(base_grid)
