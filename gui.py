# Connect Four GUI using Pygame
from email.mime import text
from turtle import color
import pygame
import sys
from game import Board, PLAYER_PIECE, AI_PIECE
from ai import AIPlayer
import random
import time
pygame.init()
# =========================
# GLOBALS
# =========================
winner = None
board_obj = Board()
turn = 0
ai_thinking = False
show_start_popup = False
popup_start_time = 0
popup_text = ""
player_start_time = 0
# Window size
WIDTH = 700
HEIGHT = 600
arrow_img = pygame.image.load(r"C:\Users\Mostafa Mohamed MSI\Desktop\project ai\pngwing.com.png")
arrow_img = pygame.transform.scale(arrow_img, (30, 30))
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Connect Four UI")
title_font = pygame.font.Font(r"C:\Users\Mostafa Mohamed MSI\Desktop\project ai\polarized bd.otf",60)
column_buttons = []
human_time = 0
ai_time = 0
ai_nodes = 0
human_score = 0
ai_score = 0
last_ai_col = None
COLS = 7
ROWS = 6
CELL_SIZE = 110
BOARD_X = 420
BOARD_Y = 120  
player_start_time = 0
# =========================
# Colors
# =========================
BACKGROUND_COLOR = (50, 117, 143)
BUTTON_COLOR = (252, 97, 0)
HOVER_COLOR = (255, 140, 50)
WHITE_BG = (255, 255, 255)
BORDER_COLOR = (30, 90, 110)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (200, 180, 40)
# =========================
color_text = "Color"
difficulty_text = "Difficulty"
font = pygame.font.Font(r"C:\Users\Mostafa Mohamed MSI\Desktop\project ai\polarized bd.otf",32)
# =========================
# Game State
# =========================
board_obj = Board()
ai = AIPlayer()
player_piece = None
ai_piece = None
turn = 0  # 0 = player , 1 = ai
game_started = False
color_menu = False
difficulty_menu = False
selected_color = None
selected_difficulty = None
board = board_obj.board
# =========================
# Buttons
# =========================
def create_buttons():
    button_width = 380
    button_height = 65
    spacing = 100
    x = 20
    y = 50
    step = button_height + spacing
    return {
        "coin": pygame.Rect(x, y + 0 * step, button_width, button_height),
        "difficulty": pygame.Rect(x, y + 1 * step, button_width, button_height),
        "start": pygame.Rect(x, y + 2 * step, button_width, button_height),
        "reset": pygame.Rect(x, y + 3 * step, button_width, button_height),
    }
buttons = create_buttons()
# =========================
# Dropdown RECTS 
# =========================
def get_color_dropdown():
    return {
        "red": pygame.Rect(buttons["coin"].x, buttons["coin"].y + 80, 180, 50),
        "yellow": pygame.Rect(buttons["coin"].x, buttons["coin"].y + 140, 180, 50),
    }
def get_difficulty_dropdown():
    return {
        "easy": pygame.Rect(buttons["difficulty"].x, buttons["difficulty"].y + 80, 180, 50),
        "medium": pygame.Rect(buttons["difficulty"].x, buttons["difficulty"].y + 140, 180, 50),
        "hard": pygame.Rect(buttons["difficulty"].x, buttons["difficulty"].y + 200, 180, 50),
    }
# =========================
# Background
# =========================
def draw_pattern():
    line_color = (80, 150, 180)
    spacing = WIDTH // 20
    for i in range(-HEIGHT, WIDTH, spacing):
        pygame.draw.line(screen, line_color, (i, 0), (i + HEIGHT, HEIGHT), 12)
