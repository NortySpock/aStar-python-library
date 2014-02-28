from path_util import *
from test_util import *

my_cost_map = make_grid(40,20,1) #default cost of 1
start_pos = [20,0]
end_pos = [20,19]

u_shaped_wall(my_cost_map)

my_text_map = create_text_map_from_cost_map(my_cost_map)
my_text_map[start_pos[0]][start_pos[1]] = 'A'
my_text_map[end_pos[0]][end_pos[1]] = 'B'
pretty_print_map(my_text_map) #show board before we tamper with it
the_path = a_star_manhattan_path(start_pos[0],start_pos[1],end_pos[0],end_pos[1],my_cost_map)
print_path_on_map(my_text_map,the_path)
pretty_print_map(my_text_map)
check_path_for_validity(start_pos[0],start_pos[1],end_pos[0],end_pos[1],the_path, my_cost_map)

