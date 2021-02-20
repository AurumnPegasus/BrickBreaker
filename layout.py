from constants import *
from colorama import Back, Style

class Layout:
    '''
        Explanation: Handles the Layout of the terminal
    '''
    def __init__(self, H, W):
        '''
            Explanation: Initialisation function for the class

            Paramters: 
                H: Height of the Terminal
                W: Width of the Terminal

            Class Variables:
                Y_UP: Handles the upper wall
                Y_DOWN: Handles the Paddle thickness
                X_LEFT: Handles the Left Wall
                X_RIGHT: Handles the Right Wall
                P_LEN: Handles the Paddle Length
                tiles: Dictionary co-relating HP with character
        '''
        self.H = H
        self.W = W
        self.Y_UP = Y_WALL
        self.Y_DOWN = PADDLE_THICKNESS 
        self.X_LEFT = X_WALL_LEFT
        self.X_RIGHT = self.W - X_WALL_RIGHT
        self.P_LEN = PADDLE_LENGTH
        self.tiles = { 1: '+', 2: '-', 3: '/', 4: '#', 5: '*'}

    def getTiles(self):
        '''
            Explanation: Returns the tiles
        '''
        return self.tiles

    def layout(self):
        '''
            Explanation: Gets the pattern required in a list and returns it
        '''

        pattern = []
        hp = 5

        # Top Empty Lines
        for i in range(self.Y_UP - 1):
            r = []
            for j in range(self.W):
                r.append(' ')
            pattern.append(r)
        
        # Unbreakable Lines
        r = []
        for i in range(self.W):
            r.append('_')
        pattern.append(r)

        # All the bricks and patterns
        count = 0 
        for i in range(0, self.H - self.Y_UP - self.Y_DOWN - 1 -2):
            r = []

            # Number of rows of bricks
            if len(pattern) > 8 and len(pattern) < 14:
                open = True
                close = False
                for j in range(0, self.X_LEFT):
                    r.append(' ')
                for j in range(self.X_LEFT, self.X_RIGHT):

                    # Number of bricks in a row
                    if len(r) >= 30 and len(r) < 100:
                        if open:
                            r.append('[')
                            open = False
                            close = True
                        elif close:
                            if count == BRICK_LEN - 2:
                                r.append(']')
                                close = False
                                open = True
                                count = 0
                            else:
                                count += 1
                                r.append(self.tiles[hp])
                    else:
                        r.append(' ')
                for j in range(self.X_RIGHT, self.W):
                    r.append(' ')
                hp -= 1
            else:
                for j in range(self.W):
                    r.append(' ')
            pattern.append(r)

        # Displays Time
        time = ['T', 'I', 'M', 'E', ':', '0', '0', '0', '.', '0']
        r = []
        c = 0
        for i in range(self.W):
            if i >= (self.W - X_WALL_RIGHT):
                if c < len(time):
                    r.append(time[c])
                    c += 1
                else:
                    r.append(' ')
            else:
                r.append(' ')
        pattern.append(r)

        # Displays Score
        score = ['S', 'C', 'O', 'R', 'E', ':', '0', '0']
        r = []
        c = 0
        for i in range(self.W):
            if i >= (self.W - X_WALL_RIGHT):
                if c < len(score):
                    r.append(score[c])
                    c += 1
                else:
                    r.append(' ')
            else:
                r.append(' ')
        pattern.append(r)

        # Displays Life
        r = []
        life = ['L', 'I', 'F', 'E', ':', ' ', '3']
        c = 0
        for i in range(self.W):
            if i == self.W//2:
                r.append(BALL)
            elif i >= (self.W - X_WALL_RIGHT):
                if c < len(life):
                    r.append(life[c])
                    c += 1
                else:
                    r.append(' ')
            else:
                r.append(' ')
        pattern.append(r)

        # Displays paddle
        paddle_start = self.W//2 - self.P_LEN//2
        for i in range(0, self.Y_DOWN):
            r = []
            for j in range(self.W):
                if j >= paddle_start and j < (paddle_start + self.P_LEN):
                    r.append('=')
                else:
                    r.append(' ')
            pattern.append(r)

        return pattern
        