# =========================
# Draw Buttons
# =========================
def draw_buttons():
    mouse_pos = pygame.mouse.get_pos()
    for key in buttons:
        color = HOVER_COLOR if buttons[key].collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(screen, color, buttons[key], border_radius=10)
    screen.blit(font.render(color_text, True, WHITE),
            (buttons["coin"].x + 20, buttons["coin"].y + 15))
    screen.blit(font.render(difficulty_text, True, WHITE),
            (buttons["difficulty"].x + 20, buttons["difficulty"].y + 15))
    screen.blit(font.render("START", True, WHITE), (buttons["start"].x + 50, buttons["start"].y + 15))
    screen.blit(font.render("RESET", True, WHITE), (buttons["reset"].x + 50, buttons["reset"].y + 15))
    # =========================
    # COLOR DROPDOWN
    # =========================
    if color_menu:
        opts = get_color_dropdown()
        for key, rect in opts.items():
            bg = (255, 230, 230) if rect.collidepoint(mouse_pos) else WHITE_BG
            draw_rect = rect.inflate(6, 6) if rect.collidepoint(mouse_pos) else rect
            pygame.draw.rect(screen, bg, draw_rect, border_radius=8)
            pygame.draw.rect(screen, BORDER_COLOR, draw_rect, 2, border_radius=8)
            text = font.render(key.capitalize(), True, BLACK)
            screen.blit(text, text.get_rect(center=draw_rect.center))
    # =========================
    # DIFFICULTY DROPDOWN
    # =========================
    if difficulty_menu:
        opts = get_difficulty_dropdown()
        for key, rect in opts.items():
            bg = (230, 255, 230) if rect.collidepoint(mouse_pos) else WHITE_BG
            draw_rect = rect.inflate(6, 6) if rect.collidepoint(mouse_pos) else rect
            pygame.draw.rect(screen, bg, draw_rect, border_radius=8)
            pygame.draw.rect(screen, BORDER_COLOR, draw_rect, 2, border_radius=8)
            text = font.render(key.capitalize(), True, BLACK)
            screen.blit(text, text.get_rect(center=draw_rect.center))
# =========================
# Layout
# =========================
def update_layout():
    base_y = 50
    spacing = 70
    color_offset = 130 if color_menu else 0
    difficulty_offset = 200 if difficulty_menu else 0
    buttons["coin"].y = base_y
    buttons["difficulty"].y = base_y + spacing + color_offset
    buttons["start"].y = base_y + 2 * spacing + color_offset + difficulty_offset
    buttons["reset"].y = base_y + 3 * spacing + color_offset + difficulty_offset
