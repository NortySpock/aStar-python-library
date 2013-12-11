from random import randrange
from copy import deepcopy


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

def replace_in_map(map_in, from_var,to_var):
  max_x = len(map_in)
  max_y = len(map_in[0])
  for i in xrange(max_y):
    for j in xrange(max_x):
      if map_in[j][i] == from_var:
	map_in[j][i] = to_var

def generate_random_cost_map(cost_map,min_cost, max_cost):
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

def check_path_for_validity(from_x,from_y,to_x,to_y, path, cost_map):
  prev = [from_x,from_y]
  
  for point in path:
    if not is_valid_move(point[0],point[1],cost_map):
      print "Move to ("+str(point[0])+","+str(point[1])+") is not valid!"
    if not is_manhattan_adjacent(prev[0],prev[1],point[0],point[1]):
      print "Prev pos ("+str(prev[0])+","+str(prev[1])+")"+" and curr pos ("+str(point[0])+","+str(point[1])+") are not adjacent!"
    prev = point
  last = path[-1]
  if last != (to_x,to_y):
    print "Final pos ("+str(last[0])+","+str(last[1])+")"+" is not the target at("+str(to_x)+","+str(to_y)+")!"

def is_valid_move(x,y,cost_map):
  max_x = len(cost_map)
  max_y = len(cost_map[0])
  if(0 <= x < max_x and 0 <= y < max_y and cost_map[x][y] != -1):
    return True
  else:
    return False

