from path_util import *
from test_util import *

my_cost_map = make_grid(4,3,1) #default cost of 1
generate_random_cost_map(my_cost_map, -1,2)
my_text_map = create_text_map_from_cost_map(my_cost_map)
pretty_print_map(my_text_map)

