from constants import *
from input import Input
from layout import Layout
from paddle import Paddle
from ball import Ball
from brick import *
from colorama import Back, Style
import os
import time

class Main:
    '''
        Explanation: This class is used as a driver class to play the game
    '''

    def __init__(self):
        '''
            Explanation: The initialisation function (constructor). It is called when object of the class is created. Clears the screen and initialises the class variables and creates required objects of other classes

            Class Variables:
                H, W: Height and Width of the terminal
                T: Stores the size of the upper wall
                P_T: Stores the thickness of the paddle
                pattern: Stores the terminal as 2D array, storing each pixel as a character
                tiles: Stores the required relation between HP of bricks and character associated
                release: Stores information regarding whether ball has been released or not from the paddle
                time: Stores the time passed since the game began
                score: Stores the score since the game began
                life: Stores the number of life a player has
        '''
        os.system('clear')
        self.H, self.W = os.popen('stty size', 'r').read().split()
        self.H = int(self.H)
        self.W = int(self.W)
        self.T = Y_WALL
        self.P_T = PADDLE_THICKNESS
        self._layout = Layout(self.H, self.W)
        self.pattern = self._layout.layout()
        self.tiles = self._layout.getTiles()
        self.brick = Brick(self.tiles)
        self.paddle = Paddle(self.H, self.W, self.pattern)
        self.ball = Ball(self.H, self.W, self.pattern)
        self.release = False
        self.one = One(self.tiles)
        self.two = Two(self.tiles)
        self.three = Three(self.tiles)
        self.four = Four(self.tiles)
        self.five = Five(self.tiles)
        self.time = 0
        self.score = 0
        self.life = 1


    def display(self):
        '''
            Explanation: Used to initially display the whole 2D array, this is done seperately as no where else is the whole array printed
        '''
        for i in range(self.H):
            for j in range(self.W):
                if self.pattern[i][j] == '_':
                    print(UNBREAKABLE_COLOR, sep='', end='')
                    print(CURSOR % (i, j), self.pattern[i][j], end='', sep='', flush=True)
                    print(Style.RESET_ALL, end='', sep='')
                elif self.pattern[i][j] == '+':
                    print(BRICK_ONE_COLOR, sep='', end='')
                    print(CURSOR % (i, j), self.pattern[i][j], end='', sep='', flush=True)
                    print(Style.RESET_ALL, end='', sep='')
                elif self.pattern[i][j] == '-':
                    print(BRICK_TWO_COLOR, sep='', end='')
                    print(CURSOR % (i, j), self.pattern[i][j], end='', sep='', flush=True)
                    print(Style.RESET_ALL, end='', sep='')
                elif self.pattern[i][j] == '/':
                    print(BRICK_THREE_COLOR, sep='', end='')
                    print(CURSOR % (i, j), self.pattern[i][j], end='', sep='', flush=True)
                    print(Style.RESET_ALL, end='', sep='')
                elif self.pattern[i][j] == '#':
                    print(BRICK_FOUR_COLOR, sep='', end='')
                    print(CURSOR % (i, j), self.pattern[i][j], end='', sep='', flush=True)
                    print(Style.RESET_ALL, end='', sep='')
                elif self.pattern[i][j] == '*':
                    print(BRICK_FIVE_COLOR, sep='', end='')
                    print(CURSOR % (i, j), self.pattern[i][j], end='', sep='', flush=True)
                    print(Style.RESET_ALL, end='', sep='')
                elif self.pattern[i][j] == '=':
                    print(PADDLE_COLOR, sep='', end='')
                    print(CURSOR % (i, j), self.pattern[i][j], end='', sep='', flush=True)
                    print(Style.RESET_ALL, end='', sep='')
                else:
                    print(CURSOR % (i, j) ,self.pattern[i][j], end='', sep='', flush=True)

    def paddle_changes(self, movement):
        '''
            Explanation: Handle all the changes and movements related to paddle

            Parameters:
                movement: A Character which holds the user input
                    'a': move left
                    'd': move right
                    ' ': release the ball if stuck to paddle

            Variables:
                start_X: Starting position of the paddle in X axis
                end_X: Ending position of the paddle in X axis
                thickness: Thickness of the paddle
        '''
        if movement == ' ':
            self.release = True

        start_X, end_X, thickness = self.paddle.location()

        # Changing the pattern
        for i in range(self.H - thickness, self.H):
            r = self.pattern[i]
            for j in range(len(r)):
                if j >= start_X and j < end_X:
                    r[j] = '='
                elif r[j] == '=':
                    r[j] = ' '
                else:
                    r[j] = r[j]
            self.pattern[i] = r

        # Printing the pattern
        for i in range(self.H - thickness, self.H):
            for j in range(self.W):
                if self.pattern[i][j] == '=':
                    print(PADDLE_COLOR, sep='', end='')
                    print(CURSOR % (i, j), self.pattern[i][j], end='', sep='', flush=True)
                    print(Style.RESET_ALL, end='', sep='')
                else:
                    print(CURSOR % (i, j), self.pattern[i][j], end='', sep='', flush=True)

    def ball_changes(self):
        '''
            Explanation: Handles all the changes and movement related to the ball

            Variables:
                X: Current X position of the ball
                Y: Current Y position of the ball
                prev_X: Old X position of the ball (required for deprinting)
                prev_Y: Old Y position of the ball (required for deprinting)
        '''

        X, Y, prev_X, prev_Y = self.ball.location()
        self.pattern[prev_Y][prev_X] = ' '
        r = self.pattern[Y]
        # Changing the current row to include the ball
        for i in range(len(r)):
            if i == X:
                r[i] = BALL
        self.pattern[Y] = r

        # Clearing the ball from previous position
        for i in range(self.W):
            if self.pattern[prev_Y][i] == '+':
                print(BRICK_ONE_COLOR, sep='', end='')
                print(CURSOR % (prev_Y, i), self.pattern[prev_Y][i], end='', sep='', flush=True)
                print(Style.RESET_ALL, end='', sep='')
            elif self.pattern[prev_Y][i] == '-':
                print(BRICK_TWO_COLOR, sep='', end='')
                print(CURSOR % (prev_Y, i), self.pattern[prev_Y][i], end='', sep='', flush=True)
                print(Style.RESET_ALL, end='', sep='')
            elif self.pattern[prev_Y][i] == '/':
                print(BRICK_THREE_COLOR, sep='', end='')
                print(CURSOR % (prev_Y, i), self.pattern[prev_Y][i], end='', sep='', flush=True)
                print(Style.RESET_ALL, end='', sep='')
            elif self.pattern[prev_Y][i] == '#':
                print(BRICK_FOUR_COLOR, sep='', end='')
                print(CURSOR % (prev_Y, i), self.pattern[prev_Y][i], end='', sep='', flush=True)
                print(Style.RESET_ALL, end='', sep='')
            elif self.pattern[prev_Y][i] == '*':
                print(BRICK_FIVE_COLOR, sep='', end='')
                print(CURSOR % (prev_Y, i), self.pattern[prev_Y][i], end='', sep='', flush=True)
                print(Style.RESET_ALL, end='', sep='')
            else:
                print(CURSOR % (prev_Y, i), self.pattern[prev_Y][i], end='', sep='', flush=True) 
        
        # Printing the ball in new position
        for i in range(self.W):
            if self.pattern[Y][i] == '+':
                print(BRICK_ONE_COLOR, sep='', end='')
                print(CURSOR % (Y, i), self.pattern[Y][i], end='', sep='', flush=True)
                print(Style.RESET_ALL, end='', sep='')
            elif self.pattern[Y][i] == '-':
                print(BRICK_TWO_COLOR, sep='', end='')
                print(CURSOR % (Y, i), self.pattern[Y][i], end='', sep='', flush=True)
                print(Style.RESET_ALL, end='', sep='')
            elif self.pattern[Y][i] == '/':
                print(BRICK_THREE_COLOR, sep='', end='')
                print(CURSOR % (Y, i), self.pattern[Y][i], end='', sep='', flush=True)
                print(Style.RESET_ALL, end='', sep='')
            elif self.pattern[Y][i] == '#':
                print(BRICK_FOUR_COLOR, sep='', end='')
                print(CURSOR % (Y, i), self.pattern[Y][i], end='', sep='', flush=True)
                print(Style.RESET_ALL, end='', sep='')
            elif self.pattern[Y][i] == '*':
                print(BRICK_FIVE_COLOR, sep='', end='')
                print(CURSOR % (Y, i), self.pattern[Y][i], end='', sep='', flush=True)
                print(Style.RESET_ALL, end='', sep='')
            else:
                print(CURSOR % (Y, i), self.pattern[Y][i], end='', sep='', flush=True) 

    def remove_brick(self, arg, temp_x, temp_y):
        '''
            Explanation: Handles changes in brick color, and removal of bricks when the ball hits any brick

            Parameters:
                arg: Character with which the ball has collided with
                temp_x: Position of arg along the X axis
                temp_y: Position of arg along the y axis
            
            Variables:
                hp: Stores the HP (hit points) of the brick
                start: Stores the index from where the brick starts
        '''

        hp = 0
        start = 0

        # Finding HP of the brick
        if arg == '[':
            hp = self.brick.type(self.pattern[temp_y][temp_x + 1])
            hp -= 1
            start = temp_x
        elif arg == ']':
            hp = self.brick.type(self.pattern[temp_y][temp_x - 1])
            hp -= 1
            start = temp_x - (BRICK_LEN - 1)
        else:
            hp = self.brick.type(arg)
            hp -= 1
            c = arg
            t = temp_x
            while c != '[':
                t -= 1
                c = self.pattern[temp_y][t]
            start = t

        # Update the score
        self.score += hp + 1

        # Get new character based on hp
        for i in range(start, start + BRICK_LEN):
            if hp == 0:
                self.pattern[temp_y][i] = self.one.reduce(self.pattern[temp_y][i])
            elif hp == 1:
                self.pattern[temp_y][i] = self.two.reduce(self.pattern[temp_y][i])
            elif hp == 2:
                self.pattern[temp_y][i] = self.three.reduce(self.pattern[temp_y][i])
            elif hp == 3:
                self.pattern[temp_y][i] = self.four.reduce(self.pattern[temp_y][i])
            elif hp == 4:
                self.pattern[temp_y][i] = self.five.reduce(self.pattern[temp_y][i])

        # Printing new pattern
        for i in range(self.W):
            if self.pattern[temp_y][i] == '+':
                print(BRICK_ONE_COLOR, sep='', end='')
                print(CURSOR % (temp_y, i), self.pattern[temp_y][i], end='', sep='', flush=True)
                print(Style.RESET_ALL, end='', sep='')
            elif self.pattern[temp_y][i] == '-':
                print(BRICK_TWO_COLOR, sep='', end='')
                print(CURSOR % (temp_y, i), self.pattern[temp_y][i], end='', sep='', flush=True)
                print(Style.RESET_ALL, end='', sep='')
            elif self.pattern[temp_y][i] == '/':
                print(BRICK_THREE_COLOR, sep='', end='')
                print(CURSOR % (temp_y, i), self.pattern[temp_y][i], end='', sep='', flush=True)
                print(Style.RESET_ALL, end='', sep='')
            elif self.pattern[temp_y][i] == '#':
                print(BRICK_FOUR_COLOR, sep='', end='')
                print(CURSOR % (temp_y, i), self.pattern[temp_y][i], end='', sep='', flush=True)
                print(Style.RESET_ALL, end='', sep='')
            elif self.pattern[temp_y][i] == '*':
                print(BRICK_FIVE_COLOR, sep='', end='')
                print(CURSOR % (temp_y, i), self.pattern[temp_y][i], end='', sep='', flush=True)
                print(Style.RESET_ALL, end='', sep='')
            else:
                print(CURSOR % (temp_y, i), self.pattern[temp_y][i], end='', sep='',)     
            
    def update_time(self):
        '''
            Explanation: Updates the time and prints it after each iteration
        '''

        self.time += 0.1

        # Putting time as characters in a list
        round(self.time, 1)
        row = self.H - PADDLE_THICKNESS - 3
        t = ['T', 'I', 'M', 'E', ':']
        for char in str(self.time):
            t.append(char)

        # Updating the pattern
        r = []
        c = 0
        for i in range(self.W):
            if i >= (self.W - X_WALL_RIGHT):
                if c < len(t):
                    r.append(t[c])
                    c += 1
                else:
                    r.append(' ')
            else:
                r.append(self.pattern[row][i])
        
        # Printing the new pattern
        for i in range(len(r)):
            print(CURSOR % (row, i), r[i], end='', sep='', flush=True)

    def update_score(self):
        '''
            Explanation: Updates the scores based on hitting of bricks
        '''

        # Getting the score as a list of characters
        row = self.H - PADDLE_THICKNESS - 2
        s = ['S', 'C', 'O', 'R', 'E', ':']
        for char in str(self.score):
            s.append(char)

        # Updates the pattern
        r = []
        c = 0
        for i in range(self.W):
            if i >= (self.W - X_WALL_RIGHT):
                if c < len(s):
                    r.append(s[c])
                    c += 1
                else:
                    r.append(' ')
            else:
                r.append(self.pattern[row][i])
        
        # Prints the new pattern
        for i in range(len(r)):
            print(CURSOR % (row, i), r[i], end='', sep='', flush=True)

    def game(self):
        '''
            Explanation: Called when a life is lost. Resets the whole game and exits if all lives are lost
        '''

        # Reduction of Life
        self.life -= 1
        if self.life == 0:
            os.system('clear')
            print('Score: ', (self.score + self.time))
            exit()
        
        # Resetting the Game
        self.paddle = Paddle(self.H, self.W, self.pattern)
        self.ball = Ball(self.H, self.W, self.pattern)
        self.release = False

        # Getting number of lives as a list of characters
        row = self.H - PADDLE_THICKNESS - 1
        l = ['L', 'I', 'F', 'E', ':']
        for char in str(self.life):
            l.append(char)

        # Updating pattern        
        r = []
        c = 0
        for i in range(self.W):
            if i >= (self.W - X_WALL_RIGHT):
                if c < len(l):
                    r.append(l[c])
                    c += 1
                else:
                    r.append(' ')
            else:
                r.append(self.pattern[row][i])
        
        # Printing the pattern
        self.pattern[row] = r
        for i in range(len(r)):
            print(CURSOR % (row, i), r[i], end='', sep='', flush=True)
   
    def play(self):
        '''
            Explanation: This is the driver code, which controls all functions and objects
        '''

        # Initial display
        self.display()

        i = 0
        while True:

            # Paddle movement
            movement = self.paddle.move()
            self.paddle_changes(movement)

            # Ball movement
            self.ball.start(movement)
            self.ball_changes()
            if self.release:

                # Ball Brick Collision
                arg, temp_x, temp_y = self.ball.brick_collide()
                self.ball.move()

                # Removing Brick if neccessary
                if arg != None:
                    self.remove_brick(arg, temp_x, temp_y)

            # Updating required variables
            self.update_time()
            self.update_score()

            # Game Status
            status = self.ball.check_life()
            if not status:
                self.game()
            i += 1


# Driver code
m = Main()
m.play()