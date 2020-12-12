import pygame
from game import Board
pygame.init()

# Window Caption
Caption = "Chess"
pygame.display.set_caption(Caption)

# Window Dimensions
size = width, height = ((800,800))
screenPieces = screen = pygame.display.set_mode(size)

# Colors
white = (192, 192, 192)
black = (40, 40, 40)

# Displays the game board
def createBoard():
    for i in range(8):
            for j in range(8):
                pygame.draw.rect(screen, white, [(i*2)*100, (2*j)*100, 100, 100])
                pygame.draw.rect(screen, black, [(2*i-1)*100, (2*j)*100, 100, 100])
                #pygame.draw.rect(screenPieces, white, [(i*2)*100, (2*j)*100, 100, 100])
                #pygame.draw.rect(screenPieces, black, [(2*i-1)*100, (2*j)*100, 100, 100])

                pygame.draw.rect(screen, white, [(2*i-1)*100, (2*j-1)*100, 100, 100])
                pygame.draw.rect(screen, black, [(2*i)*100, (2*j-1)*100, 100, 100])
                #pygame.draw.rect(screenPieces, white, [(2*i-1)*100, (2*j-1)*100, 100, 100])
                #pygame.draw.rect(screenPieces, black, [(2*i)*100, (2*j-1)*100, 100, 100])

# Game Pieces
blackBishop = pygame.image.load("images/blackBishopElf.png")
blackPawn = pygame.image.load("images/blackPawnElf.png")
blackRook = pygame.image.load("images/blackRookSanta.png")
blackKnight = pygame.image.load("images/blackKnightReindeer.png")
blackQueen = pygame.image.load("images/blackQueenSanta.png")
blackKing = pygame.image.load("images/blackKingSanta.png")
whiteBishop = pygame.image.load("images/whiteBishopElf.png")
whitePawn = pygame.image.load("images/whitePawnElf.png")
whiteRook = pygame.image.load("images/whiteRookSanta.png")
whiteKnight = pygame.image.load("images/whiteKnightReindeer.png")
whiteQueen = pygame.image.load("images/whiteQueenSanta.png")
whiteKing = pygame.image.load("images/whiteKingSanta.png")
empty = pygame.image.load("images/blank.png")

# Organizing for quick allocation
pieces = {'p':blackPawn, 'P':whitePawn, 'r':blackRook, 'R':whiteRook, 'k':blackKnight, 'K':whiteKnight,
          'b':blackBishop, 'B':whiteBishop, 'q':blackQueen, 'Q':whiteQueen, 'a':blackKing, 'A':whiteKing,
          ' ':empty}


def start():
    for i in range(8):
            for j in range(8):
                screenPieces.blit(pieces[board.at(i,j)], ((j*100)+25, (i*100)+25))

def moveUpdate():
    createBoard()
    for i in range(8):
            for j in range(8):
                screenPieces.blit(pieces[board.at(i,j)], ((j*100)+25, (i*100)+25))
                




done = False
board = Board()
createBoard()
start()

#Running
while not done :
    for event in pygame.event.get():
        # Closes program
        if event.type == pygame.QUIT:
            done = True
        #Takes coordinates once the mouse is pressed down
        if event.type == pygame.MOUSEBUTTONDOWN:
            cordinatesInit = pygame.mouse.get_pos()
            xInitial = cordinatesInit[1] // 100
            yInitial = cordinatesInit[0] // 100
        #Takes coordinates once the mouse is lifted up, then moves the piece and updates the board
        if event.type == pygame.MOUSEBUTTONUP:
            cordinatesFin = pygame.mouse.get_pos()
            xFinal = cordinatesFin[1] // 100
            yFinal = cordinatesFin[0] // 100
            board.move((xInitial,yInitial),(xFinal,yFinal))
            moveUpdate()

            
        #Displays GUI
        pygame.display.flip()