from collections import namedtuple
import argparse
import copy
import random
import math

State = namedtuple('State',['position','player'])

class Queue:
    def __init__ (self):
        self._data = []
        self._size = 0
    def __len__(self):
        return self._size
    def is_empty(self):
        return self._size == 0
    def enqueue(self, item):
        self._size+=1
        self._data.append(item)
    def dequeue(self):
        self._size-=1
        return self._data.pop(0)
    def info(self):
        return self._data


def initial_state(rows,columns,pieces):
    Size = columns * (pieces)
    rest = (rows - pieces*2) * columns
    X = []
    X2 = []
    Spaces = []
    Spaces2 = []
    O = []
    O2 = []
    Board = []

    for i in range (Size):
        X.append('X')
        O.append('O')
    for i in range ((pieces)):
        X2.append(X[i*columns:(i+1) * columns])
        O2.append(O[i*columns:(i+1) * columns])
    for j in range (rest):
        Spaces.append('.')
    for i in range (rows - pieces*2):
        Spaces2.append(Spaces[i*columns:(i+1) * columns])
    for i in range(pieces):
        Board.append(X2[i])
    for i in range (rows - pieces*2):
        Board.append(Spaces2[i])
    for i in range(pieces):
        Board.append(O2[i])
    starting_state = State(Board,"W")
    return  starting_state

def display_state(state):
    return state[0]

def white_pieces(state):
    white=[]
    black = []
    board = state[0]
    for rows in range (len(board)):
        for cols in range(len(board[0])):
            if board[rows][cols]== 'O':
                piece = []
                piece.append(rows)
                piece.append(cols)
                piece_tuple = tuple(piece)
                white.append(piece_tuple)
    return white#list of tuple locations

def black_pieces(state):
    black = []
    board = state[0]
    for rows in range (len(board)):
        for cols in range(len(board[0])):
            if board[rows][cols]== 'X':
                piece = []
                piece.append(rows)
                piece.append(cols)
                piece_tuple = tuple(piece)
                black.append(piece_tuple)
    return black #list of tuple locations in the board

def game_ending(state):
    count = 0
    Board = display_state(state)

    for i in range(len(state[0])):
        if "O" not in (state[0][i]):
            count+=1
    count = 0
    for i in range(len(state[0])):
        if "X" not in (state[0][i]):
            count+=1
    if count == len(state[0]):
        return True
    for j in range(len(state[0])):
        if Board[0][j-1] == 'O' or Board[(len(state[0])-1)][j-1] == 'X':
            return True

def move_generator(state):
    black = black_pieces(state)
    white = white_pieces(state)
    actions = {}
    if game_ending(state)==True:
        return actions#"The game has ended no further moves to generate"
    if state[1]== "W":
        for pos in white:#pos is an tuple in the list of tuples
#####Check for Obstruction
            check = (pos[0]-1, pos[1])#checks if there is a white piece ifront
            ck = (pos[0]-1, pos[1]-1)#diagonal
            ck_2 = (pos[0]-1, pos[1]+1)#diagonal
#####Check for Out of bound
            check_2 = pos[1]-1#out of bound to the left
            check_3 = pos[1]+1#out of bound to the right
            if check in white and ck in white and ck_2 in white:
                continue
            if check_2<0:
                actions[pos]=[(pos[0]-1, pos[1]),(pos[0]-1, pos[1]+1)]
            elif check_3>=len(state[0]):
                actions[pos]=[(pos[0]-1, pos[1]),(pos[0]-1, pos[1]-1)]
            else:
                actions[pos]=[(pos[0]-1, pos[1]),(pos[0]-1, pos[1]-1),(pos[0]-1, pos[1]+1)]
    if state[1]== "B":
        for pos in black:
#####Check for Obstruction
            check = (pos[0]+1, pos[1])
            ck = (pos[0]+1, pos[1]-1)#diagonal
            ck_2 = (pos[0]+1, pos[1]+1)#diagonal