# =========================
# Board 
# =========================
def draw_board():
    board_rect = pygame.Rect(BOARD_X,BOARD_Y,COLS * CELL_SIZE,ROWS * CELL_SIZE)
    pygame.draw.rect(screen,(30, 90, 200),board_rect,border_radius=12)
    pygame.draw.rect(screen,(10, 40, 80),board_rect,6,border_radius=12)
    for row in range(ROWS):
        for col in range(COLS):
            x = int(BOARD_X + col * CELL_SIZE + CELL_SIZE // 2)
            y = int(BOARD_Y + row * CELL_SIZE + CELL_SIZE // 2)
            pygame.draw.circle(screen, WHITE, (x, y), 42)
            pygame.draw.circle(screen, (10, 40, 80), (x, y), 42, 5)
def draw_pieces():
    for row in range(ROWS):
        for col in range(COLS):
            x = BOARD_X + col * CELL_SIZE + CELL_SIZE // 2
            y = BOARD_Y + (ROWS - 1 - row) * CELL_SIZE + CELL_SIZE // 2
            if board_obj.board[row][col] == PLAYER_PIECE:
                pygame.draw.circle(screen, RED, (x, y), 35)
            elif board_obj.board[row][col] == AI_PIECE:
                pygame.draw.circle(screen, YELLOW, (x, y), 35)
# =========================
# Column Buttons 
# =========================
def draw_column_buttons():
    mouse_pos = pygame.mouse.get_pos()
    for rect in column_buttons:
        color = HOVER_COLOR if rect.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(screen, color, rect, border_radius=12)
        pygame.draw.rect(screen, (10, 40, 80), rect, 2, border_radius=12)
        img_rect = arrow_img.get_rect(center=rect.center)
        screen.blit(arrow_img, img_rect)
def create_column_buttons():
    global column_buttons
    column_buttons = []
    for col in range(COLS):
        rect = pygame.Rect(
            BOARD_X + col * 110,  
            BOARD_Y - 60,
            105,   
            50)
        column_buttons.append(rect)
def calculate_score(board, piece):
    score = 0
    ROWS = len(board)
    COLS = len(board[0])
    opponent_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE
    def check_window(window):
        nonlocal score
        count = window.count(piece)
        opp_count = window.count(opponent_piece)
        empty = window.count(0)
        # ======================
        # SELF SCORING
        # ======================
        if count == 4:
            score += 100
        elif count == 3 and empty == 1:
            score += 5
        elif count == 2 and empty == 2:
            score += 2
        # ======================
        # BLOCKING OPPONENT
        # ======================
        if opp_count == 3 and empty == 1:
            score += 4
    # ======================
    # CENTER COLUMN 
    # ======================
    center_col = [board[r][COLS // 2] for r in range(ROWS)]
    center_count = center_col.count(piece)
    score += center_count * 3
    # ======================
    # Horizontal
    # ======================
    for r in range(ROWS):
        for c in range(COLS - 3):
            window = board[r][c:c+4]
            check_window(window)
    # ======================
    # Vertical
    # ======================
    for c in range(COLS):
        for r in range(ROWS - 3):
            window = [board[r+i][c] for i in range(4)]
            check_window(window)
    # ======================
    # Diagonal 
    # ======================
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            window = [board[r+i][c+i] for i in range(4)]
            check_window(window)
    # ======================
    # Diagonal 
    # ======================
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            window = [board[r-i][c+i] for i in range(4)]
            check_window(window)
    return score
def draw_stats_panels():
    panel_w = WIDTH - BOARD_X - COLS * CELL_SIZE - 40
    panel_x = WIDTH - panel_w - 20
    font_small = pygame.font.Font(None, 28)
    # =====================
    # AI PANEL 
    # =====================
    rect1 = pygame.Rect(panel_x, 120, panel_w, 140)
    pygame.draw.rect(screen, (30, 90, 140), rect1, border_radius=12)
    text1 = font_small.render("AI", True, WHITE)
    text2 = font_small.render(f"Time: {ai_time} ms", True, WHITE)
    text3 = font_small.render(f"Score: {ai_score}", True, WHITE)
    screen.blit(text1, (panel_x + 15, 135))
    screen.blit(text2, (panel_x + 15, 170))
    screen.blit(text3, (panel_x + 15, 205))
    # =====================
    # HUMAN PANEL 
    # =====================
    rect2 = pygame.Rect(panel_x, 300, panel_w, 140)
    pygame.draw.rect(screen, (20, 120, 90), rect2, border_radius=12)
    text4 = font_small.render("HUMAN", True, WHITE)
    text5 = font_small.render(f"Time: {human_time} ms", True, WHITE)
    text6 = font_small.render(f"Score: {human_score}", True, WHITE)
    screen.blit(text4, (panel_x + 15, 315))
    screen.blit(text5, (panel_x + 15, 350))
    screen.blit(text6, (panel_x + 15, 385))      
def draw_win_panel(text):
        panel_w, panel_h = 420, 160
        x = WIDTH // 2 - panel_w // 2
        y = HEIGHT // 2 - panel_h // 2
        rect = pygame.Rect(x, y, panel_w, panel_h)
        pygame.draw.rect(screen, (20, 40, 80), rect, border_radius=15)
        pygame.draw.rect(screen, (255, 255, 255), rect, 3, border_radius=15)
        font_big = pygame.font.Font(None, 60)
        render = font_big.render(text, True, WHITE)
        screen.blit(render, render.get_rect(center=rect.center))
        rect = pygame.Rect(x, y, panel_w, panel_h)
def draw_popup(text):
    panel_w, panel_h = 420, 160
    x = WIDTH // 2 - panel_w // 2
    y = HEIGHT // 2 - panel_h // 2
    rect = pygame.Rect(x, y, panel_w, panel_h)
    pygame.draw.rect(screen, (20, 40, 80), rect, border_radius=15)
    pygame.draw.rect(screen, (255, 255, 255), rect, 3, border_radius=15)
    font_big = pygame.font.Font(None, 60)
    render = font_big.render(text, True, WHITE)
    screen.blit(render, render.get_rect(center=rect.center))
# =========================
# MAIN LOOP
# =========================
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.VIDEORESIZE:
            WIDTH, HEIGHT = event.w, event.h
            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
            buttons = create_buttons()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            # =========================
            # BOARD CLICK 
            # =========================
            for col, rect in enumerate(column_buttons):
                if rect.collidepoint(mouse_pos):
                    if game_started and selected_color:
                        # PLAYER MOVE
                        if board_obj.is_valid_location(col):
                            row = board_obj.get_next_open_row(col)
                            board_obj.drop_piece(row, col, player_piece)
                            end_time = pygame.time.get_ticks()
                            human_time = end_time - player_start_time 
                            player_start_time = 0  
                            if board_obj.winning_move(player_piece):
                                winner = "PLAYER"
                                game_started = False
                            human_score = calculate_score(board_obj.board, player_piece)
                            turn = 1
            # =========================
            # MENU TOGGLES
            # =========================
            if buttons["coin"].collidepoint(mouse_pos):
                color_menu = not color_menu
                difficulty_menu = False
            elif buttons["difficulty"].collidepoint(mouse_pos):
                difficulty_menu = not difficulty_menu
                color_menu = False
            # =========================
            # COLOR SELECT
            # =========================
            if color_menu:
                opts = get_color_dropdown()
                if opts["red"].collidepoint(mouse_pos):
                    selected_color = "RED"
                    color_text = "Color: RED"
                    color_menu = False
                    player_piece = PLAYER_PIECE
                    ai_piece = AI_PIECE
                elif opts["yellow"].collidepoint(mouse_pos):
                    selected_color = "YELLOW"
                    color_text = "Color: YELLOW"
                    color_menu = False
                    player_piece = AI_PIECE
                    ai_piece = PLAYER_PIECE
            # =========================
            # DIFFICULTY SELECT
            # =========================
            if difficulty_menu:
                opts = get_difficulty_dropdown()
                if opts["easy"].collidepoint(mouse_pos):
                    selected_difficulty = "EASY"
                    difficulty_text = "Difficulty: EASY"
                    difficulty_menu = False
                elif opts["medium"].collidepoint(mouse_pos):
                    selected_difficulty = "MEDIUM"
                    difficulty_text = "Difficulty: MEDIUM"
                    difficulty_menu = False
                elif opts["hard"].collidepoint(mouse_pos):
                    selected_difficulty = "HARD"
                    difficulty_text = "Difficulty: HARD"
                    difficulty_menu = False
            # =========================
            # START
            # =========================
            if buttons["start"].collidepoint(mouse_pos):
                if selected_color and selected_difficulty:
                    game_started = True
                    show_start_popup = True
                    popup_start_time = time.time()
                    popup_text = "START!"
            # =========================
            # RESET
            # =========================
            if buttons["reset"].collidepoint(mouse_pos):
                selected_color = None
                selected_difficulty = None
                game_started = False
                color_menu = False
                difficulty_menu = False
                color_text = "Color"
                difficulty_text = "Difficulty"
                board_obj = Board()
                turn = 0
                winner = None
                player_piece = None
                ai_piece = None
            # RESET SCORES
                human_score = 0
                ai_score = 0
            # RESET TIME
                human_time = 0
                ai_time = 0
            # RESET STATS
                ai_nodes = 0
            last_ai_col = None
    # =========================
    # DRAW LOOP
    # =========================
    update_layout()
    create_column_buttons()
    screen.fill(BACKGROUND_COLOR)
    draw_pattern()
    draw_board()
    draw_pieces()
    draw_buttons()
    draw_column_buttons()
    draw_stats_panels()
    if ai_thinking:
        draw_popup("AI THINKING...")
    if show_start_popup:
        draw_popup(popup_text)
    if time.time() - popup_start_time > 1:
        show_start_popup = False    
    if game_started and turn == 0 and player_start_time == 0:
        player_start_time = pygame.time.get_ticks()
    # AI TURN
    if game_started and turn == 1:
        ai_thinking = True
        draw_popup("AI THINKING...")
        pygame.display.update()
        pygame.time.delay(80)
        start_time = time.time()
        result = ai.get_best_move(
            board_obj,
            difficulty=selected_difficulty.lower())
        end_time = time.time()
        col_ai = result["column"]
        if col_ai is None:
            col_ai = random.choice(board_obj.get_valid_locations())
        if board_obj.is_valid_location(col_ai):
            row = board_obj.get_next_open_row(col_ai)
            board_obj.drop_piece(row, col_ai, ai_piece)
            ai_thinking = False
            if board_obj.winning_move(ai_piece):
                winner = "AI"
                game_started = False
            ai_score = calculate_score(board_obj.board, ai_piece)
        print("AI MOVE")
        print("Column:", col_ai)
        print("Score:", ai_score)
        print("Nodes:", ai_nodes)
        print("Time(ms):", ai_time)
        print(board_obj.board)        
    # =========================
    # UPDATE STATS 
    # =========================
        last_ai_col = col_ai
        ai_nodes = result.get("nodes", 0)
        ai_score = calculate_score(board_obj.board, ai_piece)
        ai_time = int((end_time - start_time) * 1000)
        turn = 0
    title_text_render = title_font.render("CONNECT FOUR", True, WHITE)
    screen.blit(title_text_render, title_text_render.get_rect(center=(WIDTH // 2, 25)))
    if winner:
        draw_win_panel(f"{winner} WINS!")
    pygame.display.update()