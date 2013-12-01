from path_util import *
from test_util import *

my_cost_map = make_grid(40,20,1) #default cost of 1
generate_random_cost_map(my_cost_map, -1,4)
replace_in_map(my_cost_map, 0, 1)
my_text_map = create_text_map_from_cost_map(my_cost_map)
pretty_print_map(my_text_map)

