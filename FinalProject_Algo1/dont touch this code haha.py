import pygame
import sys
import random
import tkinter as tk
from tkinter import ttk
import imageio
import io 
from PIL import Image, ImageTk
import datetime
from datetime import datetime
from datetime import datetime as dt

pygame.init()

# Constants
GRID_SIZE = 40
MARGIN_TOP = 180
MARGIN_BOTTOM = 100
MARGIN_LEFT = 100
MARGIN_RIGHT = 100
WIDTH, HEIGHT = 6 * GRID_SIZE + MARGIN_LEFT + MARGIN_RIGHT, 6 * GRID_SIZE + MARGIN_TOP + MARGIN_BOTTOM
WHITE = (255, 255, 255)
GRAY = (192, 192, 192)
CYAN = (0, 255, 255)
FONT_SIZE = 30

# Coin class
class Coin:
    def __init__(self, value, image_path):
        self.value = value
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (GRID_SIZE, GRID_SIZE))

# Bomb class
class Bomb:
    def __init__(self, image_path):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (GRID_SIZE, GRID_SIZE))
        self.revealed = False  # Flag to track whether the bomb is revealed

# Robbery class
class Robbery:
    def __init__(self, image_path):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (GRID_SIZE, GRID_SIZE))
        self.revealed = False  # Flag to track whether the robbery is revealed

# Player class
class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0

# Global variables for match history
match_history = []
small_font_size = 20
small_press_start_font = pygame.font.Font("PressStart2P-Regular.ttf", small_font_size)
press_start_font = pygame.font.Font("PressStart2P-Regular.ttf", FONT_SIZE)

# Load match history from a file or initialize an empty list
try:
    with open('match_history.txt', 'r') as file:
        for line in file:
            match_history.append(line.strip())
except FileNotFoundError:
    match_history = []

# Initialize the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper 2 Players")

# Load the GIF frames
background_gif = imageio.mimread('giphy.gif', 'GIF')

# Convert the frames to a consistent RGBA format and resize
background_frames = []
for frame in background_gif:
    pil_image = Image.fromarray(frame)
    pil_image = pil_image.convert('RGBA')
    pil_image = pil_image.resize((WIDTH, HEIGHT))
    data = pil_image.tobytes('raw', 'RGBA')
    pygame_image = pygame.image.fromstring(data, (WIDTH, HEIGHT), 'RGBA')
    background_frames.append(pygame_image)

# Load images
original_coin1_image = pygame.image.load('coin1.png')
original_coin2_image = pygame.image.load('coin2.png')
original_coin3_image = pygame.image.load('coin3.png')
original_bomb_image = pygame.image.load('bomb.png')
original_robbery_image = pygame.image.load('robbery.png')

# Resize images
coin1 = Coin(1, 'coin1.png')
coin2 = Coin(2, 'coin2.png')
coin3 = Coin(3, 'coin3.png')
bomb = Bomb('bomb.png')
robbery = Robbery('robbery.png')

# Fonts
font = pygame.font.Font(None, FONT_SIZE)

# Load background music
pygame.mixer.music.load('forestwalk.mp3')
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)

# Function to handle turns
def handle_turn(player):
    coin_values = [1, 2, 3]
    coin_probabilities = [0.35, 0.25, 0.25]  # Adjusted probabilities
    coin_value = random.choices(coin_values, weights=coin_probabilities)[0]

    # Update player's score based on the chosen coin's value
    if coin_value == 1:
        player.score += 1
    elif coin_value == 2:
        player.score += 2
    elif coin_value == 3:
        player.score += 3

    return coin_value

# Function to initialize bombs and robberies on the board
def initialize_bombs_and_robberies(board):
    bomb_count = 2
    robbery_count = 6  # Number of robberies
    while bomb_count > 0 or robbery_count > 0:
        row = random.randint(0, 5)
        col = random.randint(0, 5)

        # Place the bomb or robbery if the cell is empty
        if board[row][col] == ' ':
            if bomb_count > 0:
                board[row][col] = Bomb('bomb.png')
                bomb_count -= 1
            elif robbery_count > 0:
                board[row][col] = Robbery('robbery.png')
                robbery_count -= 1

# Function to draw the grid
def draw_grid():
    for i in range(7):
        pygame.draw.line(screen, GRAY, (i * GRID_SIZE + MARGIN_LEFT, MARGIN_TOP),
                         (i * GRID_SIZE + MARGIN_LEFT, HEIGHT - MARGIN_BOTTOM), 2)
        pygame.draw.line(screen, GRAY, (MARGIN_LEFT, i * GRID_SIZE + MARGIN_TOP),
                         (WIDTH - MARGIN_RIGHT, i * GRID_SIZE + MARGIN_TOP), 2)

