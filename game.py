# plays against the human player
class AI:
    def move(self, board):
        for i in range(board.DIMENS):
            for j in range(board.DIMENS):
                if board.at(i, j) == 'p': # black piece
                    if board.move((i, j), (i+1, j)):
                        break

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
    # unavoidably massive monster function
    def is_available(self, old, new, src, dest):
        if self.in_check(): # do not proceed if in check
            return self.INVALID
        if src == 'P': # pawn 
            if new[0] == old[0] - 1 and new[1] == old[1] and dest == self.FREE: # move one place forward into a free space
                return self.VALID
            elif new[0] == old[0] - 1 and (new[1] == old[1] + 1 or new[1] == old[1] - 1) and dest != self.FREE: # diagonal offensive move
                return self.VALID # determining the color of dest is not necessary, as this is handled in move()
            else:
                return self.INVALID
        if src == 'K': # knight
            if new[0] == old[0] - 2 and (new[1] == old[1] + 1 or new[1] == old[1] - 1): # move three places forward and one place to the right or left
                return self.VALID
            elif new[0] == old[0] + 1 and (new[1] == old[1] + 2 or new[1] == old[1] - 2): # move one place forward and three places to the right or left
                return self.VALID
            elif new[0] == old[0] + 2 and (new[1] == old[1] + 1 or new[1] == old[1] - 1): # move three places backwards and one place to the right or left
                return self.VALID
            elif new[0] == old[0] - 1 and (new[1] == old[1] + 2 or new[1] == old[1] - 2): # move one place backwards and three places to the right or left
                return self.VALID
            else:
                return self.INVALID
        if src == 'B': # bishop
            if abs(new[0] - old[0]) == abs(new[1] - old[1]): # same diagonal
                if new[0] < old[0] and new[1] > old[1]: # up and right 
                    for i in range(1, old[0] - new[0]):
                        if self.__board[new[0]+i][old[1]+i] != self.FREE:
                            return self.INVALID
                elif new[0] < old[0] and new[1] < old[1]: # up and left
                    for i in range(1, old[0] - new[0]):
                        if self.__board[new[0]+i][new[1]+i] != self.FREE:
                            return self.INVALID
                elif new[0] > old[0] and new[1] > old[1]: # down and right
                    for i in range(1, new[0] - old[0]):
                        if self.__board[old[0]+i][old[1]+i] != self.FREE:
                            return self.INVALID
                else: # down and left
                    for i in range(1, new[0] - old[0]):
                        if self.__board[old[0]+i][new[1]+i] != self.FREE:
                            return self.INVALID
                return self.VALID
            else:
                return self.INVALID
        if src == 'R': # rook
            if new[0] == old[0]: # same row
                if new[1] > old[1]:
                    for i in range(old[1]+1, new[1]):
                        if self.__board[old[0]][i] != self.FREE:
                            return self.INVALID
                else: # move left
                    for i in range(old[1]-1, new[1], -1):
                        if self.__board[old[0]][i] != self.FREE:
                            return self.INVALID
            elif new[1] == old[1]: # same column
                if new[0] > old[0]: # move down
                    for i in range(old[0]+1, new[0]):
                        if self.__board[i][old[1]] != self.FREE:
                            return self.INVALID
                else: # move up
                    for i in range(old[0]-1, new[0], -1):
                        if self.__board[i][old[1]] != self.FREE:
                            return self.INVALID
            else:
                return self.INVALID
            return self.VALID
        if src == 'Q': # queen
            # combines rook and biship movement
            if new[0] == old[0]: # same row
                if new[1] > old[1]:
                    for i in range(old[1]+1, new[1]):
                        if self.__board[old[0]][i] != self.FREE:
                            return self.INVALID
                else: # move left
                    for i in range(old[1]-1, new[1], -1):
                        if self.__board[old[0]][i] != self.FREE:
                            return self.INVALID
            elif new[1] == old[1]: # same column
                if new[0] > old[0]: # move down
                    for i in range(old[0]+1, new[0]):
                        if self.__board[i][old[1]] != self.FREE:
                            return self.INVALID
                else: # move up
                    for i in range(old[0]-1, new[0], -1):
                        if self.__board[i][old[1]] != self.FREE:
                            return self.INVALID
            elif abs(new[0] - old[0]) == abs(new[1] - old[1]): # same diagonal
                if new[0] < old[0] and new[1] > old[1]: # up and right 
                    for i in range(1, old[0] - new[0]):
                        if self.__board[new[0]+i][old[1]+i] != self.FREE:
                            return self.INVALID
                elif new[0] < old[0] and new[1] < old[1]: # up and left
                    for i in range(1, old[0] - new[0]):
                        if self.__board[new[0]+i][new[1]+i] != self.FREE:
                            return self.INVALID
                elif new[0] > old[0] and new[1] > old[1]: # down and right
                    for i in range(1, new[0] - old[0]):
                        if self.__board[old[0]+i][old[1]+i] != self.FREE:
                            return self.INVALID
                else: # down and left
                    for i in range(1, new[0] - old[0]):
                        if self.__board[old[0]+i][new[1]+i] != self.FREE:
                            return self.INVALID
                return self.VALID
            else:
                return self.INVALID
            return self.VALID
        if src == 'A': # king
            if new[0] == old[0] - 1 and new[1] == old[1]: # move one place forward
                return self.VALID
            elif new[0] == old[0] + 1 and new[1] == old[1]: # move one place backward
                return self.VALID
            elif new[0] == old[0] and new[1] == old[1] - 1: # move one place left
                return self.VALID
            elif new[0] == old[0] and new[1] == old[1] + 1: # move one place right
                return self.VALID
            elif new[0] == old[0] - 1 and new[1] == old[1] - 1: # move one place forward left
                return self.VALID
            elif new[0] == old[0] - 1 and new[1] == old[1] + 1: # move one place forward right
                return self.VALID
            elif new[0] == old[0] + 1 and new[1] == old[1] - 1: # move one place backward left
                return self.VALID
            elif new[0] == old[0] + 1 and new[1] == old[1] + 1: # move one place backward right
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
                if dest.lower() != 'a' and self.is_available(old, new, src, dest): # move is available and is not to a king
                    self.__board[old[0]][old[1]] = self.FREE
                    self.__board[new[0]][new[1]] = src
                    self.__turn *= -1 # changes turns
                    return self.VALID # success!
            
        return self.INVALID # invalid move