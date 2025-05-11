import pygame
import sys
import pyttsx3

# Initialize pygame and pyttsx3
pygame.init()
engine = pyttsx3.init()

# Screen settings
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
LINE_WIDTH = 15
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = SCREEN_WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4

# Colors
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
screen.fill(BG_COLOR)

# Board
board = [[0 for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

# Fullscreen toggle variable
fullscreen = False

# Functions
def speak(text):
    """Provide voice feedback."""
    engine.say(text)
    engine.runAndWait()

def draw_lines():
    """Draw grid lines."""
    for row in range(1, BOARD_ROWS):
        pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE * row), (SCREEN_WIDTH, SQUARE_SIZE * row), LINE_WIDTH)
    for col in range(1, BOARD_COLS):
        pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE * col, 0), (SQUARE_SIZE * col, SCREEN_HEIGHT), LINE_WIDTH)

def draw_figures():
    """Draw Xs and Os."""
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:
                pygame.draw.circle(screen, CIRCLE_COLOR,
                                   (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2),
                                   CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 2:
                pygame.draw.line(screen, CROSS_COLOR,
                                 (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR,
                                 (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE),
                                 CROSS_WIDTH)

def check_win(player):
    """Check if a player has won."""
    # Check rows and columns
    for i in range(BOARD_ROWS):
        if all([board[i][j] == player for j in range(BOARD_COLS)]) or \
           all([board[j][i] == player for j in range(BOARD_ROWS)]):
            return True
    # Check diagonals
    if all([board[i][i] == player for i in range(BOARD_ROWS)]) or \
       all([board[i][BOARD_ROWS - i - 1] == player for i in range(BOARD_ROWS)]):
        return True
    return False

def restart_game():
    """Restart the game."""
    global board, player, game_over
    board = [[0 for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    screen.fill(BG_COLOR)
    draw_lines()
    player = 1
    game_over = False
    speak("Game restarted!")

def toggle_fullscreen():
    """Toggle fullscreen mode."""
    global fullscreen, screen
    if fullscreen:
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        speak("Exited fullscreen mode.")
    else:
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
        speak("Entered fullscreen mode.")
    screen.fill(BG_COLOR)
    draw_lines()
    draw_figures()
    fullscreen = not fullscreen

def quit_game():
    """Quit the game."""
    speak("Thank you for playing Tic Tac Toe. Goodbye!")
    pygame.quit()
    sys.exit()

def ask_to_play_again():
    """Ask players if they want to play again."""
    speak("Do you want to play again? Press R to restart or Q to quit.")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Restart
                    restart_game()
                    return
                elif event.key == pygame.K_q:  # Quit
                    quit_game()

# Main loop variables
draw_lines()
player = 1
game_over = False

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX, mouseY = event.pos  # X and Y coordinates
            clicked_row = mouseY // SQUARE_SIZE
            clicked_col = mouseX // SQUARE_SIZE

            if board[clicked_row][clicked_col] == 0:  # Square is available
                board[clicked_row][clicked_col] = player
                draw_figures()
                speak(f"Player {player} made a move.")

                if check_win(player):
                    speak(f"Player {player} wins!")
                    game_over = True
                    ask_to_play_again()
                elif all(board[row][col] != 0 for row in range(BOARD_ROWS) for col in range(BOARD_COLS)):
                    speak("It's a draw!")
                    game_over = True
                    ask_to_play_again()
                else:
                    player = 2 if player == 1 else 1

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:  # Restart the game
                restart_game()
            elif event.key == pygame.K_q:  # Quit the game
                quit_game()
            elif event.key == pygame.K_f:  # Toggle fullscreen
                toggle_fullscreen()

    pygame.display.update()
