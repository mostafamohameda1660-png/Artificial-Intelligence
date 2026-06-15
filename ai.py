import random
import math
import time
from game import AI_PIECE, PLAYER_PIECE, EMPTY, COLUMN_COUNT, ROW_COUNT

WINDOW_LENGTH = 4
DEPTH_MAP = {"easy": 2, "medium": 4, "hard": 6}


class AIPlayer:
    def __init__(self):
        self.node_count = 0

    def reset_nodes(self):
        self.node_count = 0

    def get_depth(self, difficulty):
        return DEPTH_MAP.get(difficulty, 2)

    def evaluate_window(self, window, piece):
        score = 0
        opp_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE

        if window.count(piece) > 0 and window.count(opp_piece) > 0:
            return 0

        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(EMPTY) == 1:
            score += 5
        elif window.count(piece) == 2 and window.count(EMPTY) == 2:
            score += 2

        if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
            score += 4

        return score

    def score_position(self, board_obj, piece):
        board = board_obj.board
        score = 0

        center_array = [board[r][COLUMN_COUNT // 2] for r in range(ROW_COUNT)]
        score += center_array.count(piece) * 3

        for r in range(ROW_COUNT):
            row_array = board[r]
            for c in range(COLUMN_COUNT - 3):
                window = row_array[c:c+4]
                score += self.evaluate_window(window, piece)

        for c in range(COLUMN_COUNT):
            col_array = [board[r][c] for r in range(ROW_COUNT)]
            for r in range(ROW_COUNT - 3):
                window = col_array[r:r+4]
                score += self.evaluate_window(window, piece)

        for r in range(ROW_COUNT - 3):
            for c in range(COLUMN_COUNT - 3):
                window = [board[r+i][c+i] for i in range(4)]
                score += self.evaluate_window(window, piece)

        for r in range(3, ROW_COUNT):
            for c in range(COLUMN_COUNT - 3):
                window = [board[r-i][c+i] for i in range(4)]
                score += self.evaluate_window(window, piece)

        return score

    def minimax(self, board_obj, depth, alpha, beta, maximizing):
        self.node_count += 1
        is_terminal = board_obj.is_terminal()

        if depth == 0 or is_terminal:
            if is_terminal:
                if board_obj.winning_move(AI_PIECE):
                    return None, 1000000
                if board_obj.winning_move(PLAYER_PIECE):
                    return None, -1000000
                return None, 0
            return None, self.score_position(board_obj, AI_PIECE)

        valid_locations = board_obj.get_valid_locations()
        valid_locations.sort(key=lambda x: abs(COLUMN_COUNT // 2 - x))

        if maximizing:
            value = -math.inf
            column = random.choice(valid_locations)

            for col in valid_locations:
                row = board_obj.get_next_open_row(col)
                board_obj.drop_piece(row, col, AI_PIECE)

                new_score = self.minimax(board_obj, depth - 1, alpha, beta, False)[1]

                board_obj.board[row][col] = EMPTY

                if new_score > value:
                    value = new_score
                    column = col

                alpha = max(alpha, value)
                if alpha >= beta:
                    break

            return column, value

        else:
            value = math.inf
            column = random.choice(valid_locations)

            for col in valid_locations:
                row = board_obj.get_next_open_row(col)
                board_obj.drop_piece(row, col, PLAYER_PIECE)

                new_score = self.minimax(board_obj, depth - 1, alpha, beta, True)[1]

                board_obj.board[row][col] = EMPTY

                if new_score < value:
                    value = new_score
                    column = col

                beta = min(beta, value)
                if alpha >= beta:
                    break

            return column, value

    def get_best_move(self, board_obj, depth=None, difficulty=None):
        self.reset_nodes()
        depth = depth or self.get_depth(difficulty or "easy")

        start_time = time.time()
        col, score = self.minimax(board_obj, depth, -math.inf, math.inf, True)
        elapsed = (time.time() - start_time) * 1000

        return {
            "column": col,
            "score": score,
            "nodes": self.node_count,
            "time_ms": round(elapsed, 2)
        }