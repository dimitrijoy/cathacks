# dependencies
from board import Board
import copy, random

# plays against the human in chess
class AI:
    INF = 10 ** 3
    DEPTH = 1 # moves to look ahead into the future

    def __init__(self):
        self.__turns = 0
    
    # determines the next move of the ai
    def next_move(self, chess):
        self.__turns += 1
        if self.__turns == 1: # generic opener
            return ((1, 4), (3, 4))
        elif self.__turns == 2:
            return ((0, 1), (2, 2))
        elif self.__turns == 3:
            res = random.randrange(0, 2)
            if res == 0:
                return ((0, 6), (2, 5))
            else:
                return ((0, 5), (3, 2))

        best_score, next = -self.INF, None
        for i in range(chess.dimens()):
            for j in range(chess.dimens()):
                piece = chess.at(i, j)
                if piece != ' ' and piece.get_color() == chess.BLACK:
                    for k in piece.get_legal_moves():
                        dup = copy.deepcopy(chess)
                        if not dup.move((i,j), k):
                            continue # run away! (in check)
                        score = self.minimax(dup, self.DEPTH, -self.INF, self.INF, False)
                        del dup
                        if score > best_score:
                            best_score = score
                            next = ((i,j), k)
        return next
    
    # evaluates the score of a particular move
    # helps the ai decide if the move is worth making
    def minimax(self, chess, depth, alpha, beta, maximizing):
        # end condition
        if depth == 0:
            return -chess.evaluate()
        
        if maximizing: # maximizing player (ai)
            value = -self.INF
            for i in range(chess.dimens()):
                for j in range(chess.dimens()):
                    piece = chess.at(i, j)
                    if piece != ' ':
                        for k in piece.get_legal_moves():
                            dup = copy.deepcopy(chess); dup.move((i,j), k)
                            value = max(value, self.minimax(dup, depth - 1, alpha, beta, False))
                            del dup
                            alpha = max(alpha, value)
                            if alpha >= beta:
                                break # stop searching
            return value
        else: # minimizing player (human)
            value = self.INF
            for i in range(chess.dimens()):
                for j in range(chess.dimens()):
                    piece = chess.at(i, j)
                    if piece != ' ':
                        for k in piece.get_legal_moves():
                            dup = copy.deepcopy(chess); dup.move((i,j), k)
                            value = min(value, self.minimax(dup, depth - 1, alpha, beta, True))
                            del dup
                            beta = min(beta, value)
                            if beta <= alpha:
                                break # stop searching
            return value

