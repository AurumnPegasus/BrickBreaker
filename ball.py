from constants import *
from colorama import Style, Fore, Back
import time

class Ball:

    def __init__(self, H, W, pattern):
        self.H = H
        self.W = W
        self.pattern = pattern
        self.X = W//2
        self.Y = H - 3
        self.prev_X = W//2
        self.prev_Y = H - 3
        self.V_X = 0
        self.V_Y = 0
        self.release = False
        self.life = True

    def start(self, movement):
        if movement == ' ' and not self.release:
            self.V_Y = Y_VELOCITY
            self.release = True
        elif not self.release:
            if movement == 'a':
                self.prev_X = self.X
                self.X -= 1
            elif movement == 'd':
                self.prev_X = self.X
                self.X += 1

    def location(self):
        return self.X, self.Y, self.prev_X, self.prev_Y

    def add_VX(self, temp_x, temp_y):
        if self.pattern[temp_y][temp_x] == '=':
            start_x = 0
            end_x = 0
            for i in range(len(self.pattern[temp_y])):
                if self.pattern[temp_y][i] == '=':
                    start_x = i
                    end_x = i + PADDLE_LENGTH
                    break
            
            third = PADDLE_LENGTH//3
            if temp_x >= start_x and temp_x < (start_x + third):
                self.V_X += -Y_VELOCITY
            elif temp_x >= (start_x + third) and temp_x < (start_x + 2*third):
                pass
            elif temp_x >= (start_x + 2*third) and temp_x < (start_x + 3*third):
                self.V_X += Y_VELOCITY

    def brick_collide(self):
        temp_x = self.X + self.V_X
        temp_y = self.Y + self.V_Y

        if temp_y >= self.H:
            self.life = False
            return None, None, None
            
        arg = self.pattern[temp_y][temp_x]
        if arg != ' ' and arg != '=' and arg != '_':
            return arg, temp_x, temp_y
        else:
            return None, None, None

    def check_life(self):
        return self.life

    def collide(self, delta_x=0, delta_y=0):
        temp_x = self.X + delta_x
        temp_y = self.Y + delta_y

        if temp_y >= self.H:
            self.life = False
            return

        if temp_x <= X_WALL_LEFT or temp_x >= (self.W -X_WALL_RIGHT):
            self.V_X = -self.V_X
            return

        self.add_VX(temp_x, temp_y)
        if self.pattern[temp_y][self.X] != ' ':
            self.V_Y = -self.V_Y
        elif self.pattern[self.Y][temp_x] != ' ':
            self.V_X = -self.V_X
        elif self.pattern[temp_y][temp_x] != ' ':
            self.V_X = -self.V_X
            self.V_Y = -self.V_Y

    def move(self):

        self.collide(delta_x=self.V_X, delta_y=self.V_Y)
        self.prev_Y = self.Y
        self.Y += self.V_Y
        self.prev_X = self.X
        self.X += self.V_X