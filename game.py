# manages the game, including turns, movement, and end conditions
class Board:
    # constants
    BLACK, WHITE = -1, 1 # for managing turns
    FREE = " " # free space
    SCORES = {'p': 10, 'k': 30, 'b': 30, 'r': 50, 'q': 90, 'a': 900}

    def __init__(self):
        # lowercase corresponds to black and uppercase to white
        self.__board = [['r', 'k', 'b', 'q', 'a', 'b', 'k', 'r'],
                        ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
                        ['R', 'K', 'B', 'Q', 'A', 'B', 'K', 'R']]
        self.__turn = WHITE # white always goes first
    
    # moves a particular piece
    # returns True on success and False otherwise for the caller to handle
    def move(self, old, new, turn):
        piece = self.__board[old[0], old[1]] # piece to be moved

        # moves allowed for pieces only
        if piece != FREE:
            if turn == self.__turn: # player is moving their own piece
                dest = self.__board[new[0], new[1]]
                color = WHITE if dest.isupper() else BLACK
                if color != self.__turn: # ensure move is not to player's own piece
                    self.__board[old[0], old[1]] = FREE
                    self.__board[new[0], new[1]] = piece
                    return True # success!
            
        return False # invalid move