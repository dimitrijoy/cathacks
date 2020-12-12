import pygame

pygame.init()

# Window Caption
Caption = "Chess"
pygame.display.set_caption(Caption)

# Window Dimensions
size = width, height = ((800,800))
screen = pygame.display.set_mode(size)

# Window Extras
done = False


while not done :
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        white = (255, 255, 255)
        screen.fill(white)
        tan = (255, 201, 144)
        rect_size = ((100,100))
        pygame.draw.rect(screen, tan, [100,100,100,100])
        pygame.display.flip()
