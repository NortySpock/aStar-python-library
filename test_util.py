def pretty_print_map(self, double_list):
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
        my_row = my_row + str(double_list[j][i])
      my_row = my_row + "|"
      print(my_row)
    print(header)

def populate_map(self, max_x,max_y,list_of_three_tuples):
    matrix = [[' ' for colnum in xrange(max_y)] for colpos in xrange(max_x)]
    if(list_of_three_tuples is not None and len(list_of_three_tuples) > 0):
      for point in list_of_three_tuples:
        if(point[0] >= 0 and point[0] < max_x) and (point[1] >= 0 and point[1] < max_y): #sanity
          matrix[point[0]][point[1]] = str(point[2])[0]
    return matrix

def make_me_a_world_list_of_threetuples(self):
    world_list = []
    for tile in self.tiles:
      if tile.isSpawning:
        world_list.append((tile.x,tile.y,"S"))
      if tile.pumpID != -1:
        world_list.append((tile.x,tile.y,"P"))
      if tile.waterAmount == 1:
        world_list.append((tile.x,tile.y,"w"))
      if tile.waterAmount > 1:
        world_list.append((tile.x,tile.y,"W"))
      if tile.waterAmount <= 0 and tile.depth > 0:
        world_list.append((tile.x,tile.y,"t"))
    for u in self.units:
      world_list.append((tile.x,tile.y,"U"))
      
    return world_list
    
def make_grid(x,y,init=None):
     return [[init]*x]*y

