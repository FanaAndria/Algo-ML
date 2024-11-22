import random

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

    # Régénère le grid jusqu'a ce qu'il soit solvable
    while not is_solvable(grid):
        random.shuffle(numbers)
        grid = [numbers[i * size:(i + 1) * size] for i in range(size)]
    return grid

# Vérifier si un état est le but
def is_goal(state, size):
    return state == [[(i * size + j + 1) % (size * size) for j in range(size)] for i in range(size)]
