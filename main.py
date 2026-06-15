from game import Board, PLAYER_PIECE, AI_PIECE
from ai import AIPlayer
import random

def choose_difficulty():
    while True:
        diff = input("Choose difficulty (easy / medium / hard): ").lower()
        if diff in ["easy", "medium", "hard"]:
            return diff
        else:
            print("Invalid choice! Try again.")

def choose_player():
    while True:
        choice = input("Choose your piece (1 or 2): ")
        if choice == "1":
            return PLAYER_PIECE, AI_PIECE
        elif choice == "2":
            return AI_PIECE, PLAYER_PIECE
        else:
            print("Invalid input! Please enter 1 or 2.")

def choose_column(board):
    while True:
        try:
            col = int(input("Choose column (0-6): "))
            if 0 <= col <= 6:
                if board.is_valid_location(col):
                    return col
                else:
                    print("Column full! Choose another.")
            else:
                print("Out of range! (0-6 only)")
        except:
            print("Invalid input! Enter a number.")

def main():
    print("=== CONNECT FOUR AI ===")

    board = Board()
    ai = AIPlayer()

    difficulty = choose_difficulty()
    player_piece, ai_piece = choose_player()

    game_over = False
    turn = 0

    board.print_board()

    while not game_over:

        if turn == 0:
            print("\nYour Turn")
            col = choose_column(board)

            row = board.get_next_open_row(col)
            board.drop_piece(row, col, player_piece)

            if board.winning_move(player_piece):
                board.print_board()
                print("YOU WIN!")
                game_over = True

        else:
            print("\nAI Thinking...")

            result = ai.get_best_move(board, difficulty=difficulty)
            col = result["column"]

            if col is None:
                col = random.choice(board.get_valid_locations())

            if board.is_valid_location(col):
                row = board.get_next_open_row(col)
                board.drop_piece(row, col, ai_piece)

                print(f"AI chose column {col}")

                if board.winning_move(ai_piece):
                    board.print_board()
                    print("AI WINS!")
                    game_over = True

        board.print_board()

        if len(board.get_valid_locations()) == 0 and not game_over:
            print("Draw!")
            game_over = True

        turn ^= 1

if __name__ == "__main__":
    main()