# dependencies
import chess

# maintains the position of the pieces on the board
class Board:
    # constants
    DIMENS = 8 # board dimensM
    FREE = " " # free space
    INVALID, VALID = False, True # regarding moves

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
    
    # returns piece at [row][col]
    def at(self, row, col):
        return self.__board[row][col]

    # moves a specified piece
    # returns True on success and False otherwise for the caller to handle
    def move(self, old, new):
        temp = self.__board[old[0]][old[1]]
        self.__board[old[0]][old[1]] = self.FREE
        self.__board[new[0]][new[1]] = temp
    
    # puts a piece at [row][col]
    def place(self, piece, row, col):
        self.__board[row][col] = piece

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
        super().__init__(color, 60, 'a')