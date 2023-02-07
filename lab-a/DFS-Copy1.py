
import numpy as np
from collections import namedtuple
import argparse
import sys
import copy


def load_file(file):
    data = []
    with open(file) as f:
        data = f.readlines()
    return data

State = namedtuple('State',['position','cheese'])

class Domain:

    def __init__(self, data):
        self.data = data

    def count_rows(self):#removing ,data as an imput
        rows=0
        for i in range(len(self.data)):
            rows+=1
        return rows

    def count_columns(self):#removing ,data as an imput
        for rows in self.data:
            columns=0
            for i in rows:
                if columns != '/' or columns !='n':
                    columns+=1
        return columns

    def create_maze(self):#removing ,data as an imput
        i=0
        for lines in self.data:
            j=0
            for char in lines:
                if char != '/' or char !='n':
                    if char =='%':
                        maze[i][j]=1
                    elif char ==' ':
                        maze[i][j]=0
                    elif char == 'P':
                        maze[i][j]=2
                    elif char == '.':
                        maze[i][j]=3
                j+=1
            i+=1

        return maze

    def starting_point(self):#data is the putput of the load file#removing ,data as an imput
        maze = self.create_maze()
        a = np.array(maze)
        b = np.where(a==2)
        d = np.where(a==3)
        cheese = []
        starting = []
        for i in d:
            cheese.append(i[0])
        for i in b:
            starting.append(i[0])
        state = State((starting[0],starting[1]),cheese)

        return state


    def prize_point(self):
        maze = self.create_maze()
        a = np.array(maze)
        b = np.where(a==3)
        first = []
        second = []
        for i in b:
            first.append(i[0])
        second.append((first[0],first[1]))
        return second

    def wall(self):
        maze = self.create_maze()
        a = np.array(maze)
        b = np.argwhere(a==1)
        walls = []
        for i in b:
            walls.append((i[0],i[1]))
        return walls

    def space(self):
        maze = self.create_maze()
        a = np.array(maze)
        b = np.argwhere(a==0)
        spaces = []
        for i in b:#coordinates where a==0
            spaces.append((i[0],i[1]))
        return spaces

    def everything(self):
        space = self.space()
        cheeses =  self.prize_point()
        everything = space + cheeses
        return everything

def starting_state(maze):#output from function of domain create maze


    a = np.array(maze)
    initial_pos = np.where(a==2)
    cheese_pos = np.where(a==3)

    cheese = []
    starting = []

    for i in initial_pos:
        starting.append(i[0])
    for i in cheese_pos:
        cheese.append(i[0])

    starting_state = State((starting[0],starting[1]),[cheese])

    return starting_state

def transition_state(maze,state,direcion):

    Empty_spaces = Domain(maze).everything()
    Walls_list = Domain(maze).wall()
    starting_point = state[0]

    cheeses = copy.deepcopy(state[1])
    Position_check = []#copy.deepcopy(state[0])
    new_positions = []


    for i in starting_point:#initial position check
        Position_check.append(i)

    if direcion == "W":#west In case we need to use Direction.upper()
        for mov in Empty_spaces:#mov in empty_spaces
            if (Position_check[0],Position_check[1]-1) == mov:#update for new position
                new_positions.append(mov)#append new position to list of new positions
            if (Position_check[0],Position_check[1]-1)in state[1]:
                state[1].pop()

        for mov in Walls_list:#mov in walls list
            if (Position_check[0],Position_check[1]-1) == mov:
                print("there is a wall here, can't move")

    if direcion == "S":
        for mov in Empty_spaces:
            if (Position_check[0]+1,Position_check[1]) == mov:
                new_positions.append(mov)
            if (Position_check[0]+1,Position_check[1]) in state[1]:
                state[1].pop()

        for mov in Walls_list:
            if (Position_check[0]+1,Position_check[1]) == mov:
                print("there is a wall here, can't move")


    if direcion == "N":
        for mov in Empty_spaces:
            if (Position_check[0]-1,Position_check[1]) == mov:
                new_positions.append(mov)
            if (Position_check[0]-1,Position_check[1])in state[1]:
                state[1].pop()
        for mov in Walls_list:
            if (Position_check[0]-1,Position_check[1]) == mov:
                print("there is a wall here, can't move")


    if direcion == "E":
        for mov in Empty_spaces:
            if (Position_check[0],Position_check[1]+1) == mov:
                new_positions.append(mov)
            if (Position_check[0],Position_check[1]+1)in state[1]:
                state[1].pop()

        for mov in Walls_list:
            if (Position_check[0],Position_check[1]+1) == mov:
                print("there is a wall here, can't move")
    new_state = State(new_positions,state[1])
    return new_state

def goal_test(state):
    return len(state[1])==0


