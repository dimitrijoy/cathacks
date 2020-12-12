# manages the game, including turns, movement, and end conditions
class Board:
    # constants
    BLACK, WHITE = -1, 1 # for managing turns
    FREE = " " # free space
    INVALID, VALID = False, True # regarding moves
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
        self.__turn = self.WHITE # white always goes first
    
    # determines if a particular move is possible in accordance with the game rules
    def is_available(self, old, new, src, dest):
        if src.lower() == 'p': # pawn 
            if new[0] == old[0] + 1 and new[1] == old[1] and dest == self.FREE: # move one place forward into a free space
                return self.VALID
            elif new[0] == old[0] + 1 and (new[1] == old[1] + 1 or new[1] == old[1] - 1) and dest != self.FREE: # diagonal offensive move
                return self.VALID # determining the color of dest is not necessary, as this is handled in move()
            else:
                return self.INVALID
    
    # moves a specified piece
    # returns True on success and False otherwise for the caller to handle
    def move(self, old, new):
        src, dest = self.__board[old[0]][old[1]], self.__board[new[0]][new[1]]
        src_color, dest_color = self.WHITE if src.isupper() else self.BLACK, self.WHITE if dest.isupper() else self.BLACK

        if src != self.FREE: # moves allowed for pieces only
            if src_color == self.__turn and src_color != dest_color: # player is moving their own piece to a valid space
                if self.is_available(old, new, src, dest): # move is available
                    self.__board[old[0]][old[1]] = self.FREE
                    self.__board[new[0]][new[1]] = src
                    return self.VALID # success!
            
        return self.INVALID # invalid move