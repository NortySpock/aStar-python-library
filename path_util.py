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


def norty_a_star_manhattan_path(from_x,from_y,to_x,to_y,cost_map):
  #idiot check
  if from_x == to_x and from_y == to_y:
    return [] 
  
  done = False
  
  #cost of distance from source to proposed position
  def _g(pos_x, pos_y):
    return manhattan_distance(pos_x, pos_y, from_x, from_y)
  
  #estimate of cost of distance from here to target + difficulty of proposed position
  def _h(pos_x, pos_y,cost_map): #distance + cost of current space
    return manhattan_distance(pos_x, pos_y, to_x, to_y) + cost_map[pos_x][pos_y]
  
  def _f(pos_x,pos_y,cost_map)
    return _g(pos_x,pos_y) + _h(pos_x,pos_y,cost_map)
  
  #set up inital A*
  open_set = set()
  closed_set = set()
  #add the starting position
  open_set.add([from_x,from_y])
  
  while not done:
    pos_x,pos_y = open_set.pop() #take one off the open list
    closed_set.add([pos_x,pos_y]) #add it to the closed list
    adj_list = create_manhattan_adjacent_positions(pos_x,pos_y)
    
    for adj in adj_list:
      if is_valid_move(adj[0],adj[1],cost_map): 
        if adj not in closed_set:
          open_set.add(adj)
        else:
          closed_set.add(adj):
    
    
    

def a_star_path(self, from_x,from_y,to_x,to_y, unit_number):
    if self.a_star_debug:
      print ("STARTING ASTAR")
    
    if from_x == to_x and from_y == to_y:
      return []
    #make unit list into tuples
    unit_tups = zip([i.x for i in self.units[0:]], [i.y for i in self.units[0:]])
    
    def _g(self, i):
      return self.manhattan_distance(i[0], i[1], from_x, from_y)
    
    def _h(self, i, unit_tups):
      difficulty = 1
      for unit in unit_tups:
        if unit[0] == i[0] and unit[1] == i[1]:
          difficulty = 6
          break
      if self.tiles[self.getTileIndex(i)].depth < 0 and self.tiles[self.getTileIndex(i)].waterAmount > 0:
        difficulty = 6
      return self.manhattan_distance(i[0], i[1], to_x, to_y) * difficulty
      
    def _makePath(self, childTup, endTup, failsafe):
      failsafe += 1
      if childTup != endTup and failsafe != 100:
        path.insert(0, childTup)
        failsafe = _makePath(self, parents[childTup], endTup, failsafe)
      return failsafe
      
    open_set = set()
    closed_set = set()
    candidate_list = []
    parents = {} #{child: parent}
    cur_x = from_x
    cur_y = from_y
    
    on_target = False
    safety = 0
    while not on_target:
      safety += 1
      closed_set.add((cur_x, cur_y))
      if (cur_x, cur_y) in open_set:
        open_set.remove((cur_x, cur_y))
      candidate_list = [(cur_x + 1, cur_y), (cur_x - 1, cur_y), (cur_x, cur_y + 1), (cur_x, cur_y - 1)]
      #validate the candidates.  At the minimum they should have birth certificates from USA.
      for cand in candidate_list[::-1]:
        # if cand[0] >= self.mapWidth or cand[0] < 0:
          # if self.path_debug:
            # print("Trying to remove ", cand)
          # candidate_list.remove(cand)
        # if cand[1] >= self.mapHeight or cand[1] < 0:
          # if self.path_debug:
            # print("Trying to remove ", cand)
          # candidate_list.remove(cand)
        if not self.isValidMoveSquare(cand):
          #print("Trying to remove ", cand)
          candidate_list.remove(cand)
        else:
          if self.tiles[self.getTileIndex(cand)].waterAmount > 0:
            if (cand in candidate_list):
              candidate_list.remove(cand)
            if (cand not in closed_set):
              closed_set.add(cand)
      if self.path_debug:
        print("candidate list: ", candidate_list)
      
      #generate candidate squares.  if they are traversable, add to open_set and remember parent
      for i in range(len(candidate_list)):
        if self.path_debug and candidate_list[i][0] * self.mapHeight + candidate_list[i][1] > 799:
          print ("This index is too big: ", candidate_list[i][0], " ",  self.mapHeight, " ",  candidate_list[i][1])
        if candidate_list[i] not in closed_set and \
        self.tiles[candidate_list[i][0] * self.mapHeight + candidate_list[i][1]].owner != self.playerID - 1:
          open_set.add(deepcopy(candidate_list[i]))
          parents[candidate_list[i]] = (cur_x, cur_y)
      #Calculate f(i) for every square in the open list
      best_f = 9999
      cur_square = (-1, -1)
      for square_tup in open_set:
        cur_f = _g(self, square_tup) + _h(self, square_tup, unit_tups)
        if cur_f < best_f:
          cur_square = square_tup
          best_f = cur_f
      if cur_square == (-1, -1):
        return []
        
      cur_x = cur_square[0]
      cur_y = cur_square[1]
      if cur_x == to_x and cur_y == to_y:
        on_target = True
      if safety == 1000:
        on_target = True
        print("Hit the safety")
        # print(cur_x, ' ', to_x, ' ', cur_y, ' ', to_y)
        # print("closed set")
        # print(closed_set)
        # print("open set")
        # print(open_set)
      if self.turnNumber < 10 and self.a_star_debug:
        print("at %s, %s :: going to %s, %s"%(cur_x, cur_y, to_x, to_y))
        print("candidate set")
        print(candidate_list)
        print("closed set")
        print(closed_set)
        print("open set")
        print(open_set)
      candidate_list = []
    
    #Now we need to trace backward through the parents to get the path
    path = []
    failstat = _makePath(self, cur_square, (from_x, from_y), 0)
    if self.path_debug:
      print("Inside a_star_path")
      print("from %s to %s"%((from_x, from_y), (to_x, to_y)))
      print(path)
      print("closed_set: ", closed_set)
      print("open_set: ", open_set)
    if self.time_debug:
      print("unit %s: len(closed_set)= %s, len(open_set) = %s, failstat = %s"%(unit_number, len(closed_set), len(open_set), failstat))
    return path
