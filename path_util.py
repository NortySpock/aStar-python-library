from random import randrange
from copy import deepcopy

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
  max_x = len(cost_map)
  max_y = len(cost_map[0])
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
    
    def _cross_prod(from_x, from_y, cur_x, cur_y, to_x, to_y):
      cross_prod = abs((cur_x-to_x)*(from_y-to_y) - (from_x-to_x)*(cur_y-to_y))
      return cross_prod
    
    def _h(i, cost_map):
      tile_cost = cost_map[i[0]][i[1]]
      #calulate the cross product for two vectors -- one straight from start to goal and one from curr_pos position. 
      #Slightly penalize deviation from "as the crow flies" to focus the search on empty maps.
      divergence_factor = (_cross_prod(from_x, from_y, i[0], i[1], to_x, to_y) * (1.0/number_of_tiles_on_rectangular_map(cost_map)))
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
    

    

      

      
    open_list = []
    closed_set = set()
    candidate_list = []
    cur_pos = from_pos
    
    done = False
    safety = 0 #used to make sure we don't grow infinitely due to bug
    while not done:
      safety += 1
      closed_set.add((cur_pos['x'],cur_pos['y']))
      open_list[:] = [i for i in open_list if not (i['x'] == cur_pos['x'] and i['y'] == cur_pos['y'])] #remove current position from list               
      candidate_tuples = [(cur_pos['x'] + 1, cur_pos['y']), (cur_pos['x'] - 1, cur_pos['y']), (cur_pos['x'], cur_pos['y'] + 1), (cur_pos['x'], cur_pos['y'] - 1)]
      #validate the candidates.
      for i in candidate_tuples:
        if not is_valid_move(i[0],i[1],cost_map):
          candidate_tuples.remove(i)
        else:
          if i not in closed_set:
            cand_pos = {}
            cand_pos['x'] = i[0]
            cand_pos['y'] = i[1]
            cand_pos['tilecost'] = cost_map[cand_pos['x']][cand_pos['y']]
            cand_pos['parent'] = cur_pos
            cand_pos['f'] = _f((cur_pos['x'], cur_pos['y']))
            cand_pos['g'] = _g((cur_pos['x'], cur_pos['y']))
            cand_pos['h'] = _h((cur_pos['x'], cur_pos['y']),cost_map)
            open_list.append(cand_pos)
      
      if not open_list: #if we ever find that the open list is empty, that means there is no path from here to there, so we're just going to abort early
        print("Could not find a valid path from ("+str(from_x)+","+str(from_y)+") to ("+str(to_x)+","+str(to_y)+").")
        return return_dictionary
        
      
      #now that we have open_list with all of the candidates, sort by f, then evaluate the top candidate on the list.
      open_list = sorted(open_list, key=lambda k: k['f'])
      cur_pos = open_list[0]
      
      if(cur_pos['x'] ==  to_pos['x'] and cur_pos['y'] == to_pos['y']):
        done = True
      if(safety > (number_of_tiles_on_rectangular_map(cost_map))): #If we've gone more iterations than there are squares on the map, we must be lost
        done = True
        print("Hit the safety")
        print("from: ("+str(from_x)+","+str(from_y)+")")
        print("  to: ("+str(to_x)+","+str(to_y)+")")
        print(cur_pos)
        print("closed:")
        print(closed_set)
        print("open:")
        print(open_list)
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
      open_list_tuples = []
      for pos in open_list:
        open_list_tuples.append((pos['x'],pos['y']))
      closed_list_tuples = []
      for pos in closed_set:
        closed_list_tuples.append(pos)
      return_dictionary['open'] = open_list_tuples
      return_dictionary['closed'] = closed_list_tuples
    return(return_dictionary)
