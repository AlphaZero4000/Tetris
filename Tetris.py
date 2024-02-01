import pygame as pg
import random

pg.init()

board = [[None for x in range(10)] for x in range(22)]
SQUARE_SIZE = 30

SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill((255, 255, 255))
pg.display.set_caption("Tetris")

BLUE, LIGHT_BLUE, DARK_BLUE = (60, 60, 210), (100, 100, 220), (0, 0, 150)
RED, LIGHT_RED, DARK_RED = (255, 0, 0), (255, 100, 100), (180, 0, 0)
YELLOW, LIGHT_YELLOW, DARK_YELLOW = (232, 232, 12), (255, 255, 110), (195, 195, 0)  
PURPLE, LIGHT_PURPLE, DARK_PURPLE = (195, 60, 195), (230, 110, 230), (135, 30, 135)
TURQUOISE, LIGHT_TURQUOISE, DARK_TURQUOISE = (50, 225, 225), (170, 255, 255), (50, 185, 185)
GREEN, LIGHT_GREEN, DARK_GREEN = (0, 205, 0), (0, 255, 0), (50, 150, 60)
ORANGE, LIGHT_ORANGE, DARK_ORANGE = (255, 100, 0), (250, 145, 75), (195, 80, 0)

is_lose = False

def check_row_completion():
    r = len(board) - 1
    rows_completed = []
    while r >= 0:
        completed = True
        for c in range(len(board[r])):
            if board[r][c] == None:
                completed = False
                break
        if completed:
            rows_completed.append(r)
            board.pop(r)
            board.insert(0, [None for x in range(10)])
        else:
            r -= 1
        '''
    for row in rows_completed:
        #pg.draw.rect(screen, (255, 255, 255), (0, row * SQUARE_SIZE, 300, SQUARE_SIZE))
        #pg.draw.rect(screen, (200, 200, 200), (c * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 1)
        #pg.display.update()
        
        s = pg.Surface((300, SQUARE_SIZE))
        s.fill((255,255,255))
        screen.blit(s, (c * SQUARE_SIZE, row * SQUARE_SIZE))
        for c in range(len(board[0])):
            pg.draw.rect(screen, (0, 0, 0), (c * SQUARE_SIZE, (row - 2) * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pg.draw.rect(screen, board[r][c], (c * SQUARE_SIZE + 2, (row - 2) * SQUARE_SIZE + 2, SQUARE_SIZE - 4, SQUARE_SIZE - 4))
        pg.time.delay(400)
        pg.display.update()
        pg.time.delay(400)
        
    for row in rows_completed:
        board.pop(r)
    for row in rows_completed:
        board.insert(0, [None for x in range(10)])
        '''

