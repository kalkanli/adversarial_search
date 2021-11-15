import sys
import copy

n_util_calls = [0]
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

#N,NE,E,SE,S,SW,W,NW
piece_moves = {
    'Q': ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'],
    'R': ['N', 'E', 'S', 'W'],
    'B': ['NE', 'SE', 'SW', 'NW']
}

def pprint(state):
    for row in state:
        for piece in row:
            print("{} ".format(piece), end='')
        print()

def compute_utility(board):
    n_util_calls[0] += 1
    Q = sum(row.count('Q1') for row in board) - sum(row.count('Q2') for row in board)
    R = sum(row.count('R1') for row in board) - sum(row.count('R2') for row in board)
    B = sum(row.count('B1') for row in board) - sum(row.count('B2') for row in board)
    return 9 * Q + 5 * R + 3 * B

def move_to_final_state(direction, frm, board):
    n = len(board)
    move = move_dict[direction]
    i = frm[0]
    j = frm[1]
    k = i + move[0]
    l = j + move[1]

    while(k < n and l < n and k >= 0 and l >= 0):
        if(board[k][l] == 'x'):
            i = k
            j = l
            k += move[0]
            l += move[1]
        else:
            i = k
            j = l
            break
    if(i == frm[0] and j == frm[1]):
        return None
    
    temp = board[frm[0]][frm[1]]
    board[frm[0]][frm[1]] = 'x'
    board[i][j] = temp
    return {'board': board, 'move': "{} {}".format(board[i][j][0], direction)}

def move(i, j, board):
    piece = board[i][j][0]
    legal_moves = piece_moves[piece]
    states = []
    for move in legal_moves:
        x = copy.deepcopy(board)
        result = move_to_final_state(move, (i, j), x)
        if result != None:
            states.append(result)
    return states

def get_pieces(board, agent):
    pieces = []
    for i in range(len(board)):
        for j in range(len(board)):
            if(board[i][j] != 'x' and board[i][j][1] == agent):
                pieces.append((i,j))
    return pieces

def minimax(state, depth, is_max):
    if(depth == n_actions*2):
        state['utility'] = compute_utility(state['board'])
        return state
    if(is_max):
        pieces = get_pieces(state['board'], '1')
        state['utility'] = -9000
        child_nodes = []
        for piece in pieces:
            child_nodes.extend(move(piece[0], piece[1], state['board']))
        for node in child_nodes:
            temp = minimax(node, depth+1, False)
            if temp['utility'] > state['utility']:
                state['utility'] = temp['utility']
                state['next_move'] = temp['move']
        return state
    else:
        pieces = get_pieces(state['board'], '2')
        state['utility'] = 9000
        child_nodes = []
        for piece in pieces:
            child_nodes.extend(move(piece[0], piece[1], state['board']))
        for node in child_nodes:
            temp = minimax(node, depth+1, True)
            if temp['utility'] < state['utility']:
                state['utility'] = temp['utility']
                state['next_move'] = temp['move']
        return state

def alpha_beta_pruning(state, depth, a, b, is_max):
    if(depth == n_actions*2):
        state['utility'] = compute_utility(state['board'])
        return state
    if(is_max):
        pieces = get_pieces(state['board'], '1')
        state['utility'] = -9000
        child_nodes = []
        for piece in pieces:
            child_nodes.extend(move(piece[0], piece[1], state['board']))
        for node in child_nodes:
            child = alpha_beta_pruning(node, depth + 1, a, b, False)
            if child['utility'] > state['utility']:
                state['utility'] = child['utility']
                state['next_move'] = child['move']
            if(state['utility'] >= b):
                break
            if state['utility'] > a:
                a = state['utility']
        return state
    else:
        pieces = get_pieces(state['board'], '2')
        state['utility'] = 9000
        child_nodes = []
        for piece in pieces:
            child_nodes.extend(move(piece[0], piece[1], state['board']))
        for node in child_nodes:
            child = alpha_beta_pruning(node, depth + 1, a, b, True)
            if child['utility'] < state['utility']:
                state['utility'] = child['utility']
                state['next_move'] = child['move']
            if(state['utility'] <= a):
                break
            if state['utility'] < b:
                b = state['utility']
        return state


def main(argv):
    search_type = argv[0]
    init_file = argv[1]
    global n_actions
    n_actions = int(argv[2])

    f = open(init_file, "r")
    n = f.readline()
    n1 = int(n.split(' ')[0])
    
    initial_board = []
    for i in range(n1):
        line = f.readline()
        tokens = line.split(' ')
        initial_board.append([token.replace('\n', '') for token in tokens])
    
    if(search_type == 'minimax'):
        root_node = {'board': initial_board}
        result = minimax(root_node, 0, True)
    elif(search_type == 'alpha_beta_pruning'):
        root_node = {'board': initial_board}
        result = alpha_beta_pruning(root_node, 0, -9000, 9000, True)
    elif(search_type == 'minimax_rand'):
        print()
    print("Action: Move {}".format(result['next_move']))
    print("Value: {}".format(result['utility']))
    print("Util calls: {}".format(n_util_calls[0]))

if __name__ == '__main__':
    main(sys.argv[1:])