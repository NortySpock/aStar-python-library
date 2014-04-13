from __future__ import print_function
from random import randrange
from copy import deepcopy
import heapq

def manhattan_distance(x1, y1, x2, y2):
    return (abs(x1-x2) + abs(y1-y2))

def is_inside_map(x,y,cost_map):
  max_x = len(cost_map)
  max_y = len(cost_map[0])
  if(0 <= x < max_x and 0 <= y < max_y):
    return True
  else:
    return False

def is_valid_move(x,y,cost_map):
  if(is_inside_map(x,y,cost_map) and cost_map[x][y] != -1):
    return True
  else:
    return False

def apply_tuple_to_cost_map(tup,cost_map):
  #tuple format is (x,y,cost)
  #coordinates outside cost_map are warned and ignored
  if(is_inside_map(tup[0],tup[1],cost_map)):
    cost_map[tup[0]][tup[1]] = tup[2]
  else: print("Cannot apply tuple at ("+str(tup[0])+","+str(tup[1])+")")

def apply_list_of_tuples_to_cost_map(list_in,cost_map):
  for i in list_in:
    apply_tuple_to_cost_map(i,cost_map)



def number_of_tiles_on_rectangular_map(map_in):
  return (len(map_in)*len(map_in[0]))


# returns a list of xy tuples that are a path from here to there
#this does not take into account obstacles
def naive_path(from_x,from_y,to_x,to_y):

    the_path = []
    from_pos = [from_x, from_y]
    to_pos = [to_x,to_y]
    curr_pos = from_pos
    done = False

    #idiot check
    if curr_pos == to_pos:
      done = True

    while not done:
      #calculate rise over run delta:
      run_delta = abs(curr_pos[0] - to_pos[0])
      rise_delta = abs(curr_pos[1] - to_pos[1])

      if(rise_delta > run_delta): #move vertically
      #(0,0) is top left, (40,20) is bottom right
        if (curr_pos[1] < to_pos[1]): #above target, move down
          curr_pos[1] = curr_pos[1] + 1
        else: #below target, move up
          curr_pos[1] = curr_pos[1] - 1
      else: #move horizontally
        if(curr_pos[0] < to_pos[0]): # left of target, move right
          curr_pos[0]  = curr_pos[0] + 1
        else: # right of target, move left
          curr_pos[0] = curr_pos[0] - 1
      the_path.append((curr_pos[0], curr_pos[1]))

      if curr_pos == to_pos:
        done = True

    return the_path

def random_detour_path(from_x,from_y,to_x,to_y, cost_map):
    the_path = []
    from_pos = [from_x, from_y]
    to_pos = [to_x,to_y]
    curr_pos = from_pos
    move_pos = from_pos
    done = False
    random_move_counter = 0
    max_random_moves = 10

    #idiot check
    if curr_pos == to_pos:
      done = True

    while not done:
      #calculate rise over run delta:
      run_delta = abs(curr_pos[0] - to_pos[0])
      rise_delta = abs(curr_pos[1] - to_pos[1])
      move_pos = deepcopy(curr_pos) #default to no move.

      if(rise_delta > run_delta): #move vertically
      #(0,0) is top left, (40,20) is bottom right
        if (curr_pos[1] < to_pos[1]): #above target, move down
          move_pos[1] = curr_pos[1] + 1
        else: #below target, move up
          move_pos[1] = curr_pos[1] - 1
      else: #move horizontally
        if(curr_pos[0] < to_pos[0]): # left of target, move right
          move_pos[0]  = curr_pos[0] + 1
        else: # right of target, move left
          move_pos[0] = curr_pos[0] - 1

      while not is_valid_move(move_pos[0], move_pos[1], cost_map) and not done:
        random_move_counter += 1
        print("Suggested move ("+str(move_pos[0])+","+str(move_pos[1])+") found invalid, moving randomly for the "+str(random_move_counter)+"th time.")
        move_pos = deepcopy(curr_pos) #default to no move.
        if random_move_counter > max_random_moves:
          print("Exceeded maximum number of random moves, aborting.")
          done = True
        else:
          direction = randrange(0,4)
          if direction == 0: #north
            move_pos[1] -= 1
          elif direction == 1: #east
            move_pos[0]+= 1
          elif direction == 2: #south
            move_pos[1] += 1
          elif direction == 3: #west
            move_pos[0] -= 1

      if (move_pos != curr_pos): #we actually moved
        the_path.append((move_pos[0], move_pos[1]))

      curr_pos = move_pos #update curr_pos
      if curr_pos == to_pos:
        done = True

    return the_path

def create_manhattan_adjacent_positions(pos_x,pos_y):
  pos_list = []
  pos_list.append([pos_x,pos_y-1]) #north
  pos_list.append([pos_x,pos_y+1]) #south
  pos_list.append([pos_x-1,pos_y]) #west
  pos_list.append([pos_x+1,pos_y]) #east
  return pos_list