#####Check for Out of bound
            check_2 = pos[1]-1#out of bound to the left
            check_3 = pos[1]+1#out of bound to the right
            if check in black and ck in black and ck_2 in black:
                continue
            if check_2<0:
                actions[pos]=[(pos[0]+1, pos[1]),(pos[0]+1, pos[1]+1)]
            elif check_3>=len(state[0]):
                actions[pos]=[(pos[0]+1, pos[1]),(pos[0]+1, pos[1]-1)]
            else:
                actions[pos]=[(pos[0]+1, pos[1]),(pos[0]+1, pos[1]-1),(pos[0]+1, pos[1]+1)]
    return actions

def transitional(state,piece,action):
    Board = copy.deepcopy(state[0])
    if Board[piece[0]][piece[1]] == 'X' and state[1] =='B':
        if action[0] == piece[0]+1:
            if action[1] == piece[1]-1 or action[1] == piece[1]+1 or action[1] == piece[1]:
                if  Board[action[0]][action[1]] == '.':
                    Board[action[0]][action[1]] = 'X'
                    Board[piece[0]][piece[1]] = '.'

                elif Board[action[0]][action[1]] == 'O':
                    Board[action[0]][action[1]] = 'X'
                    Board[piece[0]][piece[1]] = '.'

        new_state = State(Board,"W")
        return new_state

    elif Board[piece[0]][piece[1]] == 'O' and state[1] == 'W':
        if action[0] == piece[0]-1:
            if action[1] == piece[1]-1 or action[1] == piece[1]+1 or action[1] == piece[1]:
                if  Board[action[0]][action[1]] == '.':
                    Board[action[0]][action[1]] = 'O'
                    Board[piece[0]][piece[1]] = '.'
                elif Board[action[0]][action[1]] == 'X':
                    Board[action[0]][action[1]] = 'O'
                    Board[piece[0]][piece[1]] = '.'
        new_state = State(Board,"B")
        return new_state


class Node:
    def __init__(self,state):
        self.parent = None
        self.child = []
        self.action = None
        self.state = state
        self.utility = None
        self.depth = 0

    def get_parent(self):
        return self.parent
    def get_child(self):
        return self.child
    def get_action(self):
        return self.action
    def get_state(self):
        return self.state
    def get_utility(self):
        return self.utility
    def get_depth(self):
        return self.depth
    def set_parent(self,new_parent):
        self.parent = new_parent
    def set_action(self,new_action):
        self.action = new_action
    def set_depth(self,d):
        self.depth = d
    def set_child(self,list_kids):
        self.child=list_kids
    def set_utility(self, n):
        self.utility = n

Q = Queue()

def evasive_utility(state):
    Board = state[0]
    count = 0
    number = [0,1]
    if state[1] == 'W':
        for i in range (len(Board)):
            for j in range (len(Board)):
                if Board[i][j] == "O":
                    count += 1
        random_ = (random.choice(number))
        return (count + random_)

    if state[1] == 'B':
        for i in range (len(Board)):
            for j in range (len(Board)):
                if Board[i][j] == "O":
                    count += 1
        random_ = (random.choice(number))
        return (count + random_)


def create_tree(state, depth, utility):#three options for utility Evasive, Conquer, Kill
    curr_node = Node(state)
    Q.enqueue(curr_node)

    while Q.is_empty()==False:#game_ending(state)==False:
        curr_node = Q.dequeue()

        if curr_node.get_depth()==depth:#check if node expaned is at maximum depth
            if utility == "E":
                val = evasive_utility(curr_node.get_state())
                curr_node.set_utility(val)
            # elif utility == "Conquer":
            #     val = Conquer_utility(curr_node.get_state())
            #     curr_node.set_utility(val)
                continue

        possible_actions=move_generator(curr_node.get_state())
        if len(possible_actions)==0:
            continue
        all_keys = list(possible_actions.keys())
        child = []
        keys = 0

        while keys <len(all_keys):
            #child nodes depth is parents node +=1
            current_vals = list(possible_actions.values())#takes the amount of childs in the specific key
            n_kids = len(current_vals[keys])#how many kids are there for a specific key

            for i in range (n_kids):
                new_state = transitional(curr_node.get_state(),all_keys[keys],current_vals[keys][i])
                new_node = Node(new_state)#I need to feed a new state #the index of the children
                new_node.set_parent(curr_node)
                new_node.set_depth(curr_node.get_depth()+1)#one more than parent might have to change this
                new_node.set_action(current_vals[keys][i])# new_node.set_action(node)####IMPORTANT FIGURE THIS OUT
                child.append(new_node)#list comprehension
