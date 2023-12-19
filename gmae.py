#tet#
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
#///////////////////////////////////////////////////////////#
PLAYER = 0
AI = 1
#///////////////////////////////////////////////////////////#
EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2
WINDOW_LENGTH = 4
#///////////////////////////////////////////////////////////#
def create_board():
	board = np.zeros((ROW_COUNT,COLUMN_COUNT))#create a matrix of 7 columns and 6 rows and fill it with zeros
	return board

def drop_piece(board, row, col, piece): #drop the piece in the board
	board[row][col] = piece

def is_valid_location(board, col): #check if the column is valid
	return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col): #get the next open row
	for r in range(ROW_COUNT):
		if board[r][col] == 0:
			return r

def print_board(board): #print the board
	print(np.flip(board, 0))
#///////////////////////////////////////////////////////////#
def winning_move(board, piece):
	# Check horizontal locations for win
	for i in range(COLUMN_COUNT-3):
		for j in range(ROW_COUNT):
			if board[j][i] == piece and board[j][i+1] == piece and board[j][i+2] == piece and board[j][i+3] == piece:
				return True

	# Check vertical locations for win
	for i in range(COLUMN_COUNT):
		for j in range(ROW_COUNT-3):
			if board[j][i] == piece and board[j+1][i] == piece and board[j+2][i] == piece and board[j+3][i] == piece:
				return True

	# Check positively sloped diaganols
	for i in range(COLUMN_COUNT-3):
		for j in range(ROW_COUNT-3):
			if board[j][i] == piece and board[j+1][i+1] == piece and board[j+2][i+2] == piece and board[j+3][i+3] == piece:
				return True

	# Check negatively sloped diaganols
	for i in range(COLUMN_COUNT-3):
		for j in range(3, ROW_COUNT):
			if board[i][j] == piece and board[j-1][i+1] == piece and board[j-2][i+2] == piece and board[j-3][i+3] == piece:
				return True
#///////////////////////////////////////////////////////////#
def draw_board(board):
	for i in range(COLUMN_COUNT):
		for j in range(ROW_COUNT):
			pygame.draw.rect(screen, BLUE, (i*SQUARESIZE, j*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
			pygame.draw.circle(screen, BLACK, (int(i*SQUARESIZE+SQUARESIZE/2), int(j*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
	
	for i in range(COLUMN_COUNT):
		for j in range(ROW_COUNT):		
			if board[j][i] == 1:
				pygame.draw.circle(screen, RED, (int(i*SQUARESIZE+SQUARESIZE/2), height-int(j*SQUARESIZE+SQUARESIZE/2)), RADIUS)
			elif board[j][i] == 2: 
				pygame.draw.circle(screen, YELLOW, (int(i*SQUARESIZE+SQUARESIZE/2), height-int(j*SQUARESIZE+SQUARESIZE/2)), RADIUS)
	pygame.display.update()
#///////////////////////////////////////////////////////////#
#minmax algorithm here :-



#///////////////////////////////////////////////////////////#
board = create_board()
print_board(board)
game_over = False
pygame.init()
SQUARESIZE = 110
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE
size = (width, height)
RADIUS = int(SQUARESIZE/2 - 5)
screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()
myfont = pygame.font.SysFont("monospace", 75)
turn = random.randint(PLAYER, AI)
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
				if is_valid_location(board, col):
					row = get_next_open_row(board, col)
					drop_piece(board, row, col, PLAYER_PIECE)
                    
					turn += 1
					turn = turn % 2
					print_board(board)
					draw_board(board)
					

	#  Ask for Player 2 Input
	if turn == AI and not game_over:				
		col = random.randint(0, COLUMN_COUNT-1)
		if is_valid_location(board, col):
			pygame.time.wait(300)
			row = get_next_open_row(board, col)
			drop_piece(board, row, col, AI_PIECE)
			
			print_board(board)
			draw_board(board)
			turn += 1
			turn = turn % 2

			if game_over:
				pygame.time.wait(3000)
