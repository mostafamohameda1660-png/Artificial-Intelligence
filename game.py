ROW_COUNT = 6
COLUMN_COUNT = 7

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2

class Board:
    def __init__(self):
        self.board = []
        for _ in range(ROW_COUNT):
            row = [EMPTY] * COLUMN_COUNT
            self.board.append(row)
    
    def drop_piece(self, row, col, piece):
        self.board[row][col] = piece
    
    def is_valid_location(self, col):
        if self.board[ROW_COUNT - 1][col] == EMPTY:
            return True
        else:
            return False
    
    def get_next_open_row(self, col):
        for r in range(ROW_COUNT):
            if self.board[r][col] == EMPTY:
                return r
        return None
    
    def print_board(self):
        for r in range(ROW_COUNT - 1, -1, -1):
            print(self.board[r])
        print("  ".join(str(c) for c in range(COLUMN_COUNT)))
    
    def get_board(self):
        return self.board

    def winning_move(self, piece):
        board = self.board
        for r in range(ROW_COUNT):
            for c in range(COLUMN_COUNT - 3):
                if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                    return True
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT - 3):
                if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                    return True
        for r in range(ROW_COUNT - 3):
            for c in range(COLUMN_COUNT - 3):
                if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                    return True
        for r in range(3, ROW_COUNT):
            for c in range(COLUMN_COUNT - 3):
                if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                    return True
        return False

    def get_valid_locations(self):
        valid = []
        for col in range(COLUMN_COUNT):
            if self.board[ROW_COUNT - 1][col] == EMPTY:
                valid.append(col)
        return valid

    def is_terminal(self):
        if self.winning_move(PLAYER_PIECE):
            return True
        if self.winning_move(AI_PIECE):
            return True
        if len(self.get_valid_locations()) == 0:
            return True
        return False

def test_board():
    print("Testing Connect Four Board\n")
    b = Board()
    print("Empty board:")
    b.print_board()
    
    col = 3
    if b.is_valid_location(col):
        row = b.get_next_open_row(col)
        b.drop_piece(row, col, PLAYER_PIECE)
    print("\nAfter dropping a piece in column 3:")
    b.print_board()
    
    valid = b.get_valid_locations()
    print(f"\nValid columns: {valid}")
    print(f"Player wins? {b.winning_move(PLAYER_PIECE)}")
    print(f"Is terminal? {b.is_terminal()}")

if __name__ == "__main__":
    test_board()
