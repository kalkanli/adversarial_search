import sys
import copy

n_util_calls = 0
n_actions = 0
move_dict = {
    'N': (-1, 0),
    'S': (1, 0),
    'E': (0, 1),
    'W': (0, -1),
    'NE': (-1, 1),
    'NW': (-1, -1),
    'SE': (1, 1),
    'SW': (1, -1)
}

piece_moves = {
    'Q': ['N', 'S', 'E', 'W', 'NE', 'NW', 'SE', 'SW'],
    'R': ['N', 'S', 'E', 'W'],
    'B': ['NE', 'NW', 'SE', 'SW']
}

def pprint(state):
    for row in state:
        for piece in row:
            print("{} ".format(piece), end='')
        print()

def compute_utility(board):
    global n_util_calls
    n_util_calls = n_util_calls + 1
    Q = sum(row.count('Q1') for row in board) - sum(row.count('Q2') for row in board)
    R = sum(row.count('R1') for row in board) - sum(row.count('R2') for row in board)
    B = sum(row.count('B1') for row in board) - sum(row.count('B2') for row in board)
    return 9 * Q + 5 * R + 3 * B

def move_to_final_state(move, frm, state):
    n = len(state)
    i = frm[0] + move[0]
    j = frm[1] + move[1]
    while(i < n and j < n and i >= 0 and j >= 0):
        if(state[i][j] == 'x'):
            i += move[0]
            j += move[1]
        elif(state[i][j][1] != state[frm[0]][frm[1]][1]):
            break
        else:
            i -= move[0]
            j -= move[1]
            break
    if i == n: i = n - 1
    if j == n: j = n - 1
    if i == -1: i = 0
    if j == -1: j = 0

    if(i == frm[0] and j == frm[1]):
        return None
    
    temp = state[frm[0]][frm[1]]
    state[frm[0]][frm[1]] = 'x'
    state[i][j] = temp
    return state

def move(i, j, state):
    piece = state[i][j][0]
    legal_moves = piece_moves[piece]
    states = []
    for move in legal_moves:
        x = copy.deepcopy(state)
        result = move_to_final_state(move_dict[move], (i, j), x)
        if result != None:
            states.append(result)
    return states

def get_pieces(state, agent):
    pieces = []
    for i in range(len(state)):
        for j in range(len(state)):
            if(state[i][j] != 'x' and state[i][j][1] == agent):
                pieces.append((i,j))
    return pieces

def minimax(state, depth, is_max):
    if(depth == n_actions*2):
        return compute_utility(state)
    if(is_max):
        pieces = get_pieces(state, '1')
        value = -9000
        child_nodes = []
        for piece in pieces:
            child_nodes.extend(move(piece[0], piece[1], state))
        for node in child_nodes:
            temp = minimax(node, depth+1, False)
            if temp > value:
                value = temp
        return value
    else:
        pieces = get_pieces(state, '2')
        value = 9000
        child_nodes = []
        for piece in pieces:
            child_nodes.extend(move(piece[0], piece[1], state))
        for node in child_nodes:
            temp = minimax(node, depth+1, True)
            if temp < value:
                value = temp
        return value


def main(argv):
    search_type = argv[0]
    init_file = argv[1]
    global n_actions
    n_actions = int(argv[2])

    f = open(init_file, "r")
    n = f.readline()
    n1 = int(n.split(' ')[0])
    
    initial_state = []
    for i in range(n1):
        line = f.readline()
        tokens = line.split(' ')
        initial_state.append([token.replace('\n', '') for token in tokens])
    print(minimax(initial_state, 0, True))
    print(n_util_calls)
    

if __name__ == '__main__':
    main(sys.argv[1:])