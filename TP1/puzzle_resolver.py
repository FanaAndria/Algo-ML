import heapq

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