def successor_function(state):#only valid set of instructions
    empty_spaces = Domain(maze).everything()#changed this from space() to possible_mov()
    walls_list = Domain(maze).wall()
    cheese = copy.deepcopy(Domain(maze).prize_point())
    starting_point = state[0]
    Position_check = []
    sucessful_states = []


    for i in starting_point:#initial position check
        Position_check.append(i)

    if (Position_check[0],Position_check[1]-1) in empty_spaces:#west
        cheese = copy.deepcopy(Domain(maze).prize_point())
        if (Position_check[0],Position_check[1]-1) == cheese[0]:
            cheese.pop()
        west_state = State((Position_check[0],Position_check[1]-1),cheese)
        sucessful_states.append("W")
        sucessful_states.append(west_state)

    if (Position_check[0]+1,Position_check[1]) in empty_spaces:#south
        cheese = copy.deepcopy(Domain(maze).prize_point())
        if (Position_check[0]+1,Position_check[1]) == cheese[0]:
            cheese.pop()
        south_state = State((Position_check[0]+1,Position_check[1]),cheese)
        sucessful_states.append("S")
        sucessful_states.append(south_state)

    if (Position_check[0],Position_check[1]+1) in empty_spaces:
        cheese = copy.deepcopy(Domain(maze).prize_point())
        if (Position_check[0],Position_check[1]+1) == cheese[0]:
            cheese.pop()
        east_state = State((Position_check[0],Position_check[1]+1),cheese)
        sucessful_states.append("E")
        sucessful_states.append(east_state)

    if (Position_check[0]-1,Position_check[1]) in empty_spaces:
        cheese = copy.deepcopy(Domain(maze).prize_point())
        if (Position_check[0]-1,Position_check[1]) == cheese[0]:
            cheese.pop()
        north_state = State((Position_check[0]-1,Position_check[1]),cheese)
        sucessful_states.append("N")
        sucessful_states.append(north_state)


    return sucessful_states#Direction 0,2,4,6 #It is a string



######NODE CLASS
class Node:
    __slots__ = '_state','_move','_parent'
    def __init__(self, state=None, move=None, parent=None):
            self._state = state
            self._parent = parent#who is my parent
            self._move = move#what move was taken to get to me


    def get_state(self):
        return self._state
    def get_parent(self):
        return self._parent
    def get_move(self):
        return self._move


    def set_state(self,new_state):
        self._state = new_state
    def set_parent(self,new_parent):
        self._parent = new_parent
    def set_move(self,new_move):
        self._move = new_move


def DFS(state):

    curr_node = Node(state)
    stack = []#operations append()/ push() pop()/pop()
    parents = []
    stack.append(curr_node)
    curr_node = stack.pop()
    count = 0
    while goal_test(curr_node.get_state())!=True:
        count+=1

        list_of_children = successor_function(curr_node.get_state())
        i = 0
        while i <len(list_of_children):
            new_node_1= Node()
            new_node_1.set_move(list_of_children[i])
            new_node_1.set_state(list_of_children[i+1])
            new_node_1.set_parent(curr_node)
            if new_node_1.get_state() not in parents:
                stack.append(new_node_1)
            i+=2
        curr_node = stack.pop()
        parents.append(curr_node.get_state())
    print("All nodes expanded:", count)
    return curr_node

def track_path(node):
    curr = node
    path = []
    while curr.get_parent()!=None:
        path.append(curr.get_state()[0])
        curr = curr.get_parent()
    return path


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process file.')#Create argument paser object
    parser.add_argument('m',help='maze file')#Create first file argument
    args = parser.parse_args()

###Syntax of the maze
    load = load_file(args.m)
    d = Domain(load)
    rows = d.count_rows()
    columns = d.count_columns()
    maze = [[0 for i in range(columns)] for j in range (rows)]
    Maze_created = d.create_maze()
###Transition State Information
    state = starting_state(Maze_created)
    # state = State((5,9),[18,9])
    Transition = transition_state(Maze_created,state,"S")
    goal = goal_test(Transition)
    success = successor_function(state)
###DFS
    dfs= DFS(state)
    path = track_path(dfs)
    print("Nodes expanded for path:",len(path))

    def start(maze):
        string = ''
        for i in range(len(maze)):
            for j in range(len(maze[0])):
                if maze[i][j] == 1:
                    string = string + '%'
                elif maze[i][j] == 3:
                    string = string + '.'
                elif maze[i][j] == 2:
                    string = string + 'P'
                else:
                    string = string + ' '
            string = string + '%' + '\n'
        return(string)    
    def final_maze():
        string = ''
        full = []
        num = len(d.prize_point())
        for i in path:
            if maze[i[0]][i[1]] == 3:
                maze[i[0]][i[1]] = str(num)
                num -=1
            else:
                maze[i[0]][i[1]] = '#'
        for i in range(len(maze)):
            for j in range(len(maze[0])):
                if maze[i][j] == 1:
                    string = string + '%'
                elif maze[i][j] == '#':
                    string = string + str(maze[i][j])
                elif maze[i][j] == 3:
                    string = string + 'C'
                elif maze[i][j] == 2:
                    string = string + 'P'
                elif maze[i][j] == 0:
                    string = string + ' '
                else:
                    string = string + str(maze[i][j])
            string = string + '%' + '\n'
        return(string)
    print(start(Maze_created))
    print(final_maze())
