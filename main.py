import path_util as path

my_cost_map = path.make_grid(40,20,1) #default cost of 1

start_pos = [10,19]
end_pos = [10,10]

# start_pos = [10,0]
# end_pos = [10,19]

# my_cost_map[2][2] = -1
quick_list = [(11,10,-1),(9,10,-1),(10,11,-1),(10,9,-1)]
path.apply_list_of_tuples_to_cost_map(quick_list,my_cost_map)
# path.u_shaped_wall(my_cost_map)

my_text_map = path.create_text_map_from_cost_map(my_cost_map)
my_text_map[start_pos[0]][start_pos[1]] = 'A'
my_text_map[end_pos[0]][end_pos[1]] = 'B'
path.pretty_print_map(my_text_map) #show board before we tamper with it
path_dict = path.a_star_manhattan_path(start_pos[0],start_pos[1],end_pos[0],end_pos[1], my_cost_map)
path.print_list_of_tuples_on_map(path_dict['open'], '~',my_text_map)
path.print_list_of_tuples_on_map(path_dict['closed'], '.',my_text_map)
path.print_path_on_map(my_text_map,path_dict['path'])
path.pretty_print_map(my_text_map)
path.check_path_for_validity(start_pos[0],start_pos[1],end_pos[0],end_pos[1],path_dict['path'], my_cost_map)

