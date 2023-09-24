import numpy as np
import pygame
import sys
import math
import random

BLUE=(0,0,255)
BLACK=(0,0,0)
RED=(255,0,0)
YELLOW=(255,255,0)

row_count=6
col_count=7

PLAYER = 0
AI = 1
PLAYER_PIECE=1
AI_PIECE=2
WINDOW_LEN=4
EMPTY=0


def create_board():
    board=np.zeros((row_count,col_count))
    return board

def drop_piece(board,row,selection,piece):
    board[row][selection]=piece
    

def valid(board,selection):
    return board[row_count-1][selection]==0

def next_row(board,selection):
    for i in range(row_count):
        if board[i][selection]==0:
            return i 
        
def print_board(board):
    print(np.flip(board,0))

def win(board,piece):
    for i in range(col_count-3):
        for j in range(row_count):
            if board[j][i]==piece and board[j][i+1]==piece and board[j][i+2]==piece and board[j][i+3]==piece:
                return True
    for i in range(col_count):
        for j in range(row_count-3):
            if board[j][i]==piece and board[j+1][i]==piece and board[j+2][i]==piece and board[j+3][i]==piece:
                return True
    for i in range(col_count-3):
        for j in range(row_count-3):
            if board[j][i]==piece and board[j+1][i+1]==piece and board[j+2][i+2]==piece and board[j+3][i+3]==piece:
                return True
    for i in range(col_count-3):
        for j in range(3,row_count):
            if board[j][i]==piece and board[j-1][i+1]==piece and board[j-2][i+2]==piece and board[j-3][i+3]==piece:
                return True
            
def evaluate_window(window, piece):
	score = 0
	opp_piece = PLAYER_PIECE
	if piece == PLAYER_PIECE:
		opp_piece = AI_PIECE

	if window.count(piece) == 4:
		score += 100
	elif window.count(piece) == 3 and window.count(EMPTY) == 1:
		score += 5
	elif window.count(piece) == 2 and window.count(EMPTY) == 2:
		score += 2

	if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
		score -= 4

	return score


            
def score_pos(board,piece):
    score=0
    center_array = [int(i) for i in list(board[:, col_count//2])]
    center_count = center_array.count(piece)
    score += center_count * 6
    for r in range(row_count):
        row_array=[int(i) for i in list(board[r,:])]
        for c in range(col_count-3):
            window=row_array[c:c+WINDOW_LEN]
            if window.count(piece)==4:
                score+=100
            elif window.count(piece)==3 and window.count(EMPTY)==1:
                score +=10
    for c in range(col_count):
        col_array=[int(i)for i in list(board[:,c])]
        for r in range(row_count-3):
            window=col_array[r:r+WINDOW_LEN]
            if window.count(piece)==4:
                score+=100
            elif window.count(piece)==3 and window.count(EMPTY)==1:
                score +=10
    for r in range(row_count-3):
        for c in range(col_count-3):
            window=[board[r+i][c+i] for i in range(WINDOW_LEN)]
            if window.count(piece)==4:
                score+=100
            elif window.count(piece)==3 and window.count(EMPTY)==1:
                score +=10
    for r in range(row_count-3):
        for c in range(col_count-3):
            window=[board[r+3-i][c+i] for i in range(WINDOW_LEN)]
            if window.count(piece)==4:
                score+=100
            elif window.count(piece)==3 and window.count(EMPTY)==1:
                score +=10

    return score

def get_valid_locations(board):
    valid_locations=[]
    for col in range(col_count):
        if valid(board,col):
            valid_locations.append(col)
    return valid_locations


def best_move(board,piece):
    best_score=0
    valid_locations=get_valid_locations(board)
    best_col=random.choice(valid_locations)
    for col in valid_locations:
        row=next_row(board,col)
        temp_board=board.copy()
        drop_piece(temp_board,row,col,piece)
        score=score_pos(temp_board,piece)
        if score>best_score:
            best_score=score
            best_col=col
    return best_col

            
def draw_board(board):
    for c in range(col_count):
        for r in range(row_count):
            pygame.draw.rect(screen,BLUE,(c*SQUARESIZE,r*SQUARESIZE+SQUARESIZE,SQUARESIZE,SQUARESIZE))
            pygame.draw.circle(screen,BLACK, (int(c*SQUARESIZE+SQUARESIZE/2),int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)),RADIUS)

    for c in range(col_count):
        for r in range(row_count):  
            if board[r][c]==PLAYER_PIECE:
                pygame.draw.circle(screen,RED, (int(c*SQUARESIZE+SQUARESIZE/2),height-int(r*SQUARESIZE+SQUARESIZE/2)),RADIUS)
            elif board[r][c]==AI_PIECE:
                pygame.draw.circle(screen,YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2),height-int(r*SQUARESIZE+SQUARESIZE/2)),RADIUS)
    pygame.display.update()


board=create_board()
print_board(board)
over=False

pygame.init()

SQUARESIZE=100

width = col_count*SQUARESIZE
height= (row_count+1)*SQUARESIZE

size=(width,height)

RADIUS=int(SQUARESIZE/2 - 5)

screen=pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

font=pygame.font.SysFont("monospace",75)

turn=random.randint(PLAYER,AI)

while not over:

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            sys.exit()

        if event.type==pygame.MOUSEMOTION:
            pygame.draw.rect(screen,BLACK,(0,0,width,SQUARESIZE))
            posx=event.pos[0]
            if turn==PLAYER:
                pygame.draw.circle(screen,RED,(posx,int(SQUARESIZE/2)),RADIUS)
        
        pygame.display.update()

        if event.type==pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen,BLACK,(0,0,width,SQUARESIZE))
            # print(event.pos)
            if turn==PLAYER:
                posx=event.pos[0]
                selection=int(math.floor(posx/SQUARESIZE))
                if valid(board,selection):
                    row=next_row(board,selection)
                    drop_piece(board,row,selection,PLAYER_PIECE)
                    if win(board,PLAYER_PIECE):
                        print_board(board)
                        label=font.render("Player 1 Wins!!!",1,RED)
                        screen.blit(label,(40,10))
                        over = True

                    turn+=1
                    turn=turn%2

                    print_board(board)
                    draw_board(board)

    if turn == AI and not over:
        # selection=random.randint(0,col_count-1)
        selection=best_move(board,AI_PIECE)
        if valid(board,selection):
            pygame.time.wait(500)
            row=next_row(board,selection)
            drop_piece(board,row,selection,AI_PIECE)
            if win(board,AI_PIECE):
                print_board(board)
                label=font.render("Player 2 Wins!!!",1,YELLOW)
                screen.blit(label,(40,10))
                over = True

            print_board(board)
            draw_board(board)

            turn+=1
            turn=turn%2

    if over:
        pygame.time.wait(3000)