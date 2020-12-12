from board import Board

# upholds the rules of chess on the board
# computes legality of moves
class Chess:
    BLACK, WHITE = -1, 1 # for managing turns

    def __init__(self):
        self.__board = Board()
        self.__turn = self.WHITE # white always goes first
    
    # returns piece at [row][col]
    def at(self, row, col):
        return self.__board.at(row, col)
    
    def generate_legal_moves(self):
        for i in range(self.__board.DIMENS):
            for j in range(self.__board.DIMENS):


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
                    self.__board.move(old, new)
                    self.next() # next turn
        
    # next turn
    def next(self):
        self.__turn *= -1 # changes turns

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
        super().__init__(color, 10,  'p')

# inherits properties of Piece
class Knight(Piece):
    def __init__(self, color):
        super().__init__(color, 'k', 30)

# inherits properties of Piece
class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color, 'b', 30)

# inherits properties of Piece
class Rook(Piece):
    def __init__(self, color):
        super().__init__(color, 'r', 50)

# inherits properties of Piece
class Queen(Piece):
    def __init__(self, color):
        super().__init__(color, 'q', 90)

# inherits properties of Piece
class King(Piece):
    def __init__(self, color):
        super().__init__(color, 'a', 900)