#                 print("new node_state",new_node.get_state())
                Q.enqueue(new_node)
            keys+=1
            curr_node.set_child(child)#set children inside of the node
#         print("children",curr_node.get_child())
    return curr_node#last children
def get_root(node):
    while node.get_parent()!=None:
        node = node.get_parent()
    return node#root node of populated tree
#########################################################
def traverse_tree(root,maxplayer):

    if root.get_utility()!= None:
        return (root.get_utility(),root.get_state())

    if maxplayer == True:
        max_val = -100000000000000000
        max_child = None
        for child in root.get_child():
            util_val,util_child = traverse_tree(child,False)
            if max_val<util_val:
                max_val = util_val
                max_child = child
        root.set_utility(max_val)
        return (max_val, max_child.get_state())
    else:
        min_val = 100000000000000000
        min_child = None
        for child in root.get_child():
            util_val, util_child = traverse_tree(child,True)
            if util_val< min_val:
                min_val = util_val
                min_child = child
        root.set_utility(min_val)
        return (min_val, min_child.get_state())

def Conqueror_utility(state):
    Board = state[0]
    count = 0
    number = [0,1]
    if state[1] == 'W':
        for i in range (len(Board)):
            for j in range (len(Board)):
                if Board[i][j] == "X":
                    count += 1
        random_ = (random.choice(number))
        return ((0-count) + random_)

    if state[1] == 'B':
        for i in range (len(Board)):
            for j in range (len(Board)):
                if Board[i][j] == "O":
                    count += 1
        random_ = (random.choice(number))
        return ((0-count) + random_)

def hurdle_utility(state):
    Board = state[0]
    count = 0
    number = [0,1]
    value = []
    if state[1] == 'W':
        for i in range (len(Board)):
            for j in range (len(Board)):
                if Board[i][j] == "O":
                    value.append(i)

        random_ = (random.choice(number))
        return (min(value) + random_ )

    if state[1] == 'B':
        for i in range (len(Board)):
            for j in range (len(Board)):
                if Board[i][j] == "X":
                    value.append((len(Board)-1)-i)
        random_ = (random.choice(number))
        return (min(value) + random_)

def fortification_utility(state):
    Board = state[0]
    count = 0
    number = [0,1]
    value = []
    if state[1] == 'W':
        for i in range (len(Board)):
            for j in range (len(Board)):
                if Board[i][j] == "O":
                    value.append(i)

        random_ = (random.choice(number))
        return (max(value) + random_ )

    if state[1] == 'B':
        for i in range (len(Board)):
            for j in range (len(Board)):
                if Board[i][j] == "X":
                    value.append((len(Board)-1)-i)
        random_ = (random.choice(number))
        return (max(value) + random_)

def play_game(heuristic_white, heuristic_black, board_state):

    new_state = board_state

    while game_ending(new_state) != True:
        if new_state[1] == 'W':
            tree = create_tree(new_state,1,heuristic_white)
            root = get_root(tree)
            val, child = traverse_tree(root,True)

            new_state = State (child[0],'B')

        elif new_state[1] == 'B':
            tree = create_tree(new_state,1,heuristic_black)
            root = get_root(tree)
            val, child = traverse_tree(root,True)
            new_state = State (child[0],'W')


        print ((new_state))
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process file.')#Create argument paser object
    # parser.add_argument('m',help='teaseing')#Create first file argument
    args = parser.parse_args()

    initial_state = initial_state(8,8,2)
    # move = move_generator(initial_state)
    # print("Possible moves for player",move)
    # tran = transitional(initial_state,(6,0),(5,1))
    # termination = game_ending(initial_state)
    # print(termination)
    ####### Test for game_ending
    # l = initial_state[0][0]
    # l.insert(0,'O')
    # l.pop()
    # initial_state[0][0]=l
    # print(initial_state)
    # termination = game_ending(initial_state)
    # print(termination)
    ####test for tree
    tree = create_tree(initial_state,3,"E")
    # print(tree)
    rt = get_root(tree)
    # print(rt.get_state())
    traverse = traverse_tree(rt,True)
    # print(traverse)
    play = play_game("E","E",initial_state)
    print(play)
