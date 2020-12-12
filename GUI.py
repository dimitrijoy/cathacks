import pygame

pygame.init()

# Window Caption
Caption = "Chess"
pygame.display.set_caption(Caption)

# Window Dimensions
size = width, height = ((800,800))
screen = pygame.display.set_mode(size)
screenPieces = pygame.display.set_mode(size)
# Colors
white = (192, 192, 192)
black = (40, 40, 40)

# Displays the game board
def createBoard():
    for i in range(8):
            for j in range(8):
                pygame.draw.rect(screen, white, [(i*2)*100, (2*j)*100, 100, 100])
                pygame.draw.rect(screen, black, [(2*i-1)*100, (2*j)*100, 100, 100])

                pygame.draw.rect(screen, white, [(2*i-1)*100, (2*j-1)*100, 100, 100])
                pygame.draw.rect(screen, black, [(2*i)*100, (2*j-1)*100, 100, 100])

# Game Pieces
blackBishop = pygame.image.load("images/blackBishopElf.png")

blackPawn = pygame.image.load("images/blackPawnElf.png")

blackRook = pygame.image.load("images/blackRookSanta.png")

blackKnight = pygame.image.load("images/blackKnightReindeer.png")

blackQueen = pygame.image.load("images/blackQueenSanta.png")

blackKing = pygame.image.load("images/blackKingSanta.png")


done = False

createBoard()
while not done :
    for event in pygame.event.get():
        # Closes program
        if event.type == pygame.QUIT:
            done = True
        for i in range(8):
            screen.blit(blackPawn, ((i*100)+25, 125))
        for i in range(2):
            screen.blit(blackKnight, (125+(i*600), 25))
            screen.blit(blackRook, (25+(i*600),25))
            screen.blit(blackBishop, (225+(i*300),25))
        screen.blit(blackQueen, (425, 25))
        screen.blit(blackKing, (325, 25))
        
        #Displays GUI
        pygame.display.flip()
