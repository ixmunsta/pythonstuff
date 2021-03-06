# snake game

import math, pygame, random, tkinter
from tkinter import messagebox

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

    def __init__(self, start, dirX=1, dirY=0, color=RED):
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
            xCenter = cubeWidth // 2    # calculate pixel value for center of cube width
            yCenter = cubeHeight // 2   # calculate pixel value for center of cube height
            radius = 3                  # set radius for size of eyes
            eye1 = (rowPixRef + xCenter/2, colPixRef + 8)   # eye variable with (x, y) position
            eye2 = (rowPixRef + 3*xCenter/2, colPixRef + 8) 
            pygame.draw.circle(surface, WHITE, eye1, radius)
            pygame.draw.circle(surface, WHITE, eye2, radius)
        

# create a class for the snake

class Snake(object):
    body = []
    turns = {}  # turns will be a dictionary using each position location as a key with dirX/dirY values
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
                    c.pos = (columns-1, c.pos[1])   # if moving left and snake hits left of screen, reset at right screen
                elif c.dirX == 1 and c.pos[0] > columns+1:
                    c.pos = (0, c.pos[1])   # if moving right and snake moves off screen, reset at left side
                elif c.dirY == -1 and c.pos[1] < 0:
                    c.pos = (c.pos[0], rows-1)  # if moving up, reset to bottom when moves off screen
                elif c.dirY == 1 and c.pos[1] > rows+1:
                    c.pos = (c.pos[0], 0)   # if moving down, reset to top when moves off screen 
                else:
                    c.move(c.dirX, c.dirY)  # otherwise, continue moving in direction

    def addCube(self):
        tailCube = self.body[-1]    # create a variable reference for the last cube object of snake
        dx, dy = tailCube.dirX, tailCube.dirY   # set variable for tail dirX and dirY motion

        if dx == -1 and dy == 0:    # if snake is moving left
            newCube = cube((tailCube.pos[0]+1, tailCube.pos[1]))  # create a new cube object at x+1, same y as tail
            self.body.append(newCube)   # append to snake body so new cube is drawn
        elif dx == 1 and dy == 0:   # if snake is moving right
            newCube = cube((tailCube.pos[0]-1, tailCube.pos[1]))  # create new cube object at x-1, same y as tail
            self.body.append(newCube)   # append to snake body
        elif dx == 0 and dy == 1:   # if snake is moving down
            newCube = cube((tailCube.pos[0], tailCube.pos[1]-1))  # create new cube object at y-1, same x as tail
            self.body.append(newCube)   # append to snake body
        elif dx == 0 and dy == -1:  # if snake is moving up
            newCube = cube((tailCube.pos[0], tailCube.pos[1]+1))  # create new cube object at y+1, same x as tail
            self.body.append(newCube)   # append to snake body

        self.body[-1].dirX = dx # make new cube added have same dirX motion
        self.body[-1].dirY = dy # make new cube added have same dirY motion

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)        

    def reset(self, pos):
        # reset all parameters
        self.body = []      # reset body objects
        self.head = cube(pos)
        self.body.append(self.head)
        self.turns = {}     # reset turns
        self.dirX = 0       # setting default motion
        self.dirY = 1       # setting default motion

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
    

def redrawWindow(surface):  # function to update game screen
    global snack
    surface.fill(BLACK)
    drawGrid(width, height, rows, columns, surface)
    s.draw(surface)
    snack.draw(surface)
    pygame.display.update()

def randomSnack(rows, columns, snake):  # create function to generate snack on screen
    positions = snake.body

    while True: 
        x = random.randrange(rows)      # use random module to generate random X position in grid
        y = random.randrange(columns)   # use random module to generate random Y position in grid

        # check to see if the snake gets on top of the snack
        # this makes it so that the snack does look generate on top of the snake
        # using lambda anonymous function to avoid using loops
        # can be looped instead to verify if (x,y) == positions.pos (snake.body.pos)
        # this uses the filter function to iterate if (x,y) of snack has a matching position in snake.body
        # it creates a list for the match if there is one
        # if length of that list is greater than 0, then do not use this x, y and make a new set
        if len(list(filter(lambda a : a.pos == (x,y), positions))) > 0:
            continue
        else:
            break

        # could also do this as a loop (but code is longer)
        #for i in positions:
        #    if i.pos == (x,y):
        #        continue
        #    else:
        #        break
        
    return (x,y)

def message_box(subject, content):
    root = tkinter.Tk()  # create root = new tkinter window
    root.attributes("-topmost", True)   # make tkinter window always on top
    root.withdraw() 
    messagebox.showinfo(subject,content)
    try:
        root.destroy()
    except:
        pass

# main loop
def main():
    global s, snack
    done = False
    s = Snake(RED, (10,10))     # create snake class to start off
    snack = cube(randomSnack(rows, columns, s), color=GREEN)
    pygame.init()

    while not done:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        pygame.time.delay(50)   # add a delay
        clock.tick(10)          # 10 fps
        s.move()
        if s.body[0].pos == snack.pos:  # if the head of the snake hits the same position of the snack
            s.addCube() # add another cube to the snake body to make it grow
            snack = cube(randomSnack(rows,columns,s), color=GREEN)
        
        # when snake hits itself --> game end
        for x in range(len(s.body)):
            # use map function to check if snake body position is matching any of the rest of the body positions
            if s.body[x].pos in list(map(lambda z: z.pos, s.body[x+1:])):
                print('Score: ', len(s.body))
                message_box('Game Over', "Try Again")
                s.reset((10,10))
                break

        redrawWindow(screen)
    
main()
pygame.quit()