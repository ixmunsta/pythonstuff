# snake game

import math, pygame, random, tkinter

# set some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# set properties for screen
width = 500     
height = 500
size = (width, height)      # set size for screen window
rows = 20                   # set variable for # of rows for grid
columns = 20                # set variable for # of columns for grid
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

# create cube class for updating snake body
class cube(object):

    def __init__(self, start, dirX=1, dirY=0, color=BLUE):
        self.pos = start
        self.dirX = 1
        self.dirY = 0
        self.color = color

    def move(self, dirX, dirY):
        self.dirX = dirX
        self.dirY = dirY
        self.pos = (self.pos[0] + self.dirX, self.pos[1] + self.dirY)

    def draw(self, surface, eyes=False):
        cubeWidth = width // columns        # calculate dimensions for snake cube body, this includes grid
        cubeHeight = height // rows
        i = self.pos[0]                     # set variable to use as row number reference
        j = self.pos[1]                     # set variable to use as column number reference
        rowPixRef = i * cubeHeight          # set variable to convert i row to pixels for screen
        colPixRef = j * cubeWidth           # set variable to convert j column to pixels for screen
        
        # draw cube body using rect. cubeWidth/Height +1s and -2s are so it doesn't line up on grid (offset)
        pygame.draw.rect(surface, self.color, (rowPixRef+1, colPixRef+1, cubeWidth-2, cubeHeight-2))

        # set up an if statement to draw eyes if true
        if eyes:
            xCenter = cubeWidth // 2
            yCenter = cubeHeight // 2
            radius = 3
            eye1 = (rowPixRef + xCenter/2, colPixRef + 8)
            eye2 = (rowPixRef + 3*xCenter/2, colPixRef + 8)
            pygame.draw.circle(surface, RED, eye1, radius)
            pygame.draw.circle(surface, WHITE, eye2, radius)
        

# create a class for the snake

class Snake(object):
    body = []
    turns = {}
    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirX = 0       # setting default motion
        self.dirY = 1       # setting default motion

    def move(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
        
            keys = pygame.key.get_pressed()

            # check for key input from user
            # add a self.head.pos[:] key in the turns dictionary created with the dirX, dirY values
            # this will record when cube is at (row, col), move (dX, dY) depending on user input
            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirX = -1
                    self.dirY = 0
                    self.turns[self.head.pos[:]] = [self.dirX, self.dirY]
                elif keys[pygame.K_UP]:
                    self.dirX = 0
                    self.dirY = -1
                    self.turns[self.head.pos[:]] = [self.dirX, self.dirY]
                elif keys[pygame.K_RIGHT]:
                    self.dirX = 1
                    self.dirY = 0
                    self.turns[self.head.pos[:]] = [self.dirX, self.dirY]
                elif keys[pygame.K_DOWN]:
                    self.dirX = 0
                    self.dirY = 1
                    self.turns[self.head.pos[:]] = [self.dirX, self.dirY]

        # create a counter for snake body object --> body has cube objects in it by appending self.head
        # i will be used to count the cube bodies of the snake as it grows
        # c is the cube (body/head) object reference 
        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body)-1:   # once the counter reaches the last cube
                    self.turns.pop(p)       # delete the stored dirX and dirY values so it doesn't repeat
            else:
                if c.dirX == -1 and c.pos[0] < 0:
                    c.pos = (columns-1, c.pos[1])
                elif c.dirX == 1 and c.pos[0] > columns+1:
                    c.pos = (0, c.pos[1])
                elif c.dirY == -1 and c.pos[1] < 0:
                    c.pos = (c.pos[0], rows-1)
                elif c.dirY == 1 and c.pos[1] > rows+1:
                    c.pos = (c.pos[0], 0)
                else:
                    c.move(c.dirX, c.dirY)

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)

def drawGrid(width, height, rows, columns, surface):
    spaceBtwnRows = height / rows       # calculate spacing between rows for grid
    spaceBtwnCols = width / columns     # calculate spacing between columns for grid
    x = 0
    y = 0

    # draw the grid rows
    for i in range(rows):
        pygame.draw.line(surface, WHITE, (0, y), (width, y))    # draws a straight line from the left to right margin at y
        y += spaceBtwnRows
    
    # draw the grid columns
    for j in range(columns):
        pygame.draw.line(surface, WHITE, (x, 0), (x, height))   # draws a straight line from the top to bottom margin at x
        x += spaceBtwnCols
    

def redrawWindow(surface):
    surface.fill(BLACK)
    drawGrid(width, height, rows, columns, surface)
    s.draw(surface)
    pygame.display.update()

# main loop
def main():
    global s
    done = False
    s = Snake(RED, (10,10))     # create snake class
    
    pygame.init()

    while not done:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        pygame.time.delay(50)   # add a delay
        clock.tick(10)          # 10 fps
        s.move()
        redrawWindow(screen)
    
main()
pygame.quit()