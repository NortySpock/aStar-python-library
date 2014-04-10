import path_util as path
import test_util as test

my_cost_map = test.make_grid(100,100,1) #default cost of 1
#test.u_shaped_wall(my_cost_map)
start_pos = [0,0]
end_pos = [99,99]

# my_cost_map[2][2] = 2
#quick_list = [(3,3,3),(2,2,2),(1,1,1),(0,0,0),(-1,-1,9)]
#path.apply_list_of_tuples_to_cost_map(quick_list,my_cost_map)
#test.u_shaped_wall(my_cost_map)

my_text_map = test.create_text_map_from_cost_map(my_cost_map)
my_text_map[start_pos[0]][start_pos[1]] = 'A'
my_text_map[end_pos[0]][end_pos[1]] = 'B'
test.pretty_print_map(my_text_map) #show board before we tamper with it
path_dict = path.a_star_manhattan_path(start_pos[0],start_pos[1],end_pos[0],end_pos[1], my_cost_map)
test.print_list_of_tuples_on_map(path_dict['open'], '~',my_text_map)
test.print_list_of_tuples_on_map(path_dict['closed'], '.',my_text_map)
test.print_path_on_map(my_text_map,path_dict['path'])
test.pretty_print_map(my_text_map)
test.check_path_for_validity(start_pos[0],start_pos[1],end_pos[0],end_pos[1],path_dict['path'], my_cost_map)