# Function to draw the board
def draw_board(board):
    for row in range(6):
        for col in range(6):
            pygame.draw.rect(screen, WHITE, (col * GRID_SIZE + MARGIN_LEFT, row * GRID_SIZE + MARGIN_TOP,
                                             GRID_SIZE, GRID_SIZE), 0)
            pygame.draw.rect(screen, GRAY, (col * GRID_SIZE + MARGIN_LEFT, row * GRID_SIZE + MARGIN_TOP,
                                            GRID_SIZE, GRID_SIZE), 2)

            if board[row][col] != ' ':
                if isinstance(board[row][col], Coin) or (isinstance(board[row][col], Bomb) and board[row][col].revealed) or (isinstance(board[row][col], Robbery) and board[row][col].revealed):
                    screen.blit(board[row][col].image, (col * GRID_SIZE + MARGIN_LEFT, row * GRID_SIZE + MARGIN_TOP))

# Function to display player information
def display_player_info(players):
    for idx, player in enumerate(players):
        player_name_text = font.render(f"{player.name}", True, (255, 255, 255))
        player_score_text = font.render(f"Score: {player.score}", True, (255, 255, 255))

        text_position = (MARGIN_LEFT + (WIDTH - MARGIN_LEFT - MARGIN_RIGHT) * idx // len(players),
                         HEIGHT - MARGIN_BOTTOM + FONT_SIZE)

        screen.blit(player_name_text, text_position)
        screen.blit(player_score_text, (text_position[0], text_position[1] + FONT_SIZE))

