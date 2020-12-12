# manages the game, including turns, movement, and end conditions
class Board:
    # constants
    DIMENS = 8 # board dimens
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
    
    # returns piece at [row][col]
    def at(self, row, col):
        return self.__board[row][col]
    
    # determines if a particular move is possible in accordance with the game rules
    def is_available(self, old, new, src, dest):
        if src.lower() == 'p': # pawn 
            if new[0] == old[0] - 1 and new[1] == old[1] and dest == self.FREE: # move one place forward into a free space
                return self.VALID
            elif new[0] == old[0] - 1 and (new[1] == old[1] + 1 or new[1] == old[1] - 1) and dest != self.FREE: # diagonal offensive move
                return self.VALID # determining the color of dest is not necessary, as this is handled in move()
            else:
                return self.INVALID
        if src.lower() == 'k': # knight
            if new[0] == old[0] - 3 and (new[1] == old[1] + 1 or new[1] == old[1] - 1)  and dest == self.FREE: # move three places forward and one place to the right or left
                return self.VALID
            elif new[0] == old[0] + 1 and (new[1] == old[1] + 3 or new[1] == old[1] - 3) and dest == self.FREE: # move one place forward and three places to the right or left
                return self.VALID
            elif new[0] == old[0] + 3 and (new[1] == old[1] + 1 or new[1] == old[1] - 1)  and dest == self.FREE: # move three places backwards and one place to the right or left
                return self.VALID
            elif new[0] == old[0] - 1 and (new[1] == old[1] + 3 or new[1] == old[1] - 3) and dest == self.FREE: # move one place backwards and three places to the right or left
                return self.VALID
            else:
                return self.INVALID
        if src.lower() == 'r': # rook
            if new[0] == old[0]: # same row
                if new[1] > old[1]:
                    for i in range(old[1], new[1]): # move right
                        if self.__board[old[0]][i] != self.FREE:
                            return self.INVALID
                else: # move left
                    for i in range(new[1], old[1], -1):
                        if self.__board[old[0]][i] != self.FREE:
                            return self.INVALID
            elif new[1] == old[1]: # same column
                if new[0] < old[0]: # move up
                    for i in range(new[0], old[0]): # move right
                        if self.__board[i][old[1]] != self.FREE:
                            return self.INVALID
                else: # move down
                    for i in range(old[0], new[0], -1):
                        if self.__board[i][old[1]] != self.FREE:
                            return self.INVALID
            else:
                return self.INVALID
            return self.VALID
        if src.lower() == 'a': # king
            if new[0] == old[0] - 1 and new[1] == old[1] and dest == self.FREE: # move one place forward into a free space
                return self.VALID
            elif new[0] == old[0] + 1 and new[1] == old[1] and dest == self.FREE: # move one place backward into a free space
                return self.VALID
            elif new[0] == old[0] and new[1] == old[1] - 1 and dest == self.FREE: # move one place left into a free space
                return self.VALID
            elif new[0] == old[0] and new[1] == old[1] + 1 and dest == self.FREE: # move one place right into a free space
                return self.VALID
            elif new[0] == old[0] - 1 and new[1] == old[1] - 1 and dest == self.FREE: # move one place forward left into a free space
                return self.VALID
            elif new[0] == old[0] - 1 and new[1] == old[1] + 1 and dest == self.FREE: # move one place forward right into a free space
                return self.VALID
            elif new[0] == old[0] + 1 and new[1] == old[1] - 1 and dest == self.FREE: # move one place backward left into a free space
                return self.VALID
            elif new[0] == old[0] + 1 and new[1] == old[1] + 1 and dest == self.FREE: # move one place backward right into a free space
                return self.VALID
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