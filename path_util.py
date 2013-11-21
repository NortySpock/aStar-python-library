from math import fabs as abs

def manhattan_distance(x1, y1, x2, y2):
    return (abs(x1-x2) + abs(y1-y2))

# returns a list of xy tuples that are a path from here to there  
#this does not take into account obstacles
def my_dumb_path(self, from_x,from_y,to_x,to_y):
    if self.debug:
        print("inside my_dumb_path")
        
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
        if self.debug:
          print("rising delta = %s"% rise_delta)
        if (curr_pos[1] < to_pos[1]): #above target, move down
          curr_pos[1] = curr_pos[1] + 1
        else: #below target, move up
          curr_pos[1] = curr_pos[1] - 1
      else: #move horizontally
        if self.debug:
          print("running delta = %s"% run_delta)
        if(curr_pos[0] < to_pos[0]): # left of target, move right
          curr_pos[0]  = curr_pos[0] + 1
        else: # right of target, move left
          curr_pos[0] = curr_pos[0] - 1
      if self.debug:
        print("curr_pos = %s"% curr_pos)
      the_path.append((curr_pos[0], curr_pos[1]))
      
      if curr_pos == to_pos:
        done = True
      
    #finally append the to_pos, because that was not done
    return the_path

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
