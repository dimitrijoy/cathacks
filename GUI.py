# dependencies
from chess import AI, Chess
from pygame import mixer
import pygame, time, threading

pygame.init() # initializes the game
'''
# sounds
# bg music
mixer.music.load('Sound/backgroundChristmas.mp3')
mixer.music.play(-1)
mixer.music.set_volume(.1)
'''
# chess piece moving
move = pygame.mixer.Sound('Sound/move.wav')
pygame.mixer.Sound.set_volume(move, .1)

# window caption
CAPTION = "Chess"
pygame.display.set_caption(CAPTION)

# window dimens
DIMENS = WIDTH, HEIGHT = ((1000,800))
screenPieces = screen = pygame.display.set_mode(DIMENS)

# colors
WHITE = (242, 242, 242)
GREEN = (40, 120, 40)
SILVER = (200,200,200)
BLACK = (0, 0, 0)

# game attrs
ai = AI()
chess = Chess(); chess.start()
player = pygame.transform.scale(pygame.image.load("images/Player.png"),(100,100))
computer = pygame.transform.scale(pygame.image.load("images/Computer.png"),(100,100))
wreath = pygame.transform.scale(pygame.image.load("images/wreath.png"),(450,100))
wreath = pygame.transform.rotate(wreath, 90)
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
    for i in range(chess.dimens()):
        for j in range(chess.dimens()):
            # white then black
            pygame.draw.rect(screenPieces, WHITE, [(i*2)*100, (2*j)*100, 100, 100])
            pygame.draw.rect(screenPieces, GREEN, [(2*i-1)*100, (2*j)*100, 100, 100])
            # black then white
            pygame.draw.rect(screenPieces, WHITE, [(2*i-1)*100, (2*j-1)*100, 100, 100])
            pygame.draw.rect(screenPieces, GREEN, [(2*i)*100, (2*j-1)*100, 100, 100])
    # player's side
    pygame.draw.rect(screenPieces, SILVER, [800,0,200,1000])
    pygame.draw.rect(screenPieces, BLACK, [845, 375, 150, 50])
    pygame.draw.rect(screenPieces, BLACK, [865,50,100,100])
    pygame.draw.rect(screenPieces, BLACK, [865,650,100,100])
    screenPieces.blit(player,(865,650))
    screenPieces.blit(computer,(865,50))
    screenPieces.blit(wreath,(780,-35))
    screenPieces.blit(wreath,(780,375))
    

# updates board after moves
def update_board():
    create_board()
    for i in range(chess.dimens()):
            for j in range(chess.dimens()):
                if chess.at(i, j) == ' ':
                    screenPieces.blit(pieces[chess.at(i,j)], ((j*100), (i*100)))
                else:
                    type = chess.at(i,j).get_type()
                    if chess.at(i,j).get_color() == chess.WHITE:
                        type = type.upper()
                    screenPieces.blit(pieces[type], ((j*100), (i*100)))
    screen.blit(font.render(text, True, (255, 255, 255)), (876, 385))

clock = pygame.time.Clock()

counter, text = 0, '0'.rjust(3)
pygame.time.set_timer(pygame.USEREVENT, 1000)
font = pygame.font.SysFont('Consolas', 30)

update_board() # init
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # exits game
            exit()
        if event.type == pygame.USEREVENT: 
            counter += 1
            text = str(counter).rjust(3)
            update_board()
            x_temp = 0
            y_temp = 3
        clock.tick(60)   

        if chess.turn() == chess.WHITE:
            
            if event.type == pygame.MOUSEBUTTONDOWN: # gets cursor coordinates on mouse button down to select piece
                coordinates_init = pygame.mouse.get_pos()
                if coordinates_init <= (800,800):
                    x_init = coordinates_init[1] // 100
                    y_init = coordinates_init[0] // 100
            
            '''
            elif event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
                screenPieces.blit(FREE, (x_init,y_init))
                tempCoordinates = pygame.mouse.get_pos()
                x_temp = tempCoordinates[1]
                y_temp = tempCoordinates[0]
                if chess.at(x_init, y_init) != ' ':
                    screenPieces.blit(pieces[chess.at(x_init,y_init-8).get_type().upper()], (y_temp-50,x_temp-50))
                #update_board()
            '''

            if event.type == pygame.MOUSEBUTTONUP: # gets cursor coordinates on mouse button up to drop [move] piece
                coordinates_fin = pygame.mouse.get_pos()
                if coordinates_fin <= (800,800):
                    x_fin = coordinates_fin[1] // 100
                    y_fin = coordinates_fin[0] // 100
                    moveTrue = chess.move((x_init, y_init), (x_fin, y_fin))
                    if moveTrue:
                        pygame.mixer.Sound.play(move)
                    update_board()
        else:
            next = ai.next_move(chess)
            if next == None: # checkmate
                print("Checkmate!")
            else:
                chess.move(next[0], next[1])

        # displays GUI
        pygame.display.flip()