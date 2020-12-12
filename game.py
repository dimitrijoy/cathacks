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
        self.__los = {self.BLACK: [(2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7)],
                      self.WHITE: [(5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7)]} # line of sight
        self.__turn = self.WHITE # white always goes first
    
    # returns piece at [row][col]
    def at(self, row, col):
        return self.__board[row][col]

    # moves a specified piece
    # returns True on success and False otherwise for the caller to handle
    def move(self, old, new):
        src, dest = self.__board[old[0]][old[1]], self.__board[new[0]][new[1]]
        src_color, dest_color = self.FREE, self.FREE
        if src.islower():
            src_color = self.BLACK
        elif src.isupper():
            src_color = self.WHITE
        if dest.islower():
            dest_color = self.BLACK
        elif dest.isupper():
            dest_color = self.WHITE

        if src != self.FREE: # moves allowed for pieces only
            if src_color == self.__turn and src_color != dest_color: # player is moving their own piece to a valid space
                if self.is_legal(old, new, src, dest): # move is legal in accordance with the game rules
                    self.__board[old[0]][old[1]] = self.FREE
                    self.__board[new[0]][new[1]] = src
                    self.update_los(old, new, src, dest) # updates spaces under attack
                    self.next()
                    return self.VALID # success!
            
        return self.INVALID # invalid move
    
    # determines if a particular move is possible in accordance with the game rules
    # primarily determines if the path of a move is allowed
    # unavoidably massive monster function
    def is_legal(self, old, new, src, dest):
        # pre-conditions
        if dest.upper() == 'A': # cannot move to the space with a king
            return self.INVALID
        if src.upper() == 'P': # pawn 
            if new[0] == old[0] - self.__turn and new[1] == old[1] and dest == self.FREE: # move one place forward into a free space
                return self.VALID
            elif new[0] == old[0] - self.__turn and (new[1] == old[1] + 1 or new[1] == old[1] - 1) and dest != self.FREE: # diagonal offensive move
                return self.VALID # determining the color of dest is not necessary, as this is handled in move()
            else:
                return self.INVALID
        if src.upper() == 'K': # knight
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
        if src.upper() == 'B': # bishop
            if abs(new[0] - old[0]) == abs(new[1] - old[1]): # same diagonal
                if new[0] < old[0] and new[1] > old[1]: # up and right
                    for i in range(1, old[0] - new[0]):
                        if self.__board[old[0]-i][old[1]+i] != self.FREE:
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
                        if self.__board[new[0]-i][new[1]+i] != self.FREE:
                            return self.INVALID
                return self.VALID
            else:
                return self.INVALID
        if src.upper() == 'R': # rook
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
        if src.upper() == 'Q': # queen
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
                        if self.__board[old[0]-i][old[1]+i] != self.FREE:
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
                        if self.__board[new[0]-i][new[1]+i] != self.FREE:
                            return self.INVALID
                return self.VALID
            else:
                return self.INVALID
            return self.VALID
        if src.upper() == 'A': # king
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
    
    # proceeds to the next turn
    # updates necessary attrs on turn change
    def next(self):
        self.__turn *= -1 # changes turns
    
    # updates spaces under attack
    def update_los(self, old, new, src, dest):
        pass