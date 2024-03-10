import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
GRID_SIZE = 40
MARGIN_TOP = 40
MARGIN_BOTTOM = 100
MARGIN_LEFT = 100
MARGIN_RIGHT = 100
WIDTH, HEIGHT = 6 * GRID_SIZE + MARGIN_LEFT + MARGIN_RIGHT, 6 * GRID_SIZE + MARGIN_TOP + MARGIN_BOTTOM
MINE_COUNT = 6
LIFE_COUNT = 12
WHITE = (255, 255, 255)
GRAY = (192, 192, 192)
FONT_SIZE = 30

# Initialize the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper 2 Players")

# Load images
original_bomb_image = pygame.image.load('C:\\Users\\kenne\\OneDrive\\Documents\\TetrisProject\\Tetris\\comb.png')
original_coin_image = pygame.image.load('C:\\Users\\kenne\\OneDrive\\Documents\\TetrisProject\\Tetris\\coin.png')
original_life_image = pygame.image.load('C:\\Users\\kenne\\OneDrive\\Documents\\TetrisProject\\Tetris\\HEART.png')

# Resize images
bomb_image = pygame.transform.scale(original_bomb_image, (GRID_SIZE, GRID_SIZE))
coin_image = pygame.transform.scale(original_coin_image, (GRID_SIZE, GRID_SIZE))
life_image = pygame.transform.scale(original_life_image, (GRID_SIZE, GRID_SIZE))

# Fonts
font = pygame.font.Font(None, FONT_SIZE)

# Load background music
pygame.mixer.music.load('C:\\Users\\kenne\\OneDrive\\Documents\\TetrisProject\\Tetris\\forestwalk.mp3')
pygame.mixer.music.set_volume(0.5)  # Adjust the volume as needed
pygame.mixer.music.play(-1)  # Play the music indefinitely

# Function to reveal cells and handle turns
def reveal_cells(row, col, lives):
    if (row, col) in mine_positions:
        if lives > 0:
            return True  # Hit a mine, but still has lives
        else:
            return False  # Hit a mine, out of lives, game over
    elif (row, col) in life_positions:
        return True, True  # Got a life, and still in the game
    else:
        return True, False  # No mine, continue playing

# Function to draw the grid
def draw_grid():
    for i in range(7):
        pygame.draw.line(screen, GRAY, (i * GRID_SIZE + MARGIN_LEFT, MARGIN_TOP),
                         (i * GRID_SIZE + MARGIN_LEFT, HEIGHT - MARGIN_BOTTOM), 2)
        pygame.draw.line(screen, GRAY, (MARGIN_LEFT, i * GRID_SIZE + MARGIN_TOP),
                         (WIDTH - MARGIN_RIGHT, i * GRID_SIZE + MARGIN_TOP), 2)

# Function to draw the board
def draw_board():
    for row in range(6):
        for col in range(6):
            pygame.draw.rect(screen, WHITE, (col * GRID_SIZE + MARGIN_LEFT, row * GRID_SIZE + MARGIN_TOP,
                                             GRID_SIZE, GRID_SIZE), 0)
            pygame.draw.rect(screen, GRAY, (col * GRID_SIZE + MARGIN_LEFT, row * GRID_SIZE + MARGIN_TOP,
                                            GRID_SIZE, GRID_SIZE), 2)

            if board[row][col] != ' ':
                if board[row][col] == 'X':
                    screen.blit(bomb_image, (col * GRID_SIZE + MARGIN_LEFT, row * GRID_SIZE + MARGIN_TOP))
                elif board[row][col] == 'L':
                    screen.blit(life_image, (col * GRID_SIZE + MARGIN_LEFT, row * GRID_SIZE + MARGIN_TOP))
                else:
                    screen.blit(coin_image, (col * GRID_SIZE + MARGIN_LEFT, row * GRID_SIZE + MARGIN_TOP))

# Function to display player turn, lives, and moves
def display_info(player_turn, lives):
    player_turn_text = font.render(f"Turn: Player {player_turn}", True, (0, 0, 0))
    screen.blit(player_turn_text, (MARGIN_LEFT + 170 // 2 - FONT_SIZE, HEIGHT - MARGIN_BOTTOM // 2 - FONT_SIZE))

    player2_text = font.render("Player 2", True, (0, 0, 0))
    player1_text = font.render("Player 1", True, (0, 0, 0))
    screen.blit(player2_text, (WIDTH - MARGIN_RIGHT + 10, HEIGHT - 700 // 2 - FONT_SIZE // 2))
    screen.blit(player1_text, (MARGIN_LEFT - 90, HEIGHT - 700 // 2 - FONT_SIZE // 2))

    lives_text = font.render(f"Lives: {lives}", True, (0, 0, 0))
    text_rect = lives_text.get_rect(center=(MARGIN_LEFT + 170 // 2, HEIGHT - MARGIN_BOTTOM // 2 + FONT_SIZE))
    screen.blit(lives_text, text_rect)

# Function to display the homepage
def display_homepage():
    screen.fill(WHITE)
    title_font = pygame.font.Font(None, 50)
    title_text = title_font.render("Minesweeper", True, (0, 0, 0))
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))

    play_font = pygame.font.Font(None, 40)
    play_text = play_font.render("Play", True, (0, 0, 0))
    play_rect = play_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    pygame.draw.rect(screen, GRAY, play_rect, 2)
    screen.blit(play_text, play_rect)

    quit_text = play_font.render("Quit", True, (0, 0, 0))
    quit_rect = quit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60))
    pygame.draw.rect(screen, GRAY, quit_rect, 2)
    screen.blit(quit_text, quit_rect)

    pygame.display.flip()

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

# Main game loop
while True:
    if not display_homepage():
        break  # Player chose to quit

    player_turn = 1
    player_lives = [LIFE_COUNT, LIFE_COUNT]
    revealed_cells = 0
    running = True

    board = [[' ' for _ in range(6)] for _ in range(6)]
    mine_positions = random.sample([(i, j) for i in range(6) for j in range(6)], MINE_COUNT)
    life_positions = random.sample([(i, j) for i in range(6) for j in range(6) if (i, j) not in mine_positions], LIFE_COUNT)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                col = (event.pos[0] - MARGIN_LEFT) // GRID_SIZE
                row = (event.pos[1] - MARGIN_TOP) // GRID_SIZE

                if 0 <= row < 6 and 0 <= col < 6 and board[row][col] == ' ':
                    result, got_life = reveal_cells(row, col, player_lives[player_turn - 1])
                    if result:
                        if got_life:
                            board[row][col] = 'L'
                            player_lives[player_turn - 1] += 1
                        else:
                            mine_count = sum(1 for i, j in mine_positions if abs(row - i) <= 1 and abs(col - j) <= 1)
                            board[row][col] = str(mine_count)
                            revealed_cells += 1

                            if revealed_cells == 6 * 6 - MINE_COUNT:
                                print(f"Player {player_turn} wins! All cells revealed.")
                                running = False
                    else:
                        player_lives[player_turn - 1] -= 1
                        if player_lives[player_turn - 1] < 0:
                            print(f"Player {player_turn} is out of lives! Game Over.")
                            running = False

                    player_turn = 3 - player_turn  # Toggle between 1 and 2

        screen.fill(WHITE)
        draw_grid()
        draw_board()
        display_info(player_turn, player_lives[player_turn - 1])
        pygame.display.flip()

# Quit Pygame
pygame.mixer.music.stop()
pygame.quit()
sys.exit()