# upholds the rules of chess on the board
# computes legality of moves
class Chess:
    BLACK, WHITE = -1, 1 # for managing turns
    ONGOING, FINISHED = 0, 1

    def __init__(self):
        self.__board = Board()
        self.__check = {self.BLACK: False, self.WHITE: False}
        self.__evaluation = 0
        self.__state = self.ONGOING
        self.__turn = self.WHITE # white always goes first
        self.__unmoved_pawns = [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7),
                                (6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7)] 
    
    # returns piece at [row][col]
    def at(self, row, col):
        return self.__board.at(row, col)
    
    # returns the current evaluation of the board
    def evaluate(self):
        return self.__evaluation
    
    # finds if someone is in check
    def in_check(self, color):
        for i in range(self.__board.DIMENS):
            for j in range(self.__board.DIMENS):
                if self.at(i, j) != self.__board.FREE:
                    piece = self.at(i, j)
                    for k in piece.get_legal_moves():
                        if self.at(k[0], k[1]) != self.__board.FREE and self.at(k[0], k[1]).get_type() == 'a':
                            return self.at(k[0], k[1]).get_color() == color
        return False
    
    # gets board dimens
    def dimens(self):
        return self.__board.DIMENS
    
    # generates all legal moves for every piece on the board
    def generate_legal_moves(self):
        for i in range(self.__board.DIMENS):
            for j in range(self.__board.DIMENS):
                if self.at(i, j) != self.__board.FREE:
                    piece, legal_moves = self.at(i, j), []
                    if piece.get_type() == 'p':
                        legal_moves = self.generate_pawn_moves(piece.get_color(), (i, j))
                    elif piece.get_type() == 'k':
                        legal_moves = self.generate_knight_moves(piece.get_color(), (i, j))
                    elif piece.get_type() == 'b':
                        legal_moves = self.generate_bishop_moves(piece.get_color(), (i, j))
                    elif piece.get_type() == 'r':
                        legal_moves = self.generate_rook_moves(piece.get_color(), (i, j))
                    elif piece.get_type() == 'q':
                        legal_moves = self.generate_queen_moves(piece.get_color(), (i, j))
                    else:
                        legal_moves = self.generate_king_moves(piece.get_color(), (i, j))
                    piece.update_legal_moves(legal_moves)
    
    # generates legal moves for a particular pawn
    def generate_pawn_moves(self, color, pos):
        legal_moves = []
        if pos[0]-self.__turn >= 0 and pos[0]-self.__turn < self.__board.DIMENS and self.at(pos[0]-self.__turn, pos[1]) == self.__board.FREE: # move one place forward into a free space
            legal_moves.append((pos[0]-self.__turn, pos[1]))
        if pos[0]-self.__turn >= 0 and pos[0]-self.__turn < self.__board.DIMENS and pos[1]-1 >= 0 and pos[1]-1 < self.__board.DIMENS and self.at(pos[0]-self.__turn, pos[1]-1) != self.__board.FREE and self.at(pos[0]-self.__turn, pos[1]-1).get_color() != color: # diagonal left offensive move
            legal_moves.append((pos[0]-self.__turn, pos[1]-1))
        if pos[0]-self.__turn >= 0 and pos[0]-self.__turn < self.__board.DIMENS and pos[1]+1 >= 0 and pos[1]+1 < self.__board.DIMENS and self.at(pos[0]-self.__turn, pos[1]+1) != self.__board.FREE and self.at(pos[0]-self.__turn, pos[1]+1).get_color() != color: # diagonal right offensive move
            legal_moves.append((pos[0]-self.__turn, pos[1]+1))
        return legal_moves

    # generates legal moves for a particular knight
    def generate_knight_moves(self, color, pos):
        legal_moves = []
        if pos[0]-2 >= 0 and pos[0]-2 < 8 and pos[1]-1 >= 0 and pos[1]-1 < 8 and (self.at(pos[0]-2, pos[1]-1) == self.__board.FREE or self.at(pos[0]-2, pos[1]-1).get_color() != color): # up and left
            legal_moves.append((pos[0]-2, pos[1]-1))
        if pos[0]-2 >= 0 and pos[0]-2 < 8 and pos[1]+1 >= 0 and pos[1]+1 < 8 and (self.at(pos[0]-2, pos[1]+1) == self.__board.FREE or self.at(pos[0]-2, pos[1]+1).get_color() != color): # up and right
            legal_moves.append((pos[0]-2, pos[1]+1))
        if pos[0]+2 >= 0 and pos[0]+2 < 8 and pos[1]-1 >= 0 and pos[1]-1 < 8 and (self.at(pos[0]+2, pos[1]-1) == self.__board.FREE or self.at(pos[0]+2, pos[1]-1).get_color() != color): # down and left
            legal_moves.append((pos[0]+2, pos[1]-1))
        if pos[0]+2 >= 0 and pos[0]+2 < 8 and pos[1]+1 >= 0 and pos[1]+1 < 8 and (self.at(pos[0]+2, pos[1]+1) == self.__board.FREE or self.at(pos[0]+2, pos[1]+1).get_color() != color): # down and right
            legal_moves.append((pos[0]+2, pos[1]+1))
        if pos[0]-1 >= 0 and pos[0]-1 < 8 and pos[1]-2 >= 0 and pos[1]-2 < 8 and (self.at(pos[0]-1, pos[1]-2) == self.__board.FREE or self.at(pos[0]-1, pos[1]-2).get_color() != color): # left and up
            legal_moves.append((pos[0]-1, pos[1]-2))
        if pos[0]+1 >= 0 and pos[0]+1 < 8 and pos[1]-2 >= 0 and pos[1]-2 < 8 and (self.at(pos[0]+1, pos[1]-2) == self.__board.FREE or self.at(pos[0]+1, pos[1]-2).get_color() != color): # left and down
            legal_moves.append((pos[0]+1, pos[1]-2))
        if pos[0]-1 >= 0 and pos[0]-1 < 8 and pos[1]+2 >= 0 and pos[1]+2 < 8 and (self.at(pos[0]-1, pos[1]+2) == self.__board.FREE or self.at(pos[0]-1, pos[1]+2).get_color() != color): # right and up
            legal_moves.append((pos[0]-1, pos[1]+2))
        if pos[0]+1 >= 0 and pos[0]+1 < 8 and pos[1]+2 >= 0 and pos[1]+2 < 8 and (self.at(pos[0]+1, pos[1]+2) == self.__board.FREE or self.at(pos[0]+1, pos[1]+2).get_color() != color): # right and down
            legal_moves.append((pos[0]+1, pos[1]+2))
        return legal_moves

    # generates legal moves for a particular bishop
    def generate_bishop_moves(self, color, pos):
        legal_moves = []
        for i in range(1, self.__board.DIMENS): # up and right
            if pos[0]-i >= 0 and pos[0]-i < self.__board.DIMENS and pos[1]+i >= 0 and pos[1]+i < self.__board.DIMENS:
                piece = self.at(pos[0]-i, pos[1]+i) 
                if piece != self.__board.FREE: # not a free space
                    if color != piece.get_color(): # opponent's piece
                        legal_moves.append((pos[0]-i, pos[1]+i))
                    break
                legal_moves.append((pos[0]-i, pos[1]+i))
            else:
                break
        for i in range(1, self.__board.DIMENS): # up and left
            if pos[0]-i >= 0 and pos[0]-i < self.__board.DIMENS and pos[1]-i >= 0 and pos[1]-i < self.__board.DIMENS:
                piece = self.at(pos[0]-i, pos[1]-i) 
                if piece != self.__board.FREE: # not a free space
                    if color != piece.get_color(): # opponent's piece
                        legal_moves.append((pos[0]-i, pos[1]-i))
                    break
                legal_moves.append((pos[0]-i, pos[1]-i))
            else:
                break
        for i in range(1, self.__board.DIMENS): # down and right
            if pos[0]+i >= 0 and pos[0]+i < self.__board.DIMENS and pos[1]+i >= 0 and pos[1]+i < self.__board.DIMENS:
                piece = self.at(pos[0]+i, pos[1]+i) 
                if piece != self.__board.FREE: # not a free space
                    if color != piece.get_color(): # opponent's piece
                        legal_moves.append((pos[0]+i, pos[1]+i))
                    break
                legal_moves.append((pos[0]+i, pos[1]+i))
            else:
                break
        for i in range(1, self.__board.DIMENS): # down and left
            if pos[0]+i >= 0 and pos[0]+i < self.__board.DIMENS and pos[1]-i >= 0 and pos[1]-i < self.__board.DIMENS:
                piece = self.at(pos[0]+i, pos[1]-i) 
                if piece != self.__board.FREE: # not a free space
                    if color != piece.get_color(): # opponent's piece
                        legal_moves.append((pos[0]+i, pos[1]-i))
                    break
                legal_moves.append((pos[0]+i, pos[1]-i))
            else:
                break
        return legal_moves
    
    # generates legal moves for a particular knight
    def generate_rook_moves(self, color, pos):
        legal_moves= []
        for i in range(1, self.__board.DIMENS): # move up
            if pos[0]-i >= 0 and pos[0]-i <= self.__board.DIMENS:
                piece = self.at(pos[0]-i, pos[1])
                if piece != self.__board.FREE:
                    if color != piece.get_color():
                        legal_moves.append((pos[0]-i, pos[1]))
                    break
                legal_moves.append((pos[0]-i, pos[1]))
        for i in range(1, self.__board.DIMENS): # move down
            if pos[0]+i >= 0 and pos[0]+i < self.__board.DIMENS:
                piece = self.at(pos[0]+i, pos[1])
                if piece != self.__board.FREE:
                    if color != piece.get_color():
                        legal_moves.append((pos[0]+i, pos[1]))
                    break
                legal_moves.append((pos[0]+i, pos[1]))
        for i in range(1, self.__board.DIMENS): # move right
            if pos[1]+i >= 0 and pos[1]+i < self.__board.DIMENS:
                piece = self.at(pos[0], pos[1]+i)
                if piece != self.__board.FREE:
                    if color != piece.get_color():
                        legal_moves.append((pos[0], pos[1]+i))
                    break
                legal_moves.append((pos[0], pos[1]+i))
        for i in range(1, self.__board.DIMENS): # move left
            if pos[1]-i >= 0 and pos[1]-i < self.__board.DIMENS:
                piece = self.at(pos[0], pos[1]-i)
                if piece != self.__board.FREE:
                    if color != piece.get_color():
                        legal_moves.append((pos[0], pos[1]-i))
                    break
                legal_moves.append((pos[0], pos[1]-i))
        return legal_moves
  
    # generates legal moves for a particular queen
    def generate_queen_moves(self, color, pos):
        legal_moves = []
        # vertical/horizontal
        for i in range(1, self.__board.DIMENS): # move up
            if pos[0]-i >= 0 and pos[0]-i <= self.__board.DIMENS:
                piece = self.at(pos[0]-i, pos[1])
                if piece != self.__board.FREE:
                    if color != piece.get_color():
                        legal_moves.append((pos[0]-i, pos[1]))
                    break
                legal_moves.append((pos[0]-i, pos[1]))
        for i in range(1, self.__board.DIMENS): # move down
            if pos[0]+i >= 0 and pos[0]+i < self.__board.DIMENS:
                piece = self.at(pos[0]+i, pos[1])
                if piece != self.__board.FREE:
                    if color != piece.get_color():
                        legal_moves.append((pos[0]+i, pos[1]))
                    break
                legal_moves.append((pos[0]+i, pos[1]))
        for i in range(1, self.__board.DIMENS): # move right
            if pos[1]+i >= 0 and pos[1]+i < self.__board.DIMENS:
                piece = self.at(pos[0], pos[1]+i)
                if piece != self.__board.FREE:
                    if color != piece.get_color():
                        legal_moves.append((pos[0], pos[1]+i))
                    break
                legal_moves.append((pos[0], pos[1]+i))
        for i in range(1, self.__board.DIMENS): # move left
            if pos[1]-i >= 0 and pos[1]-i < self.__board.DIMENS:
                piece = self.at(pos[0], pos[1]-i)
                if piece != self.__board.FREE:
                    if color != piece.get_color():
                        legal_moves.append((pos[0], pos[1]-i))
                    break
                legal_moves.append((pos[0], pos[1]-i))
        # diagonal
        for i in range(1, self.__board.DIMENS): # up and right
            if pos[0]-i >= 0 and pos[0]-i < self.__board.DIMENS and pos[1]+i >= 0 and pos[1]+i < self.__board.DIMENS:
                piece = self.at(pos[0]-i, pos[1]+i) 
                if piece != self.__board.FREE: # not a free space
                    if color != piece.get_color(): # opponent's piece
                        legal_moves.append((pos[0]-i, pos[1]+i))
                    break
                legal_moves.append((pos[0]-i, pos[1]+i))
            else:
                break
        for i in range(1, self.__board.DIMENS): # up and left
            if pos[0]-i >= 0 and pos[0]-i < self.__board.DIMENS and pos[1]-i >= 0 and pos[1]-i < self.__board.DIMENS:
                piece = self.at(pos[0]-i, pos[1]-i) 
                if piece != self.__board.FREE: # not a free space
                    if color != piece.get_color(): # opponent's piece
                        legal_moves.append((pos[0]-i, pos[1]-i))
                    break
                legal_moves.append((pos[0]-i, pos[1]-i))
            else:
                break
        for i in range(1, self.__board.DIMENS): # down and right
            if pos[0]+i >= 0 and pos[0]+i < self.__board.DIMENS and pos[1]+i >= 0 and pos[1]+i < self.__board.DIMENS:
                piece = self.at(pos[0]+i, pos[1]+i) 
                if piece != self.__board.FREE: # not a free space
                    if color != piece.get_color(): # opponent's piece
                        legal_moves.append((pos[0]+i, pos[1]+i))
                    break
                legal_moves.append((pos[0]+i, pos[1]+i))
            else:
                break
        for i in range(1, self.__board.DIMENS): # down and left
            if pos[0]+i >= 0 and pos[0]+i < self.__board.DIMENS and pos[1]-i >= 0 and pos[1]-i < self.__board.DIMENS:
                piece = self.at(pos[0]+i, pos[1]-i) 
                if piece != self.__board.FREE: # not a free space
                    if color != piece.get_color(): # opponent's piece
                        legal_moves.append((pos[0]+i, pos[1]-i))
                    break
                legal_moves.append((pos[0]+i, pos[1]-i))
            else:
                break
        return legal_moves

    # generates legal moves for a particular king
    def generate_king_moves(self, color, pos):
        legal_moves = []
        if pos[0]-1 >= 0 and pos[0]-1 < self.__board.DIMENS and (self.at(pos[0]-1, pos[1]) == self.__board.FREE or self.at(pos[0]-1, pos[1]).get_color() != color): # move one place forward
            legal_moves.append((pos[0]-1, pos[1]))
        if pos[0]+1 >= 0 and pos[0]+1 < self.__board.DIMENS and (self.at(pos[0]+1, pos[1]) == self.__board.FREE or self.at(pos[0]+1, pos[1]).get_color() != color): # move one place backward
            legal_moves.append((pos[0]+1, pos[1]))
        if pos[1]-1 >= 0 and pos[1]-1 < self.__board.DIMENS and (self.at(pos[0], pos[1]-1) == self.__board.FREE or self.at(pos[0], pos[1]-1).get_color() != color): # move one place left
            legal_moves.append((pos[0], pos[1]-1))
        if pos[1]+1 >= 0 and pos[1]+1 < self.__board.DIMENS and (self.at(pos[0], pos[1]+1) == self.__board.FREE or self.at(pos[0], pos[1]+1).get_color() != color): # move one place right
            legal_moves.append((pos[0], pos[1]+1))
        if pos[0]-1 >= 0 and pos[0]-1 < self.__board.DIMENS and pos[1]+1 >= 0 and pos[1]+1 < self.__board.DIMENS and (self.at(pos[0]-1, pos[1]+1) == self.__board.FREE or self.at(pos[0]-1, pos[1]+1).get_color() != color): # move one place up and right
            legal_moves.append((pos[0]-1, pos[1]+1))
        if pos[0]-1 >= 0 and pos[0]-1 < self.__board.DIMENS and pos[1]-1 >= 0 and pos[1]-1 < self.__board.DIMENS and (self.at(pos[0]-1, pos[1]-1) == self.__board.FREE or self.at(pos[0]-1, pos[1]-1).get_color() != color): # move one place up and left
            legal_moves.append((pos[0]-1, pos[1]-1))
        if pos[0]+1 >= 0 and pos[0]+1 < self.__board.DIMENS and pos[1]+1 >= 0 and pos[1]+1 < self.__board.DIMENS and (self.at(pos[0]+1, pos[1]+1) == self.__board.FREE or self.at(pos[0]+1, pos[1]+1).get_color() != color): # move one place down and right
            legal_moves.append((pos[0]+1, pos[1]+1))
        if pos[0]+1 >= 0 and pos[0]+1 < self.__board.DIMENS and pos[1]-1 >= 0 and pos[1]-1 < self.__board.DIMENS and (self.at(pos[0]+1, pos[1]-1) == self.__board.FREE or self.at(pos[0]+1, pos[1]-1).get_color() != color): # move one place down and left
            legal_moves.append((pos[0]+1, pos[1]-1))
        return legal_moves

    # moves a specified piece
    # returns True on success and False otherwise for the caller to handle
    def move(self, old, new):
        if self.__state == self.ONGOING:
            src, dest = self.__board.at(old[0], old[1]), self.__board.at(new[0], new[1])
            if src != self.__board.FREE: # not a free space
                src_color, dest_color = src.get_color(), self.__board.FREE if dest == self.__board.FREE else dest.get_color()
                if src_color == self.__turn and src_color != dest_color and new in src.get_legal_moves(): # player is moving their own piece to a valid space
                    # assume the move is legal until check
                    self.__board.move(old, new)
                    self.next()
                    self.generate_legal_moves()

                    # fails in check
                    if self.in_check(src_color):
                        # reverts the move
                        self.__board.move(new, old)
                        self.__board.place(dest, new[0], new[1])
                        self.next()
                        self.generate_legal_moves()
                        return False # does not stop check
                    
                    # updates the game evaluation
                    mid_bonus = 20 if new[0] >= 2 and new[0] <= 5 and new[1] >= 2 and new[1] <= 5 else 0
                    if dest_color == self.WHITE:
                        self.__evaluation -= dest.get_score() + mid_bonus
                    elif dest_color == self.BLACK:
                        self.__evaluation += dest.get_score() + mid_bonus
                    
                    return True # success!
                else: # need to account for pawn's first move
                    if src.get_type() == 'p' and old in self.__unmoved_pawns:
                        if new[0] == old[0]-2*self.__turn and new[1] == old[1] and dest == self.__board.FREE:
                            self.__board.move(old, new)
                            self.next()
                            self.generate_legal_moves()
                            return True # success!
                    return False # not a pawn's first move
            else:
                return False # invalid 
        return False
    # next turn
    def next(self):
        self.__turn *= -1 # changes turns
    
    # places a piece
    def place(self, piece, i, j):
        self.__board.place(piece, i, j)
    
    # starts the game
    def start(self):
        self.generate_legal_moves() # initial legal moves
    
    # stops the game
    def stop(self):
        self.__state = self.FINISHED
    
    # returns the turn
    def turn(self):
        return self.__turn