class Piece:
    def __init__ (self, type):
        self.type = type
        self.num_rotations = 0
        if type == 'O':
            self.position = [[0, 4], [0, 5], [1, 4], [1, 5]]
            self.color = BLUE
        elif type == 'I':
            self.position = [[1, 3], [1, 4], [1, 5], [1, 6]]
            self.color = TURQUOISE
        elif type == 'S':
            self.position = [[0, 4], [0, 5], [1, 3], [1, 4]]
            self.color = RED
        elif type == 'Z':
            self.position = [[0, 4], [0, 5], [1, 5], [1, 6]]
            self.color = GREEN
        elif type == 'L':
            self.position = [[0, 5], [1, 3], [1, 4], [1, 5]]
            self.color = PURPLE
        elif type == 'J':
            self.position = [[0, 4], [1, 4], [1, 5], [1, 6]]
            self.color = YELLOW
        elif type == 'T':
            self.position = [[0, 5], [1, 4], [1, 5], [1, 6]]
            self.color = ORANGE
    
    def down(self):
        global is_lose
        temp_position = []
        for coordinate in self.position:
            temp_position.append([coordinate[0] + 1, coordinate[1]])
        self.remove_from_board()
        for coordinate in temp_position:        
            if coordinate[0] >= 22 or board[coordinate[0]][coordinate[1]] != None:
                self.place_on_board()
                check_row_completion()
                if coordinate[0] <= 1:
                    is_lose = True
                return False
        self.position = temp_position
        self.place_on_board()
        return True
    
    def right(self):
        temp_position = []
        for coordinate in self.position:
            temp_position.append([coordinate[0], coordinate[1] + 1])
        self.remove_from_board()
        for coordinate in temp_position:           
            if coordinate[1] >= 10 or board[coordinate[0]][coordinate[1]] != None:
                self.place_on_board()
                return
        self.position = temp_position
        self.place_on_board()
    
    def left(self):
        temp_position = []
        for coordinate in self.position:
            temp_position.append([coordinate[0], coordinate[1] - 1])
        self.remove_from_board()
        for coordinate in temp_position:           
            if coordinate[1] < 0 or board[coordinate[0]][coordinate[1]] != None:
                self.place_on_board()
                return
        self.position = temp_position
        self.place_on_board()
    
    def rotate(self):
        self.num_rotations += 1
        temp_position = []
        if self.type == 'O':
            return
        elif self.type == 'I':
            if self.num_rotations % 2 == 0:
                temp_position = [[self.position[1][0], self.position[1][1] - 1], [self.position[1][0], self.position[1][1]], \
                [self.position[1][0], self.position[1][1] + 1], [self.position[1][0], self.position[1][1] + 2]]
            else:
                temp_position = [[self.position[1][0] - 1, self.position[1][1]], [self.position[1][0], self.position[1][1]], \
                [self.position[1][0] + 1, self.position[1][1]], [self.position[1][0] + 2, self.position[1][1]]]
        elif self.type == 'S':
            if self.num_rotations % 2 == 0:
                temp_position = [[self.position[0][0], self.position[0][1]], [self.position[0][0], self.position[0][1] + 1], \
                [self.position[0][0] + 1, self.position[0][1] - 1], [self.position[0][0] + 1, self.position[0][1]]]
            else:
                temp_position = [[self.position[0][0], self.position[0][1]], [self.position[0][0] + 1, self.position[0][1]], \
                [self.position[0][0], self.position[0][1] - 1], [self.position[0][0] - 1, self.position[0][1] - 1]]
        elif self.type == 'Z':
            if self.num_rotations % 2 == 0:
                temp_position = [[self.position[1][0], self.position[1][1] - 1], [self.position[1][0], self.position[1][1]], \
                [self.position[1][0] + 1, self.position[1][1]], [self.position[1][0] + 1, self.position[1][1] + 1]]
            else:
                temp_position = [[self.position[1][0] + 1, self.position[1][1]], [self.position[1][0], self.position[1][1]], \
                [self.position[1][0], self.position[1][1] + 1], [self.position[1][0] - 1, self.position[1][1] + 1]]           
        elif self.type == 'T':    
            if self.num_rotations % 4 == 0:
                temp_position = [[self.position[2][0] - 1, self.position[2][1]], [self.position[2][0], self.position[2][1] - 1], \
                [self.position[2][0], self.position[2][1]], [self.position[2][0], self.position[2][1] + 1]]
            elif self.num_rotations % 4 == 1:
                temp_position = [[self.position[2][0] - 1, self.position[2][1]], [self.position[2][0] + 1, self.position[2][1]], \
                [self.position[2][0], self.position[2][1]], [self.position[2][0], self.position[2][1] + 1]]
            elif self.num_rotations % 4 == 2:
                temp_position = [[self.position[2][0] + 1, self.position[2][1]], [self.position[2][0], self.position[2][1] - 1], \
                [self.position[2][0], self.position[2][1]], [self.position[2][0], self.position[2][1] + 1]]
            else:
                temp_position = [[self.position[2][0] - 1, self.position[2][1]], [self.position[2][0], self.position[2][1] - 1], \
                [self.position[2][0], self.position[2][1]], [self.position[2][0] + 1, self.position[2][1]]]
        elif self.type == 'L':
            if self.num_rotations % 4 == 0:
                temp_position = [[self.position[2][0] - 1, self.position[2][1] + 1], [self.position[2][0], self.position[2][1] - 1], \
                [self.position[2][0], self.position[2][1]], [self.position[2][0], self.position[2][1] + 1]]
            elif self.num_rotations % 4 == 1:
                temp_position = [[self.position[2][0] - 1, self.position[2][1]], [self.position[2][0] + 1, self.position[2][1]], \
                [self.position[2][0], self.position[2][1]], [self.position[2][0] + 1, self.position[2][1] + 1]]
            elif self.num_rotations % 4 == 2:
                temp_position = [[self.position[2][0], self.position[2][1] + 1], [self.position[2][0], self.position[2][1] - 1], \
                [self.position[2][0], self.position[2][1]], [self.position[2][0] + 1, self.position[2][1] - 1]]
            else:
                temp_position = [[self.position[2][0] - 1, self.position[2][1]], [self.position[2][0] + 1, self.position[2][1]], \
                [self.position[2][0], self.position[2][1]], [self.position[2][0] - 1, self.position[2][1] - 1]]
                
        elif self.type == 'J':
            if self.num_rotations % 4 == 0:
                temp_position = [[self.position[2][0] - 1, self.position[2][1] - 1], [self.position[2][0], self.position[2][1] - 1], \
                [self.position[2][0], self.position[2][1]], [self.position[2][0], self.position[2][1] + 1]]
            elif self.num_rotations % 4 == 1:
                temp_position = [[self.position[2][0] - 1, self.position[2][1]], [self.position[2][0] + 1, self.position[2][1]], \
                [self.position[2][0], self.position[2][1]], [self.position[2][0] - 1, self.position[2][1] + 1]]
            elif self.num_rotations % 4 == 2:
                temp_position = [[self.position[2][0] + 1, self.position[2][1] + 1], [self.position[2][0], self.position[2][1] - 1], \
                [self.position[2][0], self.position[2][1]], [self.position[2][0], self.position[2][1] + 1]]
            else:
                temp_position = [[self.position[2][0] - 1, self.position[2][1]], [self.position[2][0] + 1, self.position[2][1]], \
                [self.position[2][0], self.position[2][1]], [self.position[2][0] + 1, self.position[2][1] - 1]]
            
        self.remove_from_board()
        for coordinate in temp_position:           
            if coordinate[0] < 0 or coordinate[0] >= 22 or coordinate[1] < 0 or coordinate[1] >= 10 or board[coordinate[0]][coordinate[1]] != None:
                self.place_on_board()
                return
        self.position = temp_position
        self.place_on_board()
    
    def place_on_board(self): 
        for coordinate in self.position:
            board[coordinate[0]][coordinate[1]] = self.type
            
    def remove_from_board(self):
        for coordinate in self.position:
            board[coordinate[0]][coordinate[1]] = None

