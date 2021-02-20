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
    def __init__(self):
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
        if movement == ' ':
            self.release = True

        start_X, end_X, thickness = self.paddle.location()

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

        for i in range(self.H - thickness, self.H):
            for j in range(self.W):
                if self.pattern[i][j] == '=':
                    print(PADDLE_COLOR, sep='', end='')
                    print(CURSOR % (i, j), self.pattern[i][j], end='', sep='', flush=True)
                    print(Style.RESET_ALL, end='', sep='')
                else:
                    print(CURSOR % (i, j), self.pattern[i][j], end='', sep='', flush=True)

    def ball_changes(self):
        X, Y, prev_X, prev_Y = self.ball.location()
        self.pattern[prev_Y][prev_X] = ' '
        r = self.pattern[Y]
        for i in range(len(r)):
            if i == X:
                r[i] = BALL
        self.pattern[Y] = r

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
        hp = 0
        start = 0
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
        self.score += hp + 1

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
        self.time += 0.1
        round(self.time, 1)
        row = self.H - PADDLE_THICKNESS - 3
        t = ['T', 'I', 'M', 'E', ':']
        for char in str(self.time):
            t.append(char)

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
        
        for i in range(len(r)):
            print(CURSOR % (row, i), r[i], end='', sep='', flush=True)

    def update_score(self):
        row = self.H - PADDLE_THICKNESS - 2
        s = ['S', 'C', 'O', 'R', 'E', ':']
        for char in str(self.score):
            s.append(char)

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
        
        for i in range(len(r)):
            print(CURSOR % (row, i), r[i], end='', sep='', flush=True)
    
    def game(self):
        self.life -= 1
        if self.life == 0:
            exit()
        
        self.paddle = Paddle(self.H, self.W, self.pattern)
        self.ball = Ball(self.H, self.W, self.pattern)
        self.release = False

        row = self.H - PADDLE_THICKNESS - 1
        l = ['L', 'I', 'F', 'E', ':']
        for char in str(self.life):
            l.append(char)
        
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
        
        self.pattern[row] = r
        for i in range(len(r)):
            print(CURSOR % (row, i), r[i], end='', sep='', flush=True)
   
    def play(self):
        self.display()
        for i in range(MAIN_LOOP):
            movement = self.paddle.move()
            self.paddle_changes(movement)
            self.ball.start(movement)
            self.ball_changes()
            if self.release:
                arg, temp_x, temp_y = self.ball.brick_collide()
                self.ball.move()
                if arg != None:
                    self.remove_brick(arg, temp_x, temp_y)
            self.update_time()
            self.update_score()
            status = self.ball.check_life()
            if not status:
                self.game()


m = Main()
m.play()