# Function to display player turn
def display_player_turn(player):
    player_turn_text = font.render(f"Player Turn: {player.name}", True, (255, 255, 255))
    text_position = ((WIDTH - player_turn_text.get_width()) // 2, MARGIN_TOP - FONT_SIZE)
    screen.blit(player_turn_text, text_position)

# Function to display game over message and ask for a rematch
def display_game_over(players):
    winner = max(players, key=lambda x: x.score)
    winners = [player for player in players if player.score == winner.score]

    if len(winners) == 1:
        winner_names = winners[0].name
        game_over_text = f"{winner_names} wins with {winner.score} points! Game Over."
    else:
        winner_names = ", ".join([winner.name for winner in winners])
        game_over_text = f"Draw! : {winner.score} points."

    game_over_font = pygame.font.Font(None, 30)
    game_over_render = game_over_font.render(game_over_text, True, (255, 255, 255))
    text_position = ((WIDTH - game_over_render.get_width()) // 2, MARGIN_TOP - FONT_SIZE * 6)
    screen.blit(game_over_render, text_position)

    play_again_yes_text = game_over_font.render("Yes", True, (255, 255, 255))
    play_again_yes_rect = play_again_yes_text.get_rect(center=(WIDTH // 2 - 50, MARGIN_TOP - FONT_SIZE * 4.5))
    #pygame.draw.rect(screen, GRAY, play_again_yes_rect, 2)
    screen.blit(play_again_yes_text, play_again_yes_rect)

    play_again_no_text = game_over_font.render("No", True, (255, 255, 255))
    play_again_no_rect = play_again_no_text.get_rect(center=(WIDTH // 2 + 50, MARGIN_TOP - FONT_SIZE * 4.5))
    #pygame.draw.rect(screen, GRAY, play_again_no_rect, 2)
    screen.blit(play_again_no_text, play_again_no_rect)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if play_again_yes_rect.collidepoint(event.pos):
                    return True  # Play again
                elif play_again_no_rect.collidepoint(event.pos):
                    return False  # Quit


# Function to display the homepage
def display_homepage():
    clock = pygame.time.Clock()
    frame_index = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if play_rect.collidepoint(event.pos):
                    return True  # Player chose to play
                elif quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        # Display GIF background
        screen.blit(background_frames[frame_index], (0, 0))

        # Display Minesweeper elements on top of the background
        title_text = press_start_font.render("Minesweeper", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        screen.blit(title_text, title_rect)

        title_text = small_press_start_font.render("New legacy", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4 + 40))
        screen.blit(title_text, title_rect)
        
        play_font = pygame.font.Font(None, 40)
        play_text = play_font.render("Play", True, (255, 255, 255))
        play_rect = play_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        pygame.draw.rect(screen, (64, 64, 64), play_rect, 0)
        pygame.draw.rect(screen, (64, 64, 64), play_rect, 2)
        screen.blit(play_text, play_rect)

        quit_text = play_font.render("Quit", True, (255, 255, 255))
        quit_rect = quit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60))
        pygame.draw.rect(screen, (64, 64, 64), quit_rect, 0)
        pygame.draw.rect(screen, (64, 64, 64), quit_rect, 2)
        screen.blit(quit_text, quit_rect)

        match_history_label_font = pygame.font.Font(None, 20)
        match_history_label_text = match_history_label_font.render("Matches History:", True, (255, 255, 255))
        match_history_label_rect = match_history_label_text.get_rect(center=(WIDTH // 2, HEIGHT // 1.5 + 5))
        #pygame.draw.rect(screen, GRAY, match_history_label_rect, 2)
        screen.blit(match_history_label_text, match_history_label_rect)

        # Display match history
        history_content_font = pygame.font.Font(None, 15)
        y_offset = 0
        for match in match_history:
            match_text = history_content_font.render(match, True, (255, 255, 255))
            match_rect = match_text.get_rect(center=(WIDTH // 2, HEIGHT // 1.5 + y_offset + 30))
            screen.blit(match_text, match_rect)
            y_offset += 20

        pygame.display.flip()

        frame_index = (frame_index + 1) % len(background_frames)

        clock.tick(100)  # Increased frame rate to 30 frames per second
        pygame.display.flip()
        
# Main game loop
match_history = [] 
match_number = 0
frame_index = 0


while True:
    match_number += 1
    
    if not display_homepage():
        break  # Player chose to quit

    # Create player objects
    player1 = Player("Player 1")
    player2 = Player("Player 2")

    players = [player1, player2]
    player_turn = 0
    running = True

    board = [[' ' for _ in range(6)] for _ in range(6)]

    # Initialize bombs, coins, and robberies on the board
    initialize_bombs_and_robberies(board)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                col = (event.pos[0] - MARGIN_LEFT) // GRID_SIZE
                row = (event.pos[1] - MARGIN_TOP) // GRID_SIZE

                if 0 <= row < 6 and 0 <= col < 6:
                    # Check if the selected cell contains a bomb
                    if isinstance(board[row][col], Bomb) and not board[row][col].revealed:
                        board[row][col].revealed = True
                        running = False  # Game over
                    # Check if the selected cell contains a robbery
                    # Check if the selected cell contains a robbery
                    elif isinstance(board[row][col], Robbery) and not board[row][col].revealed:
                        board[row][col].revealed = True
                        players[player_turn].score -= 5  # Deduct points for robbery
                        if players[player_turn].score < 0:
                            players[player_turn].score = 0  # Ensure the score doesn't go negative
                        else:
                            player_turn = 1 - player_turn  # Toggle between 0 and 1

                    else:
                        coin_value = handle_turn(players[player_turn])

                        if coin_value == 1:
                            board[row][col] = coin1
                        elif coin_value == 2:
                            board[row][col] = coin2
                        elif coin_value == 3:
                            board[row][col] = coin3

                        player_turn = 1 - player_turn  # Toggle between 0 and 1

                        # Check if all cells are revealed
                        revealed_cells = sum(row.count(cell) for row in board for cell in row if
                                             isinstance(cell, Bomb) and not cell.revealed) + \
                                         sum(row.count(cell) for row in board for cell in row if
                                             isinstance(cell, Robbery) and not cell.revealed)
                        if revealed_cells == 0:
                            running = False

        frame_index = (frame_index + 1) % len(background_frames)
        screen.blit(background_frames[frame_index], (0, 0))

        draw_grid()
        draw_board(board)

        # Display player turn
        display_player_turn(players[player_turn])

        # Display player information below the game table
        display_player_info(players)


        pygame.display.flip()

        pygame.time.delay(8)

    current_time = dt.now().strftime("%Y-%m-%d %H:%M:%S")
    match_result = f"Match {match_number}: {current_time}: {players[0].name} has {players[0].score} score - {players[1].name} has {players[1].score} score"
    match_history.append(match_result)

    match_history = match_history[-3:]

    # Display game over message and ask for a rematch
    if not display_game_over(players):
        break  # Player chose to quit


with open('match_history.txt', 'w') as file:
    for entry in match_history:
        file.write(f"{entry}\n")

# Stop background music
pygame.mixer.music.stop()

# Quit Pygame
pygame.quit()
sys.exit()
