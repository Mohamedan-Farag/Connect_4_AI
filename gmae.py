import random
import numpy as np
import pygame
import sys
import math
#///////////////////////////////////////////////////////////#
BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
ROW_COUNT = 6
COLUMN_COUNT = 7
R = 6
C = 7
steps_limit = 5e3
max_depth = 42
curr_steps = 0
#///////////////////////////////////////////////////////////#
PLAYER = 2
AI = 1
#///////////////////////////////////////////////////////////#
EMPTY = 0
PLAYER_PIECE = 2
AI_PIECE = 1
WINDOW_LENGTH = 4
board = []
#///////////////////////////////////////////////////////////#
def print_board(): #print the board
	global board
	print(np.flip(board, 0))

def drop_piece(row, col, piece): #drop the piece in the board
	board[row][col] = piece
#///////////////////////////////////////////////////////////#
def draw_board():
	global board
	for i in range(COLUMN_COUNT):
		for j in range(ROW_COUNT):
			pygame.draw.rect(screen, BLUE, (i*SQUARESIZE, j*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
			pygame.draw.circle(screen, BLACK, (int(i*SQUARESIZE+SQUARESIZE/2), int(j*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
	
	for i in range(COLUMN_COUNT):
		for j in range(ROW_COUNT):		
			if board[j][i] == 1:
				pygame.draw.circle(screen, YELLOW, (int(i*SQUARESIZE+SQUARESIZE/2), height-int(j*SQUARESIZE+SQUARESIZE/2)), RADIUS)
			elif board[j][i] == 2: 
				pygame.draw.circle(screen, RED, (int(i*SQUARESIZE+SQUARESIZE/2), height-int(j*SQUARESIZE+SQUARESIZE/2)), RADIUS)
	pygame.display.update()
#///////////////////////////////////////////////////////////#
#minmax algorithm here :-
def init_board():
    global board
    board = [[0 for j in range(C)] for i in range(R)]

def is_full():
    global board
    for j in range(C):
        if board[0][j] == 0:
            return False
    return True

def is_win(x):
    global board
    for i in range(R):
        for j in range(C):
            if i + 3 < R and board[i][j] == x and board[i + 1][j] == x and board[i + 2][j] == x and board[i + 3][j] == x:
                return True
            if j + 3 < C and board[i][j] == x and board[i][j + 1] == x and board[i][j + 2] == x and board[i][j + 3] == x:
                return True
            if i + 3 < R and j + 3 < C and board[i][j] == x and board[i + 1][j + 1] == x and board[i + 2][j + 2] == x and board[i + 3][j + 3] == x:
                return True
            if i + 3 < R and j - 3 >= 0 and board[i][j] == x and board[i + 1][j - 1] == x and board[i + 2][j - 2] == x and board[i + 3][j - 3] == x:
                return True
    return False

def is_terminal():
    return is_win(1) or is_win(2)

def is_valid(col):
    global board
    return board[R-1][col] == 0

def score(i, j, x):
    ret = 0
    max_consecutive = 0
    curr = 0
    p = 0
    empty_spots = 0

    for d in range(4):
        if i + d < R:
            if board[i + d][j] == x:
                p += 1
                curr += 1
                max_consecutive = max(max_consecutive, curr)
            else:
                curr = 0
                if board[i + d][j] == 0:
                    empty_spots += 1

    if p + empty_spots == 4:
        if p == 4:
            ret += 1000
        if p == 3:
            ret += 100
        if p == 2 and max_consecutive == 2:
            ret += 10

    max_consecutive = 0
    curr = 0
    p = 0
    empty_spots = 0
    for d in range(4):
        if j + d < C:
            if board[i][j + d] == x:
                p += 1
                curr += 1
                max_consecutive = max(max_consecutive, curr)
            else:
                curr = 0
                if board[i][j + d] == 0:
                    empty_spots += 1

    if p + empty_spots == 4:
        if p == 4:
            ret += 1000
        if p == 3:
            ret += 100
        if p == 2 and max_consecutive == 2:
            ret += 10

    max_consecutive = 0
    curr = 0
    p = 0
    empty_spots = 0
    for d in range(4):
        if i + d < R and j + d < C:
            if board[i + d][j + d] == x:
                p += 1
                curr += 1
                max_consecutive = max(max_consecutive, curr)
            else:
                curr = 0
                if board[i + d][j + d] == 0:
                    empty_spots += 1

    if p + empty_spots == 4:
        if p == 4:
            ret += 1000
        if p == 3:
            ret += 100
        if p == 2 and max_consecutive == 2:
            ret += 10

    max_consecutive = 0
    curr = 0
    p = 0
    empty_spots = 0
    for d in range(4):
        if i + d < R and j - d >= 0:
            if board[i + d][j - d] == x:
                p += 1
                curr += 1
                max_consecutive = max(max_consecutive, curr)
            else:
                curr = 0
                if board[i + d][j - d] == 0:
                    empty_spots += 1

    if p + empty_spots == 4:
        if p == 4:
            ret += 1000
        if p == 3:
            ret += 100
        if p == 2 and max_consecutive == 2:
            ret += 10

    if x == 1:
        return ret
    else:
        return -ret

def evaluate():
    global board
    ret = 0

    for i in range(R):
        for j in range(C):
            ret += score(i, j, 1) + score(i, j, 2)

    return ret

def add(col, player):
    global board
    for i in range(0,R):
        if board[i][col] == 0:
            board[i][col] = player
            return

def remove(col):
    global board
    for i in range(R-1,-1,-1):
        if board[i][col] != 0:
            board[i][col] = 0
            return
        
def alpha_beta(depth, alpha, beta, player):
    global curr_steps
    curr_steps += 1

    if is_terminal() or depth == 0 or curr_steps > steps_limit:
        return (evaluate(), 0)

    if player == 1:
        value = -1e9
        best = 0

        for j in range(C):
            if is_valid(j):
                add(j, player)

                ret, move = alpha_beta(depth - 1, alpha, beta, 2)
                remove(j)

                if ret > value:
                    value = ret
                    best = j

                alpha = max(alpha, value)

                if alpha >= beta:
                    break

        return (value, best)
    else:
        value = 1e9
        best = 0

        for j in range(C):
            if is_valid(j):
                add(j, player)

                ret, move = alpha_beta(depth - 1, alpha, beta, 1)
                remove(j)

                if ret < value:
                    value = ret
                    best = j

                beta = min(beta, value)

                if alpha >= beta:
                    break

        return (value, best)

def make_move():
    global curr_steps
    move = 0
    value = -1e9

    for i in range(1, max_depth + 1):
        curr_steps = 0

        ret, best = alpha_beta(i, -1e9, 1e9, 1)

        if ret > value:
            value = ret
            move = best

        if curr_steps > steps_limit:
            break

    return move


#///////////////////////////////////////////////////////////#
#board = create_board()
init_board()
#print_board(board)
game_over = False
pygame.init()
SQUARESIZE = 110
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE
size = (width, height)
RADIUS = int(SQUARESIZE/2 - 5)
screen = pygame.display.set_mode(size)
draw_board()
pygame.display.update()
myfont = pygame.font.SysFont("monospace", 75)
#turn = random.randint(PLAYER, AI)
turn = PLAYER
#///////////////////////////////////////////////////////////#
while not game_over:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		if event.type == pygame.MOUSEMOTION:
			pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
			posx = event.pos[0]
			if turn == PLAYER:
				pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
		pygame.display.update()
		if event.type == pygame.MOUSEBUTTONDOWN:
			pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
			# Ask for Player 1 Input
			if turn == PLAYER:
				posx = event.pos[0]
				col = int(math.floor(posx/SQUARESIZE))
				add(col, PLAYER_PIECE)
				if is_terminal():
					label = myfont.render("Player wins!!", 1, RED)
					screen.blit(label, (40,10))
					game_over = True
				turn = 3 - turn
				print_board()
				draw_board()
					

	#  Ask for Player 2 Input
	if turn == AI and not game_over:				
		col = make_move()
		
		pygame.time.wait(300)
		
		add(col, AI_PIECE)
		if is_terminal():
			label = myfont.render("AI wins!!", 1, YELLOW)
			screen.blit(label, (40,10))
			game_over = True
		print_board()
		draw_board()
		turn = 3 - turn

		if game_over:
			pygame.time.wait(3000)
