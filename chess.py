from board import Board

# upholds the rules of chess on the board
# computes legality of moves
class Chess:
    BLACK, WHITE = -1, 1 # for managing turns

    def __init__(self):
        self.__board = Board()
        self.__legal_moves = None
        self.__turn = self.WHITE # white always goes first

    def move(self, old, new):
        src, dest = self.__board.at(old[0], old[1]), self.__board.at(new[0], new[1])
        # determines if src/dest is free or occupied by black/white
        src_color, dest_color = self.__board.FREE, self.__board.FREE
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
                    print(self.__los)
                    self.next()

# generic piece in a game of chess
class Piece:
    def __init__(self, color, score):
        self.__color = color
        self.__score = score
        self.__legal_moves = []

SCORES = {'p': 10, 'k': 30, 'b': 30, 'r': 50, 'q': 90, 'a': 900}

# inherits properties of Piece
class Pawn(Piece):
    def __init__(self, color, score):
        super().__init__(color, 'p', score)
    
    def is_legal(self, old, new, src, dest):
        # pre-conditions
        if dest.upper() == 'A': # cannot move to the space with a king
            return self.INVALID
        if src.upper() == 'P': # pawn 
            if new[0] == old[0] - self.__turn and new[1] == old[1] and dest == self.FREE: # move one place forward into a free space
                return self.VALID
            elif new[0] == old[0] - self.__turn and (new[1] == old[1] + 1 or new[1] == old[1] - 1) and dest != self.FREE: # diagonal offensive move
                return self.VALID # determining the color of dest is not necessary, as this is handled in move()
            elif old in self.__unmoved_pawns and new[0] == old[0] - 2*self.__turn and new[1] == old[1] and dest == self.FREE and self.__board[old[0] - self.__turn][new[1]] == self.FREE:
                self.__unmoved_pawns.remove(old)
                return self.VALID # move two places forward on first move of pawn
            else:
                return self.INVALID

class Rook(Piece):
    def __init__(self, color, score):
        super().__init__(color, 'r' ,score)

    def is_legal(self, old, new, src, dest):
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

class Knight(Piece):
    def __init__(self, color, score):
        super().__init__(color, 'k' ,score)

    def is_legal(self, old, new, src, dest):
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

class Bishop(Piece):
    def __init__(self, color, score):
        super().__init__(color, 'b' ,score)

    def is_legal(self, old, new, src, dest):
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

class Queen(Piece):
    def __init__(self, color, score):
        super().__init__(color, 'q' ,score)

    def is_legal(self, old, new, src, dest):
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

class King(Piece):
    def __init__(self, color, score):
        super().__init__(color, 'a' ,score)
    
    def is_legal(self, old, new, src, dest):
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