def a_star_manhattan_path(from_x,from_y,to_x,to_y, cost_map):
    return_dictionary = {}
    return_dictionary['path'] = []
    if from_x == to_x and from_y == to_y: #if we're looking at the same thing, bail out
      return return_dictionary
    if not is_inside_map(from_x,from_y,cost_map):
      return return_dictionary
    if not is_inside_map(to_x,to_y,cost_map):
      return return_dictionary

    def _f(i):
      return (_g(i) + _h(i, cost_map))

    def _g(i):
      return manhattan_distance(i[0], i[1], from_x, from_y)

    def _h(i, cost_map):
      tile_cost = cost_map[i[0]][i[1]]
      #calculate the cross product for two vectors -- one straight from start to goal and one from curr_pos position.
      #Slightly penalize deviation from "as the crow flies" to focus the search on empty maps.
      cross_prod = abs((i[0]-to_x)*(from_y-to_y) - (from_x-to_x)*(i[1]-to_y))
      divergence_factor = (cross_prod * (1.0/number_of_tiles_on_rectangular_map(cost_map)))
      return ((manhattan_distance(i[0], i[1], to_x, to_y) + tile_cost + divergence_factor))

    from_pos = {}
    from_pos['x'] = from_x
    from_pos['y'] = from_y
    from_pos['tilecost'] = cost_map[from_pos['x']][from_pos['y']]
    from_pos['parent'] = None
    from_pos['f'] = _f((from_pos['x'], from_pos['y']))

    to_pos = {}
    to_pos['x'] = to_x
    to_pos['y'] = to_y
    to_pos['tilecost'] = cost_map[to_pos['x']][to_pos['y']]
    to_pos['parent'] = None
    to_pos['f'] = _f((to_pos['x'], to_pos['y']))


    open_heap = []
    closed_set = set()
    candidate_list = []
    cur_pos = from_pos

    done = False
    safety = 0 #used to make sure we don't grow infinitely due to bug
    heapq.heappush(open_heap, (from_pos['f'],from_pos))
    while not done:

      if not open_heap: #if we ever find that the open list is empty, that means there is no path from here to there, so we're just going to abort
        print("Could not find a valid path from ("+str(from_x)+","+str(from_y)+") to ("+str(to_x)+","+str(to_y)+").")
        return return_dictionary

      safety += 1

      cur_pos_tup = heapq.heappop(open_heap)
      cur_pos = cur_pos_tup[1]
      closed_set.add((cur_pos['x'],cur_pos['y']))

      if(cur_pos['x'] ==  to_pos['x'] and cur_pos['y'] == to_pos['y']):
        done = True
      else:
        candidate_tuples = [(cur_pos['x'] + 1, cur_pos['y']), (cur_pos['x'] - 1, cur_pos['y']), (cur_pos['x'], cur_pos['y'] + 1), (cur_pos['x'], cur_pos['y'] - 1)]
        #validate the candidates.
        for i in candidate_tuples:
          if is_valid_move(i[0],i[1],cost_map) and not (i in closed_set):
            cand_pos = {}
            cand_pos['x'] = i[0]
            cand_pos['y'] = i[1]
            cand_pos['tilecost'] = cost_map[cand_pos['x']][cand_pos['y']]
            cand_pos['parent'] = cur_pos
            cand_pos['f'] = _f((i[0], i[1]))
            heapq.heappush(open_heap, (cand_pos['f'],cand_pos))


      if(safety > (2*number_of_tiles_on_rectangular_map(cost_map))): #If we've gone more than double the iterations as there are squares on the map, we must be lost
        done = True
        print("Hit the safety")
        print("from: ("+str(from_x)+","+str(from_y)+")")
        print("  to: ("+str(to_x)+","+str(to_y)+")")
        print(cur_pos)
        print("closed:")
        print(closed_set)
        print("open:")
        print(open_heap)
        return []


    #so then we have a path, write it back out to the path list
    the_path = []
    while cur_pos['parent'] is not None:
      the_path.append((cur_pos['x'],cur_pos['y']))
      cur_pos = cur_pos['parent']
    the_path.reverse()
    return_dictionary['path'] = the_path

    return_open_and_closed_lists = True
    if return_open_and_closed_lists:
      #need to convert dictionary objects to list of tuples
      open_heap_tuples = []
      for pos in open_heap:
        open_heap_tuples.append((pos[1]['x'],pos[1]['y']))
      closed_list_tuples = []
      for pos in closed_set:
        closed_list_tuples.append(pos)
      return_dictionary['open'] = open_heap_tuples
      return_dictionary['closed'] = closed_list_tuples
    return(return_dictionary)

def print_open_heap(heap_in):
  current_heap_positions = []
  for i in heap_in:
    current_heap_positions.append((i[1]['x'], i[1]['y'], i[1]['f']))
  return str(current_heap_positions)

