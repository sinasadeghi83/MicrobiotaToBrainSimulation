# Main codes

class Square:
    title = ""
    color = []
    isPermanent = False

## Matter

## Maybe in the future
class Matter(Square):
    pass

## Cell

class Cell(Square):
    secretions = []

## Bacteria

class Bacteria(Cell):
    secretions = ["SCFA's", "LPS"]
    def __init__(self):
        self.color = [102, 204, 255]

## Probiotic

class Probiotic(Bacteria):
    def __init__(self):
        self.color = [204, 204, 0]

## Vessel

class Vessel(Cell):
    def __init__(self):
        self.title = "Vessel"
        self.color = [204, 0, 0]
        self.isPermanent = True

## Nerve

class Nerve(Cell):
    def __init__(self):
        self.title = "Nerve"
        self.color = [255, 204, 0]
        self.isPermanent = True

## Epithelial cell

class Epithelial(Cell):
    def __init__(self):
        self.title = "Epithelial"
        self.color = [102, 255, 153]
        self.isPermanent = False

## Decoding rle pattern

# import re

# def decode(text):
#     for (char, num) in re.findall(r'([a-z])([0-9]+)', text):
#         yield char * int(num)

# f = open("pattern.rle", 'r')
# pattern = ""
# for temp in f:
#     pattern = pattern + temp
# pattern = ''.join(decode(pattern))
# f.close()

## Reading cell file for pattern

def readPattern(fileName):
    f = open(fileName, 'r')
    patStr = ''
    yCount = 0
    xCount = 0
    for line in f:
        if line[0] == '!':
            continue
        patStr += line
        yCount += 1
        xCount = max(len(line), xCount)
    xCount -= 1
    pattern = [['.'] * yCount for i in range(xCount)]
    cords = [0, 0]
    for c in patStr:
        if c == '\n':
            cords[1] += 1
            cords[0] = 0
        else:
            pattern[cords[0]][cords[1]] = c
            cords[0] += 1
    return [pattern, xCount, yCount]

def swapXY(pattern):
    patt = pattern[0]
    newPatt = [['.'] * pattern[1] for i in range(pattern[2])]
    for y in range(pattern[2]):
        for x in range(pattern[1]):
            newPatt[pattern[2] - y-1][x] = patt[x][y]
    return [newPatt, pattern[2], pattern[1]]

def swapXX(pattern):
    patt = pattern[0]
    newPatt = [['.'] * pattern[2] for i in range(pattern[1])]
    for y in range(pattern[2]):
        for x in range(pattern[1]):
            newPatt[pattern[1] - x - 1][y] = patt[x][y]
    return [newPatt, pattern[1], pattern[2]]

def swapYY(pattern):
    patt = pattern[0]
    newPatt = [['.'] * pattern[2] for i in range(pattern[1])]
    for y in range(pattern[2]):
        for x in range(pattern[1]):
            newPatt[x][pattern[2] - y-1] = patt[x][y]
    return [newPatt, pattern[1], pattern[2]]

## Creating the board

breeder = swapYY(readPattern('patterns/backrake1.cells'))
xlength = int(breeder[1]/3*13)
ylength = int(breeder[2]/3*13)
board = [[0] * ylength for i in range(xlength)]
lumenRatio = 6
mucusRatio = 5
subMucusRatio = 2
yRatio = ylength/(subMucusRatio + mucusRatio + lumenRatio)

# for y in range(breeder[2]):
#     for x in range(breeder[1]):
#         print(breeder[0][x][y], end=" ")
#     print('\n')

## Writing patterns

def writePattern(firstCords, lastCords, pattern, klass, space=2):
    for y in range(firstCords[1], lastCords[1]+1):
        if (y - firstCords[1]) %(space + pattern[2]) >= pattern[2]:
            continue
        for x in range(firstCords[0], lastCords[0]+1):
            if (x - firstCords[0]) % (space + pattern[1]) >= pattern[1]:
                continue
            if pattern[0][(x - firstCords[0]) %(space + pattern[1])][(y - firstCords[1]) %(space + pattern[2])] == '.':
                board[x][y] = 0
            else:
                board[x][y] = klass()

