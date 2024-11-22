import heapq
import math

import math


def is_solvable(state):
    size = int(math.sqrt(len(state)))  # Taille de la grille (4 pour un puzzle 4x4)

    # Étape 1 : Calculer le nombre d'inversions
    inversions = 0
    for i in range(len(state)):
        for j in range(i + 1, len(state)):
            if state[i] > state[j] != 0:  # Ignorer la case vide (0)
                inversions += 1

    # Étape 2 : Trouver la ligne de la case vide (0)
    zero_index = state.index(0)
    zero_row = zero_index // size  # Ligne (en partant de 0)

    # Étape 3 : Appliquer la règle de parité
    # Pour une grille de taille paire (4x4), vérifier si la parité de (inversions + ligne du 0) est paire
    if size % 2 == 0:
        return (inversions + zero_row + 1) % 2 == 0
    else:
        # Pour une grille de taille impaire (comme 3x3), seulement les inversions comptent
        return inversions % 2 == 0


# Fonction pour calculer la distance de Manhattan
def manhattan_distance(state, goal):
    size = int(math.sqrt(len(state)))  # Taille de la grille
    distance = 0
    for i, value in enumerate(state):
        if value == 0:  # Ignorer la case vide
            continue
        goal_index = goal.index(value)
        x1, y1 = divmod(i, size)
        x2, y2 = divmod(goal_index, size)
        distance += abs(x1 - x2) + abs(y1 - y2)
    return distance

# Fonction pour générer les états voisins
def get_neighbors(state):
    size = int(math.sqrt(len(state)))
    zero_index = state.index(0)
    x, y = divmod(zero_index, size)
    neighbors = []

    # Déplacements possibles : haut, bas, gauche, droite
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dx, dy in moves:
        nx, ny = x + dx, y + dy
        if 0 <= nx < size and 0 <= ny < size:
            neighbor_index = nx * size + ny
            new_state = list(state)
            # Échanger la case vide avec son voisin
            new_state[zero_index], new_state[neighbor_index] = new_state[neighbor_index], new_state[zero_index]
            neighbors.append(tuple(new_state))
    return neighbors

# Fonction principale de l'algorithme A*
def a_star(start, goal):
    size = int(math.sqrt(len(start)))
    open_set = []
    heapq.heappush(open_set, (0, start))  # (coût estimé total, état)
    came_from = {}  # Pour reconstruire le chemin
    g_score = {start: 0}  # Coût réel du départ jusqu'à cet état
    f_score = {start: manhattan_distance(start, goal)}  # Coût estimé total

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            # Reconstruire le chemin à partir de came_from
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]  # Chemin dans l'ordre correct

        for neighbor in get_neighbors(current):
            tentative_g_score = g_score[current] + 1

            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + manhattan_distance(neighbor, goal)

                # Ajouter au tas si ce n'est pas déjà dedans
                if neighbor not in [item[1] for item in open_set]:
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None  # Pas de solution trouvée

# Exemple d'utilisation
if __name__ == "__main__":
    # Puzzle 3x3 : 0 représente la case vide
    start_state = (12, 6, 13, 10, 4, 11, 5, 9, 15, 3, 14, 0, 1, 2, 8, 7)
    goal_state = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0)

    if not is_solvable(start_state):
        print("Puzzle non solvable")
    else:
        solution = a_star(start_state, goal_state)
        if solution:
            print("Solution trouvée !")
            for step in solution:
                for i in range(int(math.sqrt(len(step)))):
                    print(step[i * int(math.sqrt(len(step))):(i + 1) * int(math.sqrt(len(step)))])
                print()
        else:
            print("Pas de solution.")


