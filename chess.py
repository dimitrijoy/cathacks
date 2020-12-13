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
    
    # gets board dimens
    def dimens(self):
        return self.__board.DIMENS
    
    # generates all legal moves for every piece on the board
    def generate_legal_moves(self):
        for i in range(self.__board.DIMENS):
            for j in range(self.__board.DIMENS):
                if self.at(i, j) != self.__board.FREE:
                    piece, legal_moves = self.at(i, j), []
                    if piece.get_type() == 'k':
                        legal_moves = self.generate_knight_moves(piece.get_color(), (i, j))
                    elif piece.get_type() == 'b':
                        legal_moves = self.generate_bishop_moves(piece.get_color(), (i, j))
                    elif piece.get_type() == 'r':
                        legal_moves = self.generate_rook_moves(piece.get_color(), (i, j))
                    elif piece.get_type() == 'q':
                        legal_moves = self.generate_queen_moves(piece.get_color(), (i, j))
                    piece.update_legal_moves(legal_moves)
    
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
            if pos[0]-i >= 0 and pos[0]-i <= self.__board.DIMENS:
                piece = self.at(pos[0]+i, pos[1])
                if piece != self.__board.FREE:
                    if color != piece.get_color():
                        legal_moves.append((pos[0]+i, pos[1]))
                    break
                legal_moves.append((pos[0]+i, pos[1]))
        for i in range(1, self.__board.DIMENS): # move right
            if pos[0]-i >= 0 and pos[0]+i <= self.__board.DIMENS:
                piece = self.at(pos[0], pos[1]+i)
                if piece != self.__board.FREE:
                    if color != piece.get_color():
                        legal_moves.append((pos[0], pos[1]+i))
                    break
                legal_moves.append((pos[0], pos[1]+i))
        for i in range(1, self.__board.DIMENS): # move left
            if pos[0]-i >= 0 and pos[0]+i <= self.__board.DIMENS:
                piece = self.at(pos[0], pos[1]-i)
                if piece != self.__board.FREE:
                    if color != piece.get_color():
                        legal_moves.append((pos[0], pos[1]-i))
                    break
                legal_moves.append((pos[0], pos[1]-i))
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
            break
        for i in range(1, self.__board.DIMENS): # up and left
            if pos[0]-i >= 0 and pos[0]-i < self.__board.DIMENS and pos[1]-i >= 0 and pos[1]-i < self.__board.DIMENS:
                piece = self.at(pos[0]-i, pos[1]-i) 
                if piece != self.__board.FREE: # not a free space
                    if color != piece.get_color(): # opponent's piece
                        legal_moves.append((pos[0]-i, pos[1]-i))
                    break
                legal_moves.append((pos[0]-i, pos[1]-i))
            break
        for i in range(1, self.__board.DIMENS): # down and right
            if pos[0]+i >= 0 and pos[0]+i < self.__board.DIMENS and pos[1]+i >= 0 and pos[1]+i < self.__board.DIMENS:
                piece = self.at(pos[0]+i, pos[1]+i) 
                if piece != self.__board.FREE: # not a free space
                    if color != piece.get_color(): # opponent's piece
                        legal_moves.append((pos[0]+i, pos[1]+i))
                    break
                legal_moves.append((pos[0]+i, pos[1]+i))
            break
        for i in range(1, self.__board.DIMENS): # down and left
                if pos[0]+i >= 0 and pos[0]+i < self.__board.DIMENS and pos[1]-i >= 0 and pos[1]-i < self.__board.DIMENS:
                    piece = self.at(pos[0]+i, pos[1]-i) 
                    if piece != self.__board.FREE: # not a free space
                        if color != piece.get_color(): # opponent's piece
                            legal_moves.append((pos[0]+i, pos[1]-i))
                        break
                    legal_moves.append((pos[0]+i, pos[1]-i))
                break
        return legal_moves

    # generates legal moves for a particular queen
    def generate_queen_moves(self, color, pos):
        legal_moves = []
        # vertical/horizontal
        for i in range(1, self.__board.DIMENS): # move up
            if pos[0]-i >= 0 and pos[0]-i <= self.__board.DIMENS:
                piece = self.at(pos[0]-i, pos[1])
                if piece != self.__board.FREE: # not a free space
                    if color != piece.get_color(): # opponent's piece
                        legal_moves.append((pos[0]-i, pos[1]))
                    break
                legal_moves.append((pos[0]-i, pos[1]))
        for i in range(1, self.__board.DIMENS): # move down
            if pos[0]-i >= 0 and pos[0]-i <= self.__board.DIMENS:
                piece = self.at(pos[0]+i, pos[1])
                if piece != self.__board.FREE: # not a free space
                    if color != piece.get_color(): # opponent's piece
                        legal_moves.append((pos[0]+i, pos[1]))
                    break
                legal_moves.append((pos[0]+i, pos[1]))
        for i in range(1, self.__board.DIMENS): # move right
            if pos[0]-i >= 0 and pos[0]+i <= self.__board.DIMENS:
                piece = self.at(pos[0], pos[1]+i)
                if piece != self.__board.FREE: # not a free space
                    if color != piece.get_color(): # opponent's piece
                        legal_moves.append((pos[0], pos[1]+i))
                    break
                legal_moves.append((pos[0], pos[1]+i))
        for i in range(1, self.__board.DIMENS): # move left
            if pos[0]-i >= 0 and pos[0]+i <= self.__board.DIMENS:
                piece = self.at(pos[0], pos[1]-i)
                if piece != self.__board.FREE: # not a free space
                    if color != piece.get_color(): # opponent's piece
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
            break
        for i in range(1, self.__board.DIMENS): # up and left
            if pos[0]-i >= 0 and pos[0]-i < self.__board.DIMENS and pos[1]-i >= 0 and pos[1]-i < self.__board.DIMENS:
                piece = self.at(pos[0]-i, pos[1]-i) 
                if piece != self.__board.FREE: # not a free space
                    if color != piece.get_color(): # opponent's piece
                        legal_moves.append((pos[0]-i, pos[1]-i))
                    break
                legal_moves.append((pos[0]-i, pos[1]-i))
            break
        for i in range(1, self.__board.DIMENS): # down and right
            if pos[0]+i >= 0 and pos[0]+i < self.__board.DIMENS and pos[1]+i >= 0 and pos[1]+i < self.__board.DIMENS:
                piece = self.at(pos[0]+i, pos[1]+i) 
                if piece != self.__board.FREE: # not a free space
                    if color != piece.get_color(): # opponent's piece
                        legal_moves.append((pos[0]+i, pos[1]+i))
                    break
                legal_moves.append((pos[0]+i, pos[1]+i))
            break
        for i in range(1, self.__board.DIMENS): # down and left
                if pos[0]+i >= 0 and pos[0]+i < self.__board.DIMENS and pos[1]-i >= 0 and pos[1]-i < self.__board.DIMENS:
                    piece = self.at(pos[0]+i, pos[1]-i) 
                    if piece != self.__board.FREE: # not a free space
                        if color != piece.get_color(): # opponent's piece
                            legal_moves.append((pos[0]+i, pos[1]-i))
                        break
                    legal_moves.append((pos[0]+i, pos[1]-i))
                break
        return legal_moves

        def generate_king_moves(self, color, pos):
            legal_moves = []
            if  pos[0]-1 >= 0 and (self.at(pos[0]-1, pos[1]) == self.__board.FREE or self.at(pos[0]-1, pos[1]).get_color() != color): # move one place forward
                legal_moves.append((pos[0]-2, pos[1]-1))
            if  pos[0]-1 <= 8 and (self.at(pos[0]+1, pos[1]) == self.__board.FREE or self.at(pos[0]+1, pos[1]).get_color() != color): # move one place backward
                legal_moves.append((pos[0]+1, pos[1]))
            if  pos[1]-1 >= 0 and (self.at(pos[0], pos[1]-1) == self.__board.FREE or self.at(pos[0], pos[1]-1).get_color() != color): # move one place left
                legal_moves.append((pos[0], pos[1]-1))
            if  pos[0]-1 >= 0 and (self.at(pos[0], pos[1]+1) == self.__board.FREE or self.at(pos[0], pos[1]+1).get_color() != color): # move one place right
                legal_moves.append((pos[0], pos[1]+1))
            if  pos[0]-1 >= 0 and pos[1] <= 8 and (self.at(pos[0]-1, pos[1]+1) == self.__board.FREE or self.at(pos[0]-1, pos[1]+1).get_color() != color): # move one place up and right
                legal_moves.append((pos[0]-1, pos[1]+1))
            if  pos[0]-1 >= 0 and pos[1] >= 0 and (self.at(pos[0]-1, pos[1]-1) == self.__board.FREE or self.at(pos[0]-1, pos[1]-1).get_color() != color): # move one place up and left
                legal_moves.append((pos[0]-1, pos[1]-1))
            if  pos[0]+1 <= 8 and pos[1] <= 8 and (self.at(pos[0]+1, pos[1]+1) == self.__board.FREE or self.at(pos[0]+1, pos[1]+1).get_color() != color): # move one place down and right
                legal_moves.append((pos[0]+1, pos[1]+1))
            if  pos[0]+1 <= 8 and pos[1] >= 0 and (self.at(pos[0]+1, pos[1]-1) == self.__board.FREE or self.at(pos[0]+1, pos[1]-1).get_color() != color): # move one place down and left
                legal_moves.append((pos[0]+1, pos[1]-1))
            return legal_moves
            
            

    def move(self, old, new):
        src, dest = self.__board.at(old[0], old[1]), self.__board.at(new[0], new[1])
        # determines if src/dest is free or occupied by black/white
        src_color, dest_color = self.__board.FREE, self.__board.FREE
        if src != self.__board.FREE: # not a free space
            print(src)
            src_color, dest_color = src.get_color(), self.__board.FREE if dest == self.__board.FREE else dest.get_color()
            if src_color == self.__turn and src_color != dest_color and new in src.get_legal_moves(): # player is moving their own piece to a valid space
                self.__board.move(old, new)
                self.next() # next turn
        
    # next turn
    def next(self):
        self.__turn *= -1 # changes turns
    
    # starts the game
    def start(self):
        self.generate_legal_moves()