def pretty_print_map(double_list):
  numcols = len(double_list)    
  colposes = len(double_list[0])
  my_row = ''
  counter = 0
  ones_row = ' '
  tens_row = ' '
  header = "+"
  for i in xrange(numcols):
    ones_row = ones_row + str(counter % 10)
    if(counter % 10 == 0):
      tens_row = tens_row + str(counter / 10)
    else:
      tens_row = tens_row + ' '
    counter = (counter + 1)
    header = header + "-"
  header = header + "+"

  print(tens_row)  
  print(ones_row)
  print(header)
  counter = 0
  for i in xrange(colposes):
    my_row = "|"
    for j in xrange(numcols):
      my_row = my_row + str(double_list[j][i])[0] #just one character, please!
    my_row = my_row + "|" + str(counter)
    counter = (counter + 1) 
    print(my_row)
  print(header)

def populate_grid(grid,list_of_three_tuples):
  max_x = len(grid)
  max_y = len(grid[0])
  if(list_of_three_tuples is not None and len(list_of_three_tuples) > 0):
    for point in list_of_three_tuples:
      if(point[0] >= 0 and point[0] < max_x) and (point[1] >= 0 and point[1] < max_y): #sanity
        grid[point[0]][point[1]] = point[2] # put in value at position (x, y, value)

    
def make_grid(x,y,init=None):
  return [[init]*y for i in xrange(x)]

def create_text_map_from_cost_map(cost_map):
  max_x = len(cost_map)
  max_y = len(cost_map[0])
  text_map = make_grid(max_x,max_y,' ')
  for i in xrange(max_y):
    for j in xrange(max_x):
      if cost_map[j][i] == -1: #impassable
        text_map[j][i] = '#'
      elif cost_map[j][i] == 1: #normal cost
        text_map[j][i] = ' '
      else:
        text_map[j][i] = str(cost_map[j][i])[0] #just store the number
        
  return text_map

def print_list_of_tuples_on_map(in_list, map_char,text_map):
  for pos in in_list:
    text_map[pos[0]][pos[1]] = str(map_char)[0]
  

def replace_in_map(map_in, from_var,to_var):
  max_x = len(map_in)
  max_y = len(map_in[0])
  for i in xrange(max_y):
    for j in xrange(max_x):
      if map_in[j][i] == from_var:
        map_in[j][i] = to_var

def generate_random_cost_map(cost_map,min_cost, max_cost):
  #TODO: either accept a seed number or generate a random seed and print it out to allow user to reproduce maps
  max_x = len(cost_map)
  max_y = len(cost_map[0])
  thing = 0
  
  for y in xrange(max_y):
    for x in xrange(max_x):    
      thing += 1
      cost_map[x][y] = randrange(min_cost,max_cost+1)
      
def generate_random_pos(max_x,max_y):
  return (randrange(0,max_x),randrange(0,max_y))
  
def print_path_on_map(map_in, path_in):
  absolute_iterations = 0
  for path_pos in path_in:
    mod_iter = (absolute_iterations % 26)
    number = ord('a') + mod_iter
    map_in[path_pos[0]][path_pos[1]] = chr(number)
    absolute_iterations += 1

def is_manhattan_adjacent(p1_x,p1_y, p2_x,p2_y):
  if(   (abs(p1_x - p2_x) == 1 and abs(p1_y - p2_y) == 0)
     or (abs(p1_x - p2_x) == 0 and abs(p1_y - p2_y) == 1)):
       return True
  else:
    return False

def print_tile_tuples_from_list_of_dictionaries(list_in):
  printable_list = []
  for thing in list_in:
    printable_list.append((thing['x'],thing['y'],thing['f'],thing['g'],thing['h']))
  print(printable_list)
  

def check_path_for_validity(from_x,from_y,to_x,to_y, path, cost_map):
  if not path:
    print("Path was empty!")
  else:
    prev = [from_x,from_y]
    
    for point in path:
      if not is_valid_move(point[0],point[1],cost_map):
        print("Move to ("+str(point[0])+","+str(point[1])+") is not valid!")
      if not is_manhattan_adjacent(prev[0],prev[1],point[0],point[1]):
        print("Prev pos ("+str(prev[0])+","+str(prev[1])+")"+" and curr pos ("+str(point[0])+","+str(point[1])+") are not adjacent!")
      prev = point
    last = path[-1]
    if last != (to_x,to_y):
      print("Final pos ("+str(last[0])+","+str(last[1])+")"+" is not the target at("+str(to_x)+","+str(to_y)+")!")
      


def fixed_map_wall(cost_map):
  for i in range(5,35): #horizontal wall
    cost_map[i][10] = -1
    
def u_shaped_wall(cost_map):
  for i in range(5,35): #horizontal wall
    cost_map[i][15] = -1
  for i in range(5,15): #vertical
    cost_map[5][i] = -1
    cost_map[35][i] = -1
    
    
def unbreachable_wall(cost_map):
  map_len = len(cost_map)
  for i in range(0,map_len-1):
    cost_map[i][15] = -1
    
