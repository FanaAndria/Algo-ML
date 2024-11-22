import pygame
import time
from  puzzle_resolver import a_star
from puzzle_util import create_puzzle, is_solvable

# Initialisation
pygame.init()

# Dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 400, 550  # Espace supplémentaire pour les boutons
FONT = pygame.font.Font(None, 36)

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 122, 122)
GRAY = (200, 200, 200)
GREEN = (0, 200, 0)

# Variables globales
GRID_SIZE = 3  # Par défaut, 8-puzzle
TILE_SIZE = SCREEN_WIDTH // GRID_SIZE
grid = []
empty_pos = None
selected_tiles = []

def swap_tiles(grid, pos1, pos2):
    r1, c1 = pos1
    r2, c2 = pos2
    grid[r1][c1], grid[r2][c2] = grid[r2][c2], grid[r1][c1]

# Affichage des boutons
def draw_buttons(screen):
    pygame.draw.rect(screen, GRAY, (50, 450, 140, 50))
    pygame.draw.rect(screen, GRAY, (210, 450, 140, 50))
    pygame.draw.rect(screen, GREEN, (130, 510, 140, 50))

    text_8 = FONT.render("3x3 (8)", True, BLACK)
    text_15 = FONT.render("4x4 (15)", True, BLACK)
    text_resolve = FONT.render("Résoudre", True, WHITE)
    screen.blit(text_8, (70, 460))
    screen.blit(text_15, (230, 460))
    screen.blit(text_resolve, (140, 520))

# Affichage de la grille
def draw_grid(screen, grid, grid_size):
    screen.fill(WHITE)
    for row in range(grid_size):
        for col in range(grid_size):
            tile = grid[row][col]
            if tile != 0:
                pygame.draw.rect(screen, BLUE, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                text = FONT.render(str(tile), True, WHITE)
                text_rect = text.get_rect(center=(col * TILE_SIZE + TILE_SIZE // 2, row * TILE_SIZE + TILE_SIZE // 2))
                screen.blit(text, text_rect)
            pygame.draw.rect(screen, BLACK, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE), 2)
    draw_buttons(screen)

# Mouvement des tuiles
def move_tile(grid, row, col, empty_row, empty_col):
    grid[empty_row][empty_col], grid[row][col] = grid[row][col], grid[empty_row][empty_col]

# Changement de puzzle
def change_puzzle(new_size):
    global GRID_SIZE, TILE_SIZE, grid, empty_pos
    GRID_SIZE = new_size
    TILE_SIZE = SCREEN_WIDTH // GRID_SIZE
    grid = create_puzzle(GRID_SIZE)
    empty_pos = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if grid[r][c] == 0][0]

# Résolution en temps réel
def resolve_puzzle():
    global empty_pos

    if not is_solvable(grid):
        print("Ce puzzle est non solvable.")
        return

    goal = [[(i * GRID_SIZE + j + 1) % (GRID_SIZE * GRID_SIZE) for j in range(GRID_SIZE)] for i in range(GRID_SIZE)]
    # Affichage de l'écran de chargement
    loading_text = FONT.render("Résolution en cours...", True, BLACK)
    loading_rect = loading_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.fill(WHITE)
    screen.blit(loading_text, loading_rect)
    pygame.display.flip()

    path = a_star(grid, goal)

    # Une fois la résolution terminée, on supprime l'écran de chargement
    screen.fill(WHITE)
    draw_grid(screen, grid, GRID_SIZE)
    pygame.display.flip()


    for move in path:
        row, col = empty_pos
        new_row, new_col = move
        move_tile(grid, new_row, new_col, row, col)
        empty_pos = (new_row, new_col)
        draw_grid(screen, grid, GRID_SIZE)
        pygame.display.flip()
        time.sleep(0.1)  # Pause pour animer chaque mouvement

# Boucle principale
def game_loop():
    global selected_tiles
    global empty_pos

    # Initialisation du puzzle
    change_puzzle(GRID_SIZE)

    global screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Puzzle Slider")
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                row, col = empty_pos
                if event.key == pygame.K_UP and row < GRID_SIZE - 1:
                    move_tile(grid, row + 1, col, row, col)
                    empty_pos = (row + 1, col)
                elif event.key == pygame.K_DOWN and row > 0:
                    move_tile(grid, row - 1, col, row, col)
                    empty_pos = (row - 1, col)
                elif event.key == pygame.K_LEFT and col < GRID_SIZE - 1:
                    move_tile(grid, row, col + 1, row, col)
                    empty_pos = (row, col + 1)
                elif event.key == pygame.K_RIGHT and col > 0:
                    move_tile(grid, row, col - 1, row, col)
                    empty_pos = (row, col - 1)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 50 <= x <= 190 and 450 <= y <= 500:  # Bouton 3x3
                    change_puzzle(3)
                elif 210 <= x <= 350 and 450 <= y <= 500:  # Bouton 4x4
                    change_puzzle(4)
                elif 130 <= x <= 270 and 510 <= y <= 560:  # Bouton Resolver
                    resolve_puzzle()
                else:
                    # Handle tile selection for swapping
                    row = y // TILE_SIZE
                    col = x // TILE_SIZE
                    if row < GRID_SIZE and col < GRID_SIZE:  # Ensure click is inside the grid
                        selected_tiles.append((row, col))
                        if len(selected_tiles) == 2:
                            swap_tiles(grid, selected_tiles[0], selected_tiles[1])
                            selected_tiles = []  # Reset after swap


        draw_grid(screen, grid, GRID_SIZE)
        pygame.display.flip()

    pygame.quit()

# Lancer le jeu
game_loop()

