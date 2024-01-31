from collections import deque

# TO-DO: 
# potentially cutting corners, e.g. 45 degree turns
# account for turns in shortest path (find time taken for a turn/moving forward)

N = 9

dx = [1, 0, -1, 0]
dy = [0, -1, 0, 1]

def bfs(start, bonus_zones, wood_blocks, minimum_path):
    directions = [(1, 0), (0, -1), (-1, 0), (0, 1)]
    q = deque([(start, 0)])
    while q:
        coord, gates_visited = q.popleft()
        for i in range(4):
            ncoord = (coord[0] + dx[i], coord[1] + dy[i])
            if 0 <= ncoord[0] < N and 0 <= ncoord[1] < N and not wood_blocks[ncoord[0]][ncoord[1]]:
                ngates_visited = gates_visited
                if ncoord in bonus_zones:
                    ngates_visited |= (1 << bonus_zones[ncoord])
                if minimum_path[ncoord[0]][ncoord[1]][ngates_visited] == []:
                    if 0 <= coord[0] < N and 0 <= coord[1] < N and not wood_blocks[coord[0]][coord[1]]:
                        minimum_path[ncoord[0]][ncoord[1]][ngates_visited] = minimum_path[coord[0]][coord[1]][gates_visited].copy()
                    else:
                        minimum_path[ncoord[0]][ncoord[1]][ngates_visited].append(coord)
                    minimum_path[ncoord[0]][ncoord[1]][ngates_visited].append(ncoord)
                    q.append((ncoord, ngates_visited))

def shortestPath():    
    stdin = open("board-input.txt", "r")
    stdout = open("path-input.txt", "w")
    m = int(stdin.readline())
    start = (m * 2 + 1, 0)
    a, b = map(int, stdin.readline().split())
    target = (a * 2 + 1, b * 2 + 1)

    n_bonus = int(stdin.readline())
    bonus_zones = {}
    for i in range(n_bonus):
        x, y = map(int, stdin.readline().split())
        p = (x * 2 + 1, y * 2 + 1)
        bonus_zones[p] = i
    # n_wood = int(stdin.readline())
    n_wood = 0
    wood_blocks = [[False] * N for _ in range(N)]
    wood_locations = []
    for i in range(4):
        s = stdin.readline()
        for j in range(3):
            if s[j] == '1':
                # wood_blocks[(j + 1) * 2][(3 - i) * 2 + 1] = True
                wood_locations.append(((j + 1) * 2, (3 - i) * 2 + 1))
                n_wood += 1
    for i in range(3):
        s = stdin.readline()
        for j in range(4):
            if s[j] == '1':
                # wood_blocks[j * 2 + 1][(i + 1) * 2] = True
                wood_locations.append((j * 2 + 1, (3 - i) * 2))
                n_wood += 1
    # ended here
    for i in range(n_wood):
        # p = tuple(map(int, stdin.readline().split()))
        p = wood_locations[i]
        # print(p)
        if p[0] % 2:
            wood_blocks[p[0]][p[1]] = True
            if p[0] + 1 < N:
                wood_blocks[p[0] + 1][p[1]] = True
            if p[0] - 1 >= 0:
                wood_blocks[p[0] - 1][p[1]] = True
        else:
            wood_blocks[p[0]][p[1]] = True
            if p[1] + 1 < N:
                wood_blocks[p[0]][p[1] + 1] = True
            if p[1] - 1 >= 0:
                wood_blocks[p[0]][p[1] - 1] = True

    for i in range(N):
        for j in range(N):
            if i == 0 or i == N - 1 or j == 0 or j == N - 1:
                wood_blocks[i][j] = True

    minimum_path = [[[[] for _ in range(1 << n_bonus)] for _ in range(N)] for _ in range(N)]
    bfs(start, bonus_zones, wood_blocks, minimum_path)

    curr_dir = 0 if start[0] == 0 else 2 if start[0] == N - 1 else 1 if start[1] == 0 else 3
    instructions = []
    cum = 0.5
    for i in range(len(minimum_path[target[0]][target[1]][(1 << n_bonus) - 1]) - 1):
        a = minimum_path[target[0]][target[1]][(1 << n_bonus) - 1][i]
        b = minimum_path[target[0]][target[1]][(1 << n_bonus) - 1][i + 1]
        dist = abs(a[0] - b[0]) + abs(a[1] - b[1])
        ndir = -1
        if b[0] - a[0] > 0:
            ndir = 0
        elif b[0] - a[0] < 0:
            ndir = 2
        elif b[1] - a[1] > 0:
            ndir = 1
        else:
            ndir = 3
        if ndir != curr_dir:
            instructions.append("tile " + str(int(cum)))
            cum = 0
        if abs(ndir - curr_dir) == 2:
            instructions.extend(["left", "left"])
        elif ndir - curr_dir == 1 or ndir - curr_dir == -3:
            instructions.append("left")
        elif ndir - curr_dir == -1 or ndir - curr_dir == 3:
            instructions.append("right")
        curr_dir = ndir
        cum += 0.5
    if cum != 0:
        instructions.append ("tile " + str(int(cum)))
    # for s in instructions:
    #     print(s)
    return instructions
    # for s in instructions:
    #     stdout.write(s + "\n")
    stdin.close()
    stdout.close()