#Creating probiotic attack
writePattern([0, 0], [xlength-1, int(lumenRatio*2/3 * yRatio)-1], breeder, Probiotic)

#Creating Bacteria flora
writePattern([0, int(lumenRatio*2/3 * yRatio)], [xlength-1, int(lumenRatio * yRatio -1)], readPattern('patterns/eater1.cells'), Bacteria)

# Creating mucus layer with Tub
writePattern([0, int(yRatio * lumenRatio)], [xlength-1, int(yRatio * (lumenRatio+mucusRatio)-1)], readPattern('patterns/tub.cells'), Epithelial)

#Creating submucuosa
for x in range(xlength):
    for y in range(int(ylength-(yRatio * subMucusRatio)), int(ylength-(yRatio * subMucusRatio/2))):
        if x%4 == 0 or x%4 == 1:
            ner = Nerve()
            board[x][y] = ner
    for y in range(int(ylength-(yRatio * subMucusRatio/2)), ylength):
        ves = Vessel()
        board[x][y] = ves

## Testing that the above cods are correct or not:

# for y in range(int(yRatio * lumenRatio), int(yRatio * lumenRatio + 9)):
#     for x in range(20):
#         print(int(board[x][y] != 0), end=" ")
#     print('\n')

# for y in range(0, int(yRatio * lumenRatio)):
#     for x in range(xlength-20, xlength):
#         print(int(board[x][y] != 0), end=" ")
#     print('\n')

# for y in range(int(ylength-(yRatio * subMucusRatio)), ylength):
#     for x in range(20):
#         print(int(board[x][y] != 0), end=' ')
#     print('\n')

# Game Engine

#Get the type of thing that live in the square
def getClassName(obj):
    name = str(type(obj))
    name = name[name.find("__.")+3:name.find("'", name.find("'")+1)]
    return name

import random
def getNewStatus(x, y, board):
    if len(board) == 0:
        return 0
    if board[x][y] != 0:
        if board[x][y].isPermanent:
            return board[x][y]
    neighbors = dict()
    aliveNeigh = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if (i == 0 and j == 0) or x+i<0 or y+j<0 or x+i >= len(board) or y+j >= len(board[0]):
                continue
            elif board[x+i][y+j] == 0:
                continue
            clName = getClassName(board[x+i][y+j])
            if clName == "Nerve" or clName == "Vessel":
                continue
            neighbors[clName] = neighbors.get(clName, 0) + 1
            aliveNeigh += 1
    if (aliveNeigh == 3 or aliveNeigh == 6) and board[x][y] == 0:
        maxAlive = 0
        maxSort = []
        for sort in neighbors:
            if neighbors[sort] > maxAlive:
                maxAlive = neighbors[sort]
                maxSort.append(sort)
        return globals()[maxSort[random.randint(0, len(maxSort)-1)]]()

    if aliveNeigh < 2 or aliveNeigh > 3:
        return 0

    return board[x][y]

def getNextGen():
    newBoard = [[0] * ylength for i in range(xlength)]
    for x in range(xlength):
        for y in range(ylength):
            newBoard[x][y] = getNewStatus(x, y, board)
    return newBoard

# Graphical setup

import numpy as np
import matplotlib
import matplotlib.pyplot as plt 
import matplotlib.animation as animation

def getGrid():
    im = np.random.randint(254, 255, (xlength, ylength))
    grid = np.dstack([im, im, im])
    for x in range(xlength):
        for y in range(ylength):
            if board[x][y] == 0:
                grid[x, y, :] = [255, 255, 255]
            else:
                grid[x, y, :] = board[x][y].color
    return grid

def update(data=''):
    global board
    board = getNextGen()
    # update data
    img.set_data(getGrid())
    return img
    
fig, ax = plt.subplots()
img = ax.imshow(getGrid(), interpolation='nearest')
ani = animation.FuncAnimation(fig, update, frames=700, interval=100,
                            save_count=50)
# plt.show()

ani.save('testfilm.mp4', fps=30, extra_args=['-vcodec', 'libx264'])