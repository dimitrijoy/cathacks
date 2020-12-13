import chess

# maintains the position of the pieces on the board
class Board:
    # constants
    DIMENS = 8 # board dimensM
    FREE = " " # free space
    INVALID, VALID = False, True # regarding moves
    SCORES = {'p': 10, 'k': 30, 'b': 30, 'r': 50, 'q': 90, 'a': 900}

    def __init__(self):
        # lowercase corresponds to black and uppercase to white
        self.__board = [[Rook(chess.Chess.BLACK), Knight(chess.Chess.BLACK), Bishop(chess.Chess.BLACK), Queen(chess.Chess.BLACK), King(chess.Chess.BLACK), Bishop(chess.Chess.BLACK), Knight(chess.Chess.BLACK), Rook(chess.Chess.BLACK)],
                        [Pawn(chess.Chess.BLACK), Pawn(chess.Chess.BLACK), Pawn(chess.Chess.BLACK), Pawn(chess.Chess.BLACK), Pawn(chess.Chess.BLACK), Pawn(chess.Chess.BLACK), Pawn(chess.Chess.BLACK), Pawn(chess.Chess.BLACK)],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [Pawn(chess.Chess.WHITE), Pawn(chess.Chess.WHITE), Pawn(chess.Chess.WHITE), Pawn(chess.Chess.WHITE), Pawn(chess.Chess.WHITE), Pawn(chess.Chess.WHITE), Pawn(chess.Chess.WHITE), Pawn(chess.Chess.WHITE)],
                        [Rook(chess.Chess.WHITE), Knight(chess.Chess.WHITE), Bishop(chess.Chess.WHITE), Queen(chess.Chess.WHITE), King(chess.Chess.WHITE), Bishop(chess.Chess.WHITE), Knight(chess.Chess.WHITE), Rook(chess.Chess.WHITE)]]
        self.__unmoved_pawns = [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7),
                                (6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7)] 
    
    # returns piece at [row][col]
    def at(self, row, col):
        return self.__board[row][col]

    # moves a specified piece
    # returns True on success and False otherwise for the caller to handle
    def move(self, old, new):
        temp = self.__board[old[0]][old[1]]
        self.__board[old[0]][old[1]] = self.FREE
        self.__board[new[0]][new[1]] = temp
    
    # determines if a particular move is possible in accordance with the game rules and if the path of a move is allowed
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
            elif old in self.__unmoved_pawns and new[0] == old[0] - 2*self.__turn and new[1] == old[1] and dest == self.FREE and self.__board[old[0] - self.__turn][new[1]] == self.FREE:
                self.__unmoved_pawns.remove(old)
                return self.VALID # move two places forward on first move of pawn
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

# generic piece in a game of chess
class Piece:
    def __init__(self, color, score, type):
        self.__color = color
        self.__type = type
        self.__score = score
        self.__legal_moves = []
    
    # gets color of piece
    def get_color(self):
        return self.__color
    
    # gets legal moves
    def get_legal_moves(self):
        return self.__legal_moves
    
    # gets score
    def get_score(self):
        return self.__score
    
    # gets the type of piece
    def get_type(self):
        return self.__type
    
    # updates legal moves in accordance with the game rules
    def update_legal_moves(self, legal_moves):
        self.__legal_moves = legal_moves

# inherits properties of Piece
class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color, 10, 'p')

# inherits properties of Piece
class Knight(Piece):
    def __init__(self, color):
        super().__init__(color, 30, 'k')

# inherits properties of Piece
class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color, 30, 'b')

# inherits properties of Piece
class Rook(Piece):
    def __init__(self, color):
        super().__init__(color, 50, 'r')

# inherits properties of Piece
class Queen(Piece):
    def __init__(self, color):
        super().__init__(color, 90, 'q')

# inherits properties of Piece
class King(Piece):
    def __init__(self, color):
        super().__init__(color, 900, 'a')