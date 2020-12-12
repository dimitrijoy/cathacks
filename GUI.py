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
white = (255, 255, 255)
black = (0, 0, 0)

# Displays the game board
def createBoard():
    for i in range(8):
            for j in range(8):
                pygame.draw.rect(screen, white, [(i*2)*100, (2*j)*100, 100, 100])
                pygame.draw.rect(screen, black, [(2*i-1)*100, (2*j)*100, 100, 100])

                pygame.draw.rect(screen, white, [(2*i-1)*100, (2*j-1)*100, 100, 100])
                pygame.draw.rect(screen, black, [(2*i)*100, (2*j-1)*100, 100, 100])

# Game Pieces
blackBishop = pygame.image.load("blackBishopElf.jpg")
blackBishopRect = blackBishop.get_rect()



done = False

createBoard()
while not done :
    for event in pygame.event.get():
        # Closes program
        if event.type == pygame.QUIT:
            done = True
        screen.blit(blackBishop, (300,20))

        #Displays GUI
        pygame.display.flip()
