import collections
import ctypes
from multiprocessing import Process as _Process, Array as _Array
import numpy as _np

MAX_COST = 100000

class SimpleGraph:
    def __init__(self):
        self.edges = {}
    
    def neighbors(self, xy):
        return self.edges[xy]

class SquareGrid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.obstacles = [] #list of x,y coordinates
    
    def in_bounds(self, xy):
        (x, y) = xy
        return 0 <= x < self.width and 0 <= y < self.height
    
    def passable(self, xy):
        #print "Obstacles: ", xy, self.obstacles
        return xy not in self.obstacles
    
    def neighbors(self, xy):
        (x, y) = xy
        results = [(x+1, y), (x, y-1), (x-1, y), (x, y+1)]
        if (x + y) % 2 == 0: results.reverse() # aesthetics
        #print "Neighbours at ", results
        results = filter(self.in_bounds, results)
        #print "Neighbours that are inbounds: ", results
        results = filter(self.passable, results)
        print "Neighbours that we can go to: ", results
        return results

    def pad_arr(vector, pad_width, iaxis, kwargs):
        vector[:pad_width[0]] = 0
        vector[-pad_width[1]:] = 0
        return vector

    def cost(self, from_node, to_node):
        if self.passable(to_node): return 1
        return 1000

import heapq
class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self):
        return heapq.heappop(self.elements)[1]



def heuristic(a, b, _type='manhattan'):
    D=1
    (x1, y1) = a
    (x2, y2) = b
    dx = abs(x1 - x2)
    dy = abs(y1 - y2)
    if _type == 'manhattan':
        return D * (dx + dy)
    elif _type == 'diagonal':
        D2 = 1
        return D * (dx + dy) + (D2 - 2 * D) * min(dx, dy) 
    elif _type == 'euclidean':
        return D * (dx*dx + dy*dy)

def reconstruct_path(came_from, start, goal):
    current = goal
    path = [current]
    while current != start:
        current = came_from[current]
        path.append(current)
        path.reverse()
   
    #print "Path:", path
    return path[1]

def a_star_search(result, grid, start, goal):
    print "Starting at ", start 
    print "Goal at ", goal 
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0
    
    while not frontier.empty():
        current = frontier.get()
        
        if current == goal:
            #print "At goal, break"
            break
        
        for next in grid.neighbors(current):
            new_cost = cost_so_far[current] + grid.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(goal,  next)
                frontier.put(next, priority)
                came_from[next] = current
 
    result[0] = 0
    result[1] = 0
    result[2] = MAX_COST 

    try:
        #print "Came from = {}, start = {}, goal = {}".format(came_from, start, goal)
        print "Valid path = {}".format(len(came_from) > 1)
        if len(came_from) > 1:
            (x,y) = reconstruct_path(came_from, start, goal)
            result[0] = x
            result[1] = y
            result[2] = cost_so_far[goal]
    except:
        print "Error occured"
        


def ping(grid, curr_pos, goals):
    
    shared_array_base = _Array(ctypes.c_int, len(goals)*3)
    result = _np.ctypeslib.as_array(shared_array_base.get_obj())
    result = result.reshape(len(goals), 3)
  
    #result = [ a_star_search([0,0,0], grid, current, goal) for goal in goals ]
    #processes = [ _Process(target=a_star_search, args=(result, grid, current, goal)) ]

    processes = [ _Process(target=a_star_search, args=(result[i], grid, curr_pos, goal)) for i, goal in enumerate(goals) ]
    
    
    for p in processes:
        p.start();

    for p in processes:
        p.join();
    
    print "Results:", result
    valid = grid.neighbors(curr_pos)
    cost = MAX_COST #result[0][2] 
    index = -1
    for i,x in enumerate(result):
        if x[2] < cost and x[2] > 0 and (x[0],x[1] in valid):
            cost = x[2]
            index = i
   
    if index == -1:
         print "Uh oh! Couldn't find anything"
         next_move = neighbours(curr_pos)[0] 
    else:
         next_move = (result[index][0], result[index][1]) 
    
    move = get_dir(curr_pos, next_move) 
  
    return move

def get_dir(a,b):
    (x1, y1) = a
    (x2, y2) = b

    print "Going {} to {}".format(a,b)

    if x1 == x2:
        if y1 < y2: return "up"
        else: return "down"
    else:
        if x1 < x2: return "right"

    return "left"

def get_move(grid, curr_pos, food):
    move = ping(grid, curr_pos, food) 
    print "Moving to: ", move
    return move

