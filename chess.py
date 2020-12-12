from board import Board

# upholds the rules of chess on the board
# computes legality of moves
class Chess:
    BLACK, WHITE = -1, 1 # for managing turns

    def __init__(self):
        self.__board = Board()
        self.__legal_moves = None
        self.__turn = self.WHITE # white always goes first
    
    def generate_legal_moves(self):
        for 

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
    def __init__(self, color, type, score):
        self.__color = color
        self.__type = type
        self.__score = score
        self.__legal_moves = []
    
    # gets legal moves
    def get_legal_moves(self):
        return self.__legal_moves
    
    # gets the type of piece
    def get_type(self):
        return self.__type
    
    # updates legal moves in accordance with the game rules
    def update_legal_moves(self, legal_moves):
        self.__legal_moves = legal_moves

# inherits properties of Piece
class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color, 'p', 10)