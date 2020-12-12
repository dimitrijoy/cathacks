# dependencies
from game import Board
import pygame

pygame.init() # initializes the game

# window caption
CAPTION = "Chess"
pygame.display.set_caption(CAPTION)

# window dimens
DIMENS = WIDTH, HEIGHT = ((800,800))
screenPieces = screen = pygame.display.set_mode(DIMENS)

# colors
WHITE = (192, 192, 192)
BLACK = (40, 40, 40)

# game attrs
board = Board()
b = pygame.image.load("images/blackBishopElf.png")
p = pygame.image.load("images/blackPawnElf.png")
r = pygame.image.load("images/blackRookSanta.png")
k = pygame.image.load("images/blackKnightReindeer.png")
q = pygame.image.load("images/blackQueenSanta.png")
a = pygame.image.load("images/blackKingSanta.png")
B = pygame.image.load("images/whiteBishopElf.png")
P = pygame.image.load("images/whitePawnElf.png")
R = pygame.image.load("images/whiteRookSanta.png")
K = pygame.image.load("images/whiteKnightReindeer.png")
Q = pygame.image.load("images/whiteQueenSanta.png")
A = pygame.image.load("images/whiteKingSanta.png")
FREE = pygame.image.load("images/blank.png")

# pieces to corresponding images
pieces = {'p': p, 'P': P, 'r': r, 'R': R, 'k': k, 'K': K,
          'b': b, 'B': B, 'q': q, 'Q': Q, 'a': a, 'A': A,
          ' ': FREE}

# displays the game board
def create_board():
    for i in range(8):
        for j in range(8):
            pygame.draw.rect(screen, WHITE, [(i*2)*100, (2*j)*100, 100, 100])
            pygame.draw.rect(screen, BLACK, [(2*i-1)*100, (2*j)*100, 100, 100])
            pygame.draw.rect(screenPieces, WHITE, [(i*2)*100, (2*j)*100, 100, 100])
            pygame.draw.rect(screenPieces, BLACK, [(2*i-1)*100, (2*j)*100, 100, 100])
            pygame.draw.rect(screen, WHITE, [(2*i-1)*100, (2*j-1)*100, 100, 100])
            pygame.draw.rect(screen, BLACK, [(2*i)*100, (2*j-1)*100, 100, 100])
            pygame.draw.rect(screenPieces, WHITE, [(2*i-1)*100, (2*j-1)*100, 100, 100])
            pygame.draw.rect(screenPieces, BLACK, [(2*i)*100, (2*j-1)*100, 100, 100])

# updates board after moves
def update_board():
    create_board()
    for i in range(board.DIMENS):
            for j in range(board.DIMENS):
                screenPieces.blit(pieces[board.at(i,j)], ((j*100)+25, (i*100)+25))    

update_board() # init
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # exits game
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN: # gets cursor coordinates on mouse button down to select piece
            coordinates_init = pygame.mouse.get_pos()
            x_init = coordinates_init[1] // 100
            y_init = coordinates_init[0] // 100
        elif event.type == pygame.MOUSEBUTTONUP: # gets cursor coordinates on mouse button up to drop [move] piece
            coordinates_fin = pygame.mouse.get_pos()
            x_fin = coordinates_fin[1] // 100
            y_fin = coordinates_fin[0] // 100
            board.move((x_init, y_init), (x_fin, y_fin))
            update_board()
    
        # displays GUI
        pygame.display.flip()