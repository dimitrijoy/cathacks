import pygame

pygame.init()

# Window Caption
Caption = "Chess"
pygame.display.set_caption(Caption)

# Window Dimensions
size = width, height = ((800,800))
screen = pygame.display.set_mode(size)

# Window Extras
red = (255, 0, 0)
green = (0, 188, 0)

done = False


while not done :
    for event in pygame.event.get():
        # Closes program
        if event.type == pygame.QUIT:
            done = True
        # Creates squares
        for i in range(8):
            for j in range(8):
                pygame.draw.rect(screen, red, [(i*2)*100, (2*j)*100, 100, 100])
                pygame.draw.rect(screen, green, [(2*i-1)*100, (2*j)*100, 100, 100])

                pygame.draw.rect(screen, red, [(2*i-1)*100, (2*j-1)*100, 100, 100])
                pygame.draw.rect(screen, green, [(2*i)*100, (2*j-1)*100, 100, 100])

        
        
        #Displays GUI
        pygame.display.flip()
