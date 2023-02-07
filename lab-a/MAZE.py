
import numpy as np
from collections import namedtuple
import argparse
import sys
import copy
from sys import maxsize


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
        # State = namedtuple('State',['position','cheese'])
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

    def prize_point(self):#
        maze = self.create_maze()

        a = np.array(maze)
        b = np.where(a==3)
        prize = []

        for i in b:
            prize.append(i[0])

        return prize

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

    Empty_spaces = Domain(maze).space()
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
    empty_spaces = Domain(maze).space()
    walls_list = Domain(maze).wall()
    starting_point = state[0]
    Position_check = []
    sucessful_states = []


    for i in starting_point:#initial position check
        Position_check.append(i)

    if (Position_check[0],Position_check[1]-1) in empty_spaces:#west

        west_state = State((Position_check[0],Position_check[1]-1),state[1])
        sucessful_states.append(west_state)

    if (Position_check[0]+1,Position_check[1]) in empty_spaces:#south
        south_state = State((Position_check[0]+1,Position_check[1]),state[1])
        sucessful_states.append(south_state)

    if (Position_check[0]-1,Position_check[1]) in empty_spaces:
        north_state = State((Position_check[0]-1,Position_check[1]),state[1])
        sucessful_states.append(north_state)

    if (Position_check[0],Position_check[1]+1) in empty_spaces:
        east_state = State((Position_check[0],Position_check[1]+1),state[1])
        sucessful_states.append(east_state)

    return sucessful_states

def createStack():
    stack = []
    return stack

def isEmpty(stack):
    return len(stack) == 0

def push(stack, item):
    stack.append(item)
    
def pop(stack):
    if (isEmpty(stack)):
        return str(-maxsize -1) # return minus infinite
     
    return stack.pop()


def depth_for_search():
    
    stack = createStack()
    
    start = starting_state(Maze_created)
    #cheese = Domain(maze).prize_point()
    Transition = transition_state(Maze_created,start,"S")
    goal = goal_test(Transition)
    
    

    #forward = [start]
    #explored = []
    
    #while goal != True:
     #   for i in range(556):
      #      if successor_function(forward[-1])[0] != None:
       #         if successor_function(forward[-1])[0] in explored:
        #            if successor_function(forward[-1])[1] in explored:
         #               forward.append(successor_function(forward[-1])[2])
          #              explored+=[forward[-2]]
           #             parent = forward.remove(forward[-2])
            #        else:
             #           forward.append(successor_function(forward[-1])[1])
              #          explored+=[forward[-2]]
               #         parent = forward.remove(forward[-2])


                #else:
                 #   forward.append(successor_function(forward[-1])[0])
                  #  explored+=[forward[-2]]
                   # parent = forward.remove(forward[-2])
            
                    
        #return (forward,'yes',explored)


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
    Transition = transition_state(Maze_created,state,"S")
    goal = goal_test(Transition)
    succes = successor_function(state)
    