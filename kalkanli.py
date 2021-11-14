import sys
import copy

n_util_calls = 0
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

def pprint(state):
    for row in state:
        for piece in row:
            print("{} ".format(piece), end='')
        print()

def compute_utility(board):
    Q = sum(row.count('Q1') for row in board) - sum(row.count('Q2') for row in board)
    R = sum(row.count('R1') for row in board) - sum(row.count('R2') for row in board)
    B = sum(row.count('B1') for row in board) - sum(row.count('B2') for row in board)
    return 9 * Q + 5 * R + 3 * B

def move_to_final_state(move_to, i, j, state):
    up = move_to[0]
    right = move_to[1]

    if(i + up == len(state) or j + right == len(state) or j + right == -1 or i + up == -1): ## if out of board
        return state ## be careful with returning the same state. it would be catastrophic
    elif(state[i + up][j + right] == 'x'): ## if no piece
        temp = state[i][j]
        state[i][j] = state[i + up][j + right]
        state[i + up][j + right] = temp
        return move_to_final_state(move_to, i + up, j + right, state)
    if(state[i + up][j + right][1] == state[i][j][1]):  ## if same agent's piece
        return state
    elif(state[i + up][j + right][1] != state[i][j][1]): ## if opponent's piece
        state[i + up][j + right] = state[i][j]
        state[i][j] = 'x'
        return state

def move_bishop(i, j, state):
    legal_moves = ['NE', 'NW', 'SE', 'SW']
    states = []
    for move in legal_moves:
        states.append(move_to_final_state(move_dict[move], i, j, state))
    return states

def move_queen(i, j, state):
    legal_moves = ['N', 'S', 'E', 'W', 'NE', 'NW', 'SE', 'SW']
    states = []
    for move in legal_moves:
        x = move_to_final_state(move_dict[move], i, j, copy.deepcopy(state))
        print(move)
        pprint(x)
        states.append(x)
    return states

def move_rook(i, j, state):
    legal_moves = ['N', 'S', 'E', 'W']
    states = []
    for move in legal_moves:
        states.append(move_to_final_state(move_dict[move], i, j, state))
    return states

def move(i, j, state):
    piece = state[i][j][0]
    states = []
    if(piece == 'Q'):
        return move_queen(i, j, state)
    elif(piece == 'R'):
        move_rook(i, j, state)
    elif(piece == 'B'):
        move_bishop(i, j, state)


def main(argv):
    search_type = argv[0]
    init_file = argv[1]
    n_actions = int(argv[2])

    f = open(init_file, "r")
    n = f.readline()
    n1 = int(n.split(' ')[0])
    
    initial_state = []
    for i in range(n1):
        line = f.readline()
        tokens = line.split(' ')
        initial_state.append([token.replace('\n', '') for token in tokens])
    
    move_queen(2, 2, initial_state)

if __name__ == '__main__':
    main(sys.argv[1:])