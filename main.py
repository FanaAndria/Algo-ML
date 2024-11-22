import pygame
import random
import heapq
import time

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

def is_solvable(state):
    # Convertir la grille en une liste plate
    flattened = [tile for row in state for tile in row]
    size = len(state)

    # Étape 1 : Calculer le nombre d'inversions
    inversions = 0
    for i in range(len(flattened)):
        for j in range(i + 1, len(flattened)):
            if flattened[i] != 0 and flattened[j] != 0 and flattened[i] > flattened[j]:
                inversions += 1

    # Étape 2 : Trouver la ligne de la case vide (0)
    zero_row = next(row for row in range(size) if 0 in state[row])  # Ligne où se trouve la case vide

    # Étape 3 : Vérifier les conditions de résolvabilité
    if size % 2 == 0:  # Grille de taille paire (4x4)
        return (inversions + zero_row + 1) % 2 == 0
    else:  # Grille de taille impaire (3x3)
        return inversions % 2 == 0


# Création d'un puzzle mélangé
def create_puzzle(size):
    numbers = list(range(1, size * size)) + [0]  # 0 représente le vide
    random.shuffle(numbers)
    grid = [numbers[i * size:(i + 1) * size] for i in range(size)]

    # Regenere le grid jusqu'a ce qu'il soit solvable
    while not is_solvable(grid):
        numbers = list(range(1, size * size)) + [0]
        random.shuffle(numbers)
        grid = [numbers[i * size:(i + 1) * size] for i in range(size)]
    return [numbers[i * size:(i + 1) * size] for i in range(size)]

# Vérifier si un état est le but
def is_goal(state, size):
    return state == [[(i * size + j + 1) % (size * size) for j in range(size)] for i in range(size)]

# Générer les voisins d'un état
def get_neighbors(state):
    size = len(state)
    neighbors = []
    empty_pos = [(r, c) for r in range(size) for c in range(size) if state[r][c] == 0][0]
    row, col = empty_pos
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for dr, dc in moves:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < size and 0 <= new_col < size:
            new_state = [list(row) for row in state]
            new_state[row][col], new_state[new_row][new_col] = new_state[new_row][new_col], new_state[row][col]
            neighbors.append((new_state, (new_row, new_col)))
    return neighbors

# Heuristique : Distance de Manhattan
def manhattan_distance(state, goal):
    distance = 0
    size = len(state)
    for i in range(size):
        for j in range(size):
            if state[i][j] != 0:
                correct_pos = [(row, col) for row in range(size) for col in range(size) if goal[row][col] == state[i][j]][0]
                distance += abs(correct_pos[0] - i) + abs(correct_pos[1] - j)
    return distance


# Algorithme A*
def a_star(start, goal):
    frontier = []
    heapq.heappush(frontier, (0, start, []))  # (coût, état, chemin)
    visited = set()
    visited.add(str(start))

    while frontier:
        _, current, path = heapq.heappop(frontier)

        if current == goal:
            return path

        for neighbor, move in get_neighbors(current):
            if str(neighbor) not in visited:
                visited.add(str(neighbor))
                #visited.add(tuple(map(tuple, neighbor)))
                new_path = path + [move]
                priority = len(new_path) + manhattan_distance(neighbor, goal)
                heapq.heappush(frontier, (priority, neighbor, new_path))
    return []

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

        draw_grid(screen, grid, GRID_SIZE)
        pygame.display.flip()

    pygame.quit()

# Lancer le jeu
game_loop()

