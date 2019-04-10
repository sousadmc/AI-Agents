#
from search import *
# TAI content
def c_peg ():
    return "O"

def c_empty ():
    return "_"

def c_blocked ():
    return "X"

def is_empty (e):
    return e == c_empty()

def is_peg (e):
    return e == c_peg()

def is_blocked (e):
    return e == c_blocked()

# TAI pos
# Tuplo (l, c)
def  make_pos (l, c):
    return (l, c)

def pos_l (pos):
    return pos[0]

def pos_c (pos):
    return pos[1]


# TAI move
# Lista [p_initial, p_final]
def make_move (i, f):
    return [i, f]

def move_initial (move):
    return move[0]

def move_final (move):
    return move[1]

def board_moves(board):
    moves = []
    for e in range(0,len(board)):
        for i in range(0,len(board[e])):
            
            if i < (len(board[e])-2) and is_peg(board[e][i]) and is_peg(board[e][i+1]) and is_empty(board[e][i+2]):
                c = make_pos(e,i)
                n = make_pos(e,i+2)
                moves += [[c,n]]
                
            if e < (len(board)-2) and is_peg(board[e][i]) and is_peg(board[e+1][i]) and is_empty(board[e+2][i]):
                c = make_pos(e,i)
                n = make_pos(e+2,i)
                moves += [[c,n]] 

                
            if  i > 1 and is_peg(board[e][i]) and is_peg(board[e][i-1]) and is_empty(board[e][i-2]):
                c = make_pos(e,i)
                n = make_pos(e,i-2)
                moves += [[c,n]]

                
            if e > 1 and is_peg(board[e][i]) and is_peg(board[e-1][i]) and is_empty(board[e-2][i]):
                c = make_pos(e,i)
                n = make_pos(e-2,i)
                moves += [[c,n]]

    return moves

def board_perform_move(board,move):
    board_final = [e[:] for e in board]
    
    ini = move[0]
    fin = move[1]
    
    board_final[move[0][0]][move[0][1]] = '_'
    board_final[move[1][0]][move[1][1]] = 'O'  
    
    if fin[0] == (ini[0]+2):
        board_final[move[0][0]+1][move[0][1]] = '_'        
        
    if fin[0] == (ini[0]-2):
        board_final[move[0][0]-1][move[0][1]] = '_'        
        
    if fin[1] == (ini[1]+2):
        board_final[move[0][0]][move[0][1]+1] = '_'        
    
    if fin[1] == (ini[1]-2):
        board_final[move[0][0]][move[0][1]-1] = '_'        
        
    return board_final


def peg_block(board, position):
    ln = position[0]
    col = position[1]

    if ln > 1 and board[ln-1][col] == 'O' and board[ln-2][col] == '_':
        return 0
    
    if ln < len(board)-2 and board[ln+1][col] == 'O' and board[ln+2][col] == '_':
        return 0
    
    if col > 1 and board[ln][col-1] == 'O' and board[ln][col-2] == '_':
        return 0 
    
    if col < len(board[ln])-2 and board[ln][col+1] == 'O' and board[ln][col+2] == '_':
        return 0 
    
    return 1

def blocked_peg(board):
    s = 0
    for e in range(0,len(board)):
        for i in range(0,len(board[e])):
            if is_peg(board[e][i]) and peg_block(board, (e,i)) == 1:
                s += 1
    return s    

def board_peg(board):
    s = 0
    for e in range(0,len(board)):
        for i in range(0,len(board[e])):
            if board[e][i] == 'O':
                s += 1
    return s
    

class sol_state:
    
    def __init__(self,b):
        self.board = b
        self.moves = board_moves(b)
        self.num_board_peg = board_peg(b)
    
    def __lt__(self, other_sol_state):
        return self.num_board_peg > other_sol_state.num_board_peg
    
class solitaire(Problem):
    
    def __init__(self, board):
        super(Problem, self).__init__()
        self.initial = sol_state(board)
        self.goal = 1
        
    def actions(self, state):
        return board_moves(state.board)
        
    def result(self, state, action):
        return sol_state(board_perform_move(state.board, action))
        
    def goal_test(self, state):
        return state.num_board_peg == self.goal
 
        
    def path_cost(self, c, state1, action, state2):
        return c + 1
        
    def h(self, node): 
        
        return (((node.state.num_board_peg) + blocked_peg(node.state.board)))
    