from constants import *
from colorama import Back, Style
from input import Input
import os

class Paddle:
    
    def __init__(self, H, W, pattern):
        '''
            Explanation: Initialisation function for the class

            Parameters:
                start_X: Starting position of the paddle
                end_X: Ending position of the paddle
                thickness: Thickness of the paddle
                V: Velocity of the paddle
        '''
        self.H = H
        self.W = W
        self.pattern = pattern
        self.start_X = W//2 - PADDLE_LENGTH//2
        self.end_X = self.start_X + PADDLE_LENGTH
        self.thickness = PADDLE_THICKNESS
        self.V = PADDLE_V
        self.input = Input()

    def location(self):
        '''
            Explanation: Returns position and thickness of the paddle
        '''
        return self.start_X, self.end_X, self.thickness

    def collision(self, delta=0):
        '''
            Explanation: Handles collision related to paddle and wall

            Parameters:
                temp_start_x: Next position of the starting paddle
                temp_end_x: Next position of the ending paddle
        '''
        temp_start_x = self.start_X + delta
        temp_end_x = self.end_X + delta
        
        if temp_start_x <= X_WALL_LEFT or temp_end_x >= (self.W - X_WALL_RIGHT):
            return True
        else:
            return False

    def move(self):
        '''
            Explanation: Handles movement of the paddle

            Variables:
                movement: Gets input from the user and moves paddle according
        '''

        # Gets input from the user
        os.system('stty -echo')
        movement = self.input.getInput()
        os.system('stty echo')

        # Handles the movement
        if movement == 'a':
            if not self.collision(delta= -self.V):
                self.start_X -= self.V
                self.end_X -= self.V
            else:
                return None
        elif movement == 'd':
            if not self.collision(delta = self.V):
                self.start_X += self.V
                self.end_X += self.V
            else:
                return None

        return movement
