from random import randrange
from copy import deepcopy
from itertools import product

def pretty_print_map(double_list):
  numcols = len(double_list)    
  colposes = len(double_list[0])
  my_row = ''
  
  header = "+"
  for i in xrange(numcols):
    header = header + "-"
  header = header + "+"
  
  print(header)
  for i in xrange(colposes):
    my_row = "|"
    for j in xrange(numcols):
      my_row = my_row + str(double_list[j][i])[0] #just one character, please!
    my_row = my_row + "|"
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
  return [[init]*y]*x

def create_text_map_from_cost_map(cost_map):
  max_x = len(cost_map)
  max_y = len(cost_map[0])
  text_map = make_grid(max_x,max_y,' ')
  for i in xrange(max_y):
    for j in xrange(max_x):
      if cost_map[j][i] == -1: #impassable
        text_map[j][i] = 'X'
      elif cost_map[j][i] == 1: #normal cost
        text_map[j][i] = ' '
      else:
        text_map[j][i] = cost_map[j][i] #just store the number

def generate_random_cost_map(cost_map,min_cost, max_cost):
  print ("in generate_random_cost_map")
  max_x = len(cost_map)
  max_y = len(cost_map[0])
  thing = 0
  xthing = range(max_x)
  print (xthing)
  ything = range(max_y)
  print (ything)
  coord_list = [range(max_x),range(max_y)]
  print (coord_list)
  my_iterator = product(*coord_list)
  print(my_iterator)

  for coord in product(*coord_list):
    thing += 1
    print("thing =",thing)
    print cost_map
    cost_map[coord[0]][coord[1]] = thing
    print cost_map
  


