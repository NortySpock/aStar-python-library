from random import randrange
from test_util import is_valid_move
from copy import deepcopy
import heapq

def manhattan_distance(x1, y1, x2, y2):
    return (abs(x1-x2) + abs(y1-y2))

# returns a list of xy tuples that are a path from here to there  
#this does not take into account obstacles
def my_dumb_path(from_x,from_y,to_x,to_y):
        
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
  
def detour_random_path(from_x,from_y,to_x,to_y, cost_map):
    the_path = []
    from_pos = [from_x, from_y]
    to_pos = [to_x,to_y]
    curr_pos = deepcopy(from_pos)
    move_pos = deepcopy(from_pos)
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

      curr_pos = deepcopy(move_pos) #update curr_pos
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
    from_pos = (from_x,from_y)
    to_pos = (to_x,to_y)
    
    if from_pos == to_pos:
      return []
      
    def _g(i):
      return manhattan_distance(i[0], i[1], from_pos[0], from_pos[1])
    
    def _h(i, cost_map):
      tile_cost = cost_map[i[0]][i[1]]
      return (manhattan_distance(i[0], i[1], to_pos[0], to_pos[1]) + tile_cost)
      
    def _makePath(childTup, endTup, failsafe):
      failsafe += 1
      if childTup != endTup and failsafe != 100:
        path.insert(0, childTup)
        failsafe = _makePath(parents[childTup], endTup, failsafe)
      return failsafe
      
    open_set = set()
    closed_set = set()
    candidate_list = []
    parents = {} #{child: parent}
    cur_x = from_pos[0]
    cur_y = from_pos[1]
    
    done = False
    safety = 0 #used to make sure we don't grow infinitely due to bug
    while not done:
      safety += 1
      closed_set.add((cur_x, cur_y))
      if (cur_x, cur_y) in open_set:
        open_set.remove((cur_x, cur_y))
      candidate_list = [(cur_x + 1, cur_y), (cur_x - 1, cur_y), (cur_x, cur_y + 1), (cur_x, cur_y - 1)]
      #validate the candidates.
      for cand in candidate_list:
        if not is_valid_move(cand):
          candidate_list.remove(cand)
            
      #generate candidate squares.  if they are traversable, add to open_set and remember parent
      for i in range(len(candidate_list)):
        if candidate_list[i] not in closed_set:
          open_set.add(deepcopy(candidate_list[i]))
          parents[candidate_list[i]] = (cur_x, cur_y)
      #Calculate f(i) for every square in the open list
      best_f = 9999
      cur_square = (-1, -1)
      for square_tup in open_set: #TODO: No wonder we had perf problems, we're re-calculating f!
        cur_f = _g(self, square_tup) + _h(self, square_tup, unit_tups)
        if cur_f < best_f:
          cur_square = square_tup
          best_f = cur_f
      if cur_square == (-1, -1):
        return []
        
      cur_x = cur_square[0]
      cur_y = cur_square[1]
      if cur_x == to_x and cur_y == to_y:
        done = True
      if safety == 1000:
        done = True
        print("Hit the safety")
        print(cur_x, ' ', to_x, ' ', cur_y, ' ', to_y)
        print("closed set")
        print(closed_set)
        print("open set")
        print(open_set)
      candidate_list = []
    
    #Now we need to trace backward through the parents to get the path
    path = []
    failstat = _makePath(self, cur_square, (from_x, from_y), 0)

    return path