def random_piece():
    num = random.randint(1, 7)   
    if num == 1:
        return 'O'  
    if num == 2:
        return 'I' 
    if num == 3:
        return 'T' 
    if num == 4:
        return 'L' 
    if num == 5:
        return 'J' 
    if num == 6:
        return 'S' 
    if num == 7:
        return 'Z'    

run = True
current_piece = Piece(random_piece())
MOVE_DOWN, SPEED = pg.USEREVENT+1, 500
pg.time.set_timer(MOVE_DOWN, SPEED)
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_DOWN:
                if (not current_piece.down()):
                    current_piece = Piece(random_piece())
            elif event.key == pg.K_UP:
                current_piece.rotate()
            elif event.key == pg.K_LEFT:
                current_piece.left()
            elif event.key == pg.K_RIGHT:
                current_piece.right()
            elif event.key == pg.K_SPACE:
                for i in range(22):
                    if (not current_piece.down()):
                        break
                current_piece = Piece(random_piece())
        if event.type == MOVE_DOWN:
            if (not current_piece.down()):
                current_piece = Piece(random_piece())
    screen.fill((255, 255, 255))
    for r in range(len(board)):
        for c in range(len(board[r])):
            pg.draw.rect(screen, (200, 200, 200), (c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 1)
            if board[r][c] != None:
                WIDTH = 4
                color, light, dark = BLUE, LIGHT_BLUE, DARK_BLUE
                if board[r][c] == 'O':
                    color, light, dark = BLUE, LIGHT_BLUE, DARK_BLUE
                elif board[r][c] == 'I':
                    color, light, dark = TURQUOISE, LIGHT_TURQUOISE, DARK_TURQUOISE
                elif board[r][c] == 'S':
                    color, light, dark = RED, LIGHT_RED, DARK_RED
                elif board[r][c] == 'Z':
                    color, light, dark = GREEN, LIGHT_GREEN, DARK_GREEN 
                elif board[r][c] == 'L':
                    color, light, dark = PURPLE, LIGHT_PURPLE, DARK_PURPLE
                elif board[r][c] == 'J':
                    color, light, dark = YELLOW, LIGHT_YELLOW, DARK_YELLOW
                elif board[r][c] == 'T':
                    color, light, dark = ORANGE, LIGHT_ORANGE, DARK_ORANGE
                r -= 2
                pg.draw.rect(screen, color, (c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                pg.draw.polygon(screen, light, [(c * SQUARE_SIZE, r * SQUARE_SIZE), (c * SQUARE_SIZE, (r + 1) * SQUARE_SIZE), (c * SQUARE_SIZE + WIDTH, (r + 1) * SQUARE_SIZE - WIDTH), \
                (c * SQUARE_SIZE + WIDTH, r * SQUARE_SIZE + WIDTH), ((c + 1) * SQUARE_SIZE - WIDTH, r * SQUARE_SIZE + WIDTH), ((c + 1) * SQUARE_SIZE, r * SQUARE_SIZE)])
                pg.draw.polygon(screen, dark, [(c * SQUARE_SIZE, (r + 1) * SQUARE_SIZE), (c * SQUARE_SIZE + WIDTH, (r + 1) * SQUARE_SIZE - WIDTH), ((c + 1) * SQUARE_SIZE - WIDTH, (r + 1) * SQUARE_SIZE - WIDTH), \
                ((c + 1) * SQUARE_SIZE - WIDTH, r * SQUARE_SIZE + WIDTH), ((c + 1) * SQUARE_SIZE, r * SQUARE_SIZE), ((c + 1) * SQUARE_SIZE, (r + 1) * SQUARE_SIZE)])
                r += 2
    if is_lose:
        s = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        s.set_alpha(140)
        s.fill((255,255,255))
        screen.blit(s, (0,0))
        font = pg.font.SysFont(None, 50)
        img = font.render("Game Over", True, (0, 0, 0))
        screen.blit(img, (106, 130))
    pg.display.update()
pg.quit()


