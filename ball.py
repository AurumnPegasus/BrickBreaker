from constants import *
from colorama import Style, Fore, Back
import time

class Ball:

    '''
        Explanation: This class is used to handle the ball used in the game
    '''

    def __init__(self, H, W, pattern):
        '''
            Explanation: This is the initialisation function, called when the class is created

            Paramters:
                H: Height of the Terminal
                W: Width of the Terminal
                pattern: 2D array of the terminal

            Class Variables:
                X: Current X position of the ball
                Y: Current Y position of the ball
                prev_X: Previous X position of the ball (required for deprinting)
                prev_Y: Previous Y position of the ball (required for deprinting)
                V_X: Velocity along the X axis of the ball
                V_Y: Velocity along the Y axis of the ball
                release: Flag if ball has been released from the paddle
                life: Flag if life is lost :(
        '''
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
        '''
            Explanation: Controlls movement of the ball when it is stuck to the paddle

            Parameters:
                movement: Character representing movement of the paddle, hence movement of the ball
                    'a': Move the ball Left
                    'd': Move the ball Right
                    ' ': Release the ball
        '''
        if movement == ' ' and not self.release:
            self.V_Y = Y_VELOCITY
            self.release = True
        elif not self.release:
            if movement == 'a':
                self.prev_X = self.X
                self.X -= PADDLE_V
            elif movement == 'd':
                self.prev_X = self.X
                self.X += PADDLE_V

    def location(self):
        '''
            Explanation: Returns the Current and Previous Location of the ball
        '''
        return self.X, self.Y, self.prev_X, self.prev_Y

    def add_VX(self, temp_x, temp_y):
        '''
            Explanation: Adds X velocity to the ball depending on where the ball hits the paddle
        '''

        # Checks if collision with paddle occurs
        if self.pattern[temp_y][temp_x] == '=':
            start_x = 0
            end_x = 0
            for i in range(len(self.pattern[temp_y])):
                if self.pattern[temp_y][i] == '=':
                    start_x = i
                    end_x = i + PADDLE_LENGTH
                    break
            
            third = PADDLE_LENGTH//3

            # Imparts X velocity based on where collision occurs
            if temp_x >= start_x and temp_x < (start_x + third):
                self.V_X += -Y_VELOCITY
            elif temp_x >= (start_x + third) and temp_x < (start_x + 2*third):
                pass
            elif temp_x >= (start_x + 2*third) and temp_x < (start_x + 3*third):
                self.V_X += Y_VELOCITY

    def brick_collide(self):
        '''
            Explanation: Checks whether the ball is colliding with any brick

            Variables:
                temp_x: Next Position of the ball
                temp_y: Next Position of the ball
                arg: Character the ball hits (if it is a brick)
        '''
        temp_x = self.X + self.V_X
        temp_y = self.Y + self.V_Y

        # Game Over condition
        if temp_y >= self.H:
            self.life = False
            return None, None, None
            
        arg = self.pattern[temp_y][temp_x]
        if arg != ' ' and arg != '=' and arg != '_':
            return arg, temp_x, temp_y
        else:
            return None, None, None

    def check_life(self):
        '''
            Explanation: Returns whether or not you are dead
        '''
        return self.life

    def collide(self, delta_x=0, delta_y=0):
        '''
            Explanation: Handles collision of Ball with Paddle and Bricks and Walls

            Parameters:
                delta_x: Change in X direction
                delta_y: Change in Y direction
        '''
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
        '''
            Explanation: Driver code for ball movement
        '''
        self.collide(delta_x=self.V_X, delta_y=self.V_Y)
        self.prev_Y = self.Y
        self.Y += self.V_Y
        self.prev_X = self.X
        self.X += self.V_X