# dependencies
from board import Board
from chess import Chess
import pygame
import time

pygame.init() # initializes the game

# window caption
CAPTION = "Chess"
pygame.display.set_caption(CAPTION)

# window dimens
DIMENS = WIDTH, HEIGHT = ((800,800))
screenPieces = screen = pygame.display.set_mode(DIMENS)

# colors
WHITE = (242, 242, 242)
BLACK = (40, 120, 40)

# game attrs
board = Board()
b = pygame.transform.scale(pygame.image.load("images/blackBishopElf.png"),(100,100))
p = pygame.transform.scale(pygame.image.load("images/blackPawnElf.png"),(100,100))
r = pygame.transform.scale(pygame.image.load("images/blackRookSanta.png"),(100,100))
k = pygame.transform.scale(pygame.image.load("images/blackKnightReindeer.png"),(100,100))
q = pygame.transform.scale(pygame.image.load("images/blackQueenSanta.png"),(100,100))
a = pygame.transform.scale(pygame.image.load("images/blackKingSanta.png"),(100,100))
B = pygame.transform.scale(pygame.image.load("images/whiteBishopElf.png"),(100,100))
P = pygame.transform.scale(pygame.image.load("images/whitePawnElf.png"),(100,100))
R = pygame.transform.scale(pygame.image.load("images/whiteRookSanta.png"),(100,100))
K = pygame.transform.scale(pygame.image.load("images/whiteKnightReindeer.png"),(100,100))
Q = pygame.transform.scale(pygame.image.load("images/whiteQueenSanta.png"),(100,100))
A = pygame.transform.scale(pygame.image.load("images/whiteKingSanta.png"),(100,100))
FREE = pygame.transform.scale(pygame.image.load("images/blank.png"),(100,100))

# pieces to corresponding images
pieces = {'p': p, 'P': P, 'r': r, 'R': R, 'k': k, 'K': K,
          'b': b, 'B': B, 'q': q, 'Q': Q, 'a': a, 'A': A,
          ' ': FREE}

# displays the game board
def create_board():
    for i in range(board.DIMENS):
        for j in range(board.DIMENS):
            # White then Black
            pygame.draw.rect(screenPieces, WHITE, [(i*2)*100, (2*j)*100, 100, 100])
            pygame.draw.rect(screenPieces, BLACK, [(2*i-1)*100, (2*j)*100, 100, 100])
            # Black then White
            pygame.draw.rect(screenPieces, WHITE, [(2*i-1)*100, (2*j-1)*100, 100, 100])
            pygame.draw.rect(screenPieces, BLACK, [(2*i)*100, (2*j-1)*100, 100, 100])

# updates board after moves
def update_board():
    create_board()
    for i in range(board.DIMENS):
            for j in range(board.DIMENS):
                screenPieces.blit(pieces[board.at(i,j)], ((j*100), (i*100))) 

update_board() # init
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # exits game
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN: # gets cursor coordinates on mouse button down to select piece
            coordinates_init = pygame.mouse.get_pos()
            x_init = coordinates_init[1] // 100
            y_init = coordinates_init[0] // 100
        elif event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
            tempCoordinates = pygame.mouse.get_pos()
            x_temp = tempCoordinates[1]
            y_temp = tempCoordinates[0]
            screenPieces.blit(pieces[board.at(x_init,y_init)], (y_temp,x_temp))
        elif event.type == pygame.MOUSEBUTTONUP: # gets cursor coordinates on mouse button up to drop [move] piece
            coordinates_fin = pygame.mouse.get_pos()
            x_fin = coordinates_fin[1] // 100
            y_fin = coordinates_fin[0] // 100
            board.move((x_init, y_init), (x_fin, y_fin))
            update_board()
    
        # displays GUI
        pygame.display.flip()