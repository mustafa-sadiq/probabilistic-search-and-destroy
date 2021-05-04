## CS440 Spring 2021
## Project 3 - Search and Destroy
## Mustafa Sadiq (ms3035)

##########################################################################################
import numpy as np
import random as rand
import matplotlib.pyplot as plt
import time
import math

##########################################################################################
cell_types = [1, 2, 3, 4]
type_of_cell = {1 : 'flat', 2 : 'hilly', 3 : 'forested', 4 : 'caves'}
false_negative_rates = {1 : 0.1, 2 : 0.3, 3 : 0.7, 4 : 0.9}

def generate_environement_map():
    dim = 50
    map = np.empty([dim, dim], dtype=int)
    for x in range(dim):
        for y in range(dim):
            map[x][y] = rand.choice(cell_types)
    target = (rand.randrange(0, dim), rand.randrange(0, dim))

    return map, target

def query_environment_map(map, target, query):
    if query == target:
        random_probability = rand.random()
        if map[query[0]][query[1]] == 1:
            if random_probability <= false_negative_rates[1]:
                return False
            else:
                return True

        if map[query[0]][query[1]] == 2:
            if random_probability <= false_negative_rates[2]:
                return False
            else:
                return True

        if map[query[0]][query[1]] == 3:
            if random_probability <= false_negative_rates[3]:
                return False
            else:
                return True

        if map[query[0]][query[1]] == 4:
            if random_probability <= false_negative_rates[4]:
                return False
            else:
                return True
    else:
        return False

def get_neighbours(current):
    x = current[0]
    y = current[1]
    dim = 50
    neighbours = []
    
    if x+1 < dim:
        neighbours.append((x+1, y))
    if x-1 > 0:
        neighbours.append((x-1, y))
    if y+1 < dim:
        neighbours.append((x, y+1))
    if y-1 > 0:
        neighbours.append((x, y-1))
    
    return neighbours

def manhattan_distance(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def print_map(map, file_name):
    dim = len(map)
    file = open(file_name, 'a')
    file.write('\n' + '----'*50 + '\n')
    for x in range(dim):
        for y in range(dim):
            file.write('| ' + str(map[x][y]) + ' ')        
        file.write('|\n' + '----'*50 + '\n')
    file.write('\n')
    file.close()

def update_belief(map, belief, current):
    dim = 50
    belief[current[0]][current[1]] = belief[current[0]][current[1]] * false_negative_rates[map[current[0]][current[1]]]
    total_belief = np.sum(belief)

    for x in range(dim):
        for y in range(dim):
            belief[x][y] = belief[x][y]/total_belief


# def update_belief(map, belief, current):
#     dim = 50
#     failure = (false_negative_rates[map[current[0]][current[1]]] * belief[current[0]][current[1]]) + (1 - belief[current[0]][current[1]])
#     for x in range(dim):
#         for y in range(dim):
#             if (x, y) == current:
#                 belief[x][y] = (belief[x][y] * false_negative_rates[map[current[0]][current[1]]])/failure
#             else:
#                 belief[x][y] = belief[x][y]/failure

def get_belief_finding_map(map, belief):
    dim = 50
    belief_finding = np.copy(belief)
    for x in range(dim):
        for y in range(dim):
            belief_finding[x][y] = belief_finding[x][y] * (1-false_negative_rates[map[x][y]])
    return belief_finding

def get_belief_finding_map_improved(map, belief, current):
    dim = 50
    belief_finding = np.copy(belief)
    for x in range(dim):
        for y in range(dim):
            belief_finding[x][y] = (belief_finding[x][y] * (1-false_negative_rates[map[x][y]])) / (1 + manhattan_distance(current, (x,y)))
    return belief_finding

def update_belief_within_five(map, belief, current):
    dim = 50
    for x in range(dim):
        for y in range(dim):
            if manhattan_distance(current, (x,y)) > 5:
                belief[x][y] = 0.0000000000000000001
    total_belief = np.sum(belief)

    for x in range(dim):
        for y in range(dim):
            belief[x][y] = belief[x][y]/total_belief

def update_belief_not_within_five(map, belief, current):
    dim = 50
    for x in range(dim):
        for y in range(dim):
            if manhattan_distance(current, (x,y)) <= 5:
                belief[x][y] = 0.0000000000000000001
    total_belief = np.sum(belief)

    for x in range(dim):
        for y in range(dim):
            belief[x][y] = belief[x][y]/total_belief

def within_five(target, current):
    if manhattan_distance(target, current) <= 5:
        return True
    else:
        return False

def next_cell(belief_map, current):
    highest_probability_cells = np.where(belief_map == np.amax(belief_map))
    highest_probability_cells = list(zip(highest_probability_cells[0], highest_probability_cells[1]))
    minimum_distance = 100000000
    minimum_distance_cells = []
    for highest_probability_cell in highest_probability_cells:
        distance = manhattan_distance(current, highest_probability_cell)
        if distance < minimum_distance:
            minimum_distance = distance
            minimum_distance_cells = [highest_probability_cell]
        if distance == minimum_distance:
            minimum_distance_cells.append(highest_probability_cell)            
    # print(minimum_distance_cells)
    return rand.choice(minimum_distance_cells)


# ############################# Basic agent 1 ############################################
# dim = 50
# map, target = generate_environement_map()
# belief_map = np.full([dim,dim], 1/(dim*dim))
# current = (rand.randrange(0, dim), rand.randrange(0, dim))

# print("Target cell type:", type_of_cell[map[target[0]][target[1]]])

# total_searches = 0
# distance_travelled = 0

# while True:
#     query_cell = next_cell(belief_map, current)
#     total_searches += 1
#     distance_travelled += manhattan_distance(query_cell, current)
#     query_result = query_environment_map(map, target, query_cell)
#     if query_result == True:
#         current = query_cell
#         break
#     else:
#         current = query_cell
#         update_belief(map, belief_map, current)

# print(total_searches+distance_travelled)


############################# Basic agent 1 terrain data ############################################
# maps_for_each_type = 10

# cell_type_data_count = {'flat':0, 'hilly':0, 'forested':0, 'caves':0}
# cell_type_data = {'flat':0, 'hilly':0, 'forested':0, 'caves':0}


# while cell_type_data_count['flat'] < maps_for_each_type or cell_type_data_count['hilly'] < maps_for_each_type or cell_type_data_count['forested'] < maps_for_each_type or cell_type_data_count['caves'] < maps_for_each_type:
#     dim = 50
#     map, target = generate_environement_map()    
#     target_type = type_of_cell[map[target[0]][target[1]]]

#     if target_type == 'flat' and cell_type_data_count['flat'] == maps_for_each_type:
#         continue
#     if target_type == 'hilly' and cell_type_data_count['hilly'] == maps_for_each_type:
#         continue
#     if target_type == 'forested' and cell_type_data_count['forested'] == maps_for_each_type:
#         continue
#     if target_type == 'caves' and cell_type_data_count['caves'] == maps_for_each_type:
#         continue
    
#     cell_type_data_count[target_type] += 1    
#     print("Target cell type:", target_type)

#     belief_map = np.full([dim,dim], 1/(dim*dim))
#     current = (rand.randrange(0, dim), rand.randrange(0, dim))



#     total_searches = 0
#     distance_travelled = 0

#     while True:
#         query_cell = next_cell(belief_map, current)
#         total_searches += 1
#         distance_travelled += manhattan_distance(query_cell, current)
#         query_result = query_environment_map(map, target, query_cell)
#         if query_result == True:
#             current = query_cell
#             break
#         else:
#             current = query_cell
#             update_belief(map, belief_map, current)

#     if cell_type_data[target_type] == 0:
#         cell_type_data[target_type] = (total_searches+distance_travelled)
#     else:
#         cell_type_data[target_type] = (cell_type_data[target_type] + (total_searches+distance_travelled))/2

# print(cell_type_data)


############################# Basic agent 2 ############################################
# dim = 50
# map, target = generate_environement_map()
# belief_map = np.full([dim,dim], 1/(dim*dim))
# belief_finding_map = get_belief_finding_map(map, belief_map) 
# current = (rand.randrange(0, dim), rand.randrange(0, dim))

# print("Target cell type:", type_of_cell[map[target[0]][target[1]]])

# total_searches = 0
# distance_travelled = 0

# while True:
#     query_cell = next_cell(belief_finding_map, current)
#     total_searches += 1
#     distance_travelled += manhattan_distance(query_cell, current)
#     query_result = query_environment_map(map, target, query_cell)
#     if query_result == True:
#         current = query_cell
#         break
#     else:
#         current = query_cell
#         update_belief(map, belief_map, current)
#         belief_finding_map = get_belief_finding_map(map, belief_map)

# print(total_searches+distance_travelled)

############################# Basic agent 2 terrain data ############################################
# maps_for_each_type = 10

# cell_type_data_count = {'flat':0, 'hilly':0, 'forested':0, 'caves':0}
# cell_type_data = {'flat':0, 'hilly':0, 'forested':0, 'caves':0}


# while cell_type_data_count['flat'] < maps_for_each_type or cell_type_data_count['hilly'] < maps_for_each_type or cell_type_data_count['forested'] < maps_for_each_type or cell_type_data_count['caves'] < maps_for_each_type:
#     dim = 50
#     map, target = generate_environement_map()    
#     target_type = type_of_cell[map[target[0]][target[1]]]

#     if target_type == 'flat' and cell_type_data_count['flat'] == maps_for_each_type:
#         continue
#     if target_type == 'hilly' and cell_type_data_count['hilly'] == maps_for_each_type:
#         continue
#     if target_type == 'forested' and cell_type_data_count['forested'] == maps_for_each_type:
#         continue
#     if target_type == 'caves' and cell_type_data_count['caves'] == maps_for_each_type:
#         continue
    
#     cell_type_data_count[target_type] += 1    
#     print("Target cell type:", target_type)

#     belief_map = np.full([dim,dim], 1/(dim*dim))
#     belief_finding_map = get_belief_finding_map(map, belief_map)
#     current = (rand.randrange(0, dim), rand.randrange(0, dim))



#     total_searches = 0
#     distance_travelled = 0

#     while True:
#         query_cell = next_cell(belief_finding_map, current)
#         total_searches += 1
#         distance_travelled += manhattan_distance(query_cell, current)
#         query_result = query_environment_map(map, target, query_cell)
#         if query_result == True:
#             current = query_cell
#             break
#         else:
#             current = query_cell
#             update_belief(map, belief_map, current)
#             belief_finding_map = get_belief_finding_map(map, belief_map)

#     if cell_type_data[target_type] == 0:
#         cell_type_data[target_type] = (total_searches+distance_travelled)
#     else:
#         cell_type_data[target_type] = (cell_type_data[target_type] + (total_searches+distance_travelled))/2

# print(cell_type_data)


############################# Improved agent terrain data ############################################
# maps_for_each_type = 10

# cell_type_data_count = {'flat':0, 'hilly':0, 'forested':0, 'caves':0}
# cell_type_data = {'flat':0, 'hilly':0, 'forested':0, 'caves':0}


# while cell_type_data_count['flat'] < maps_for_each_type or cell_type_data_count['hilly'] < maps_for_each_type or cell_type_data_count['forested'] < maps_for_each_type or cell_type_data_count['caves'] < maps_for_each_type:
#     dim = 50
#     map, target = generate_environement_map()    
#     target_type = type_of_cell[map[target[0]][target[1]]]

#     if target_type == 'flat' and cell_type_data_count['flat'] == maps_for_each_type:
#         continue
#     if target_type == 'hilly' and cell_type_data_count['hilly'] == maps_for_each_type:
#         continue
#     if target_type == 'forested' and cell_type_data_count['forested'] == maps_for_each_type:
#         continue
#     if target_type == 'caves' and cell_type_data_count['caves'] == maps_for_each_type:
#         continue
    
#     cell_type_data_count[target_type] += 1    
#     print("Target cell type:", target_type)

#     belief_map = np.full([dim,dim], 1/(dim*dim))    
#     current = (rand.randrange(0, dim), rand.randrange(0, dim))
#     belief_finding_map = get_belief_finding_map_improved(map, belief_map, current)



#     total_searches = 0
#     distance_travelled = 0

#     while True:
#         query_cell = next_cell(belief_finding_map, current)
#         total_searches += 1
#         distance_travelled += manhattan_distance(query_cell, current)
#         query_result = query_environment_map(map, target, query_cell)
#         if query_result == True:
#             current = query_cell
#             break
#         else:
#             current = query_cell
#             update_belief(map, belief_map, current)
#             belief_finding_map = get_belief_finding_map_improved(map, belief_map, current)

#     if cell_type_data[target_type] == 0:
#         cell_type_data[target_type] = (total_searches+distance_travelled)
#     else:
#         cell_type_data[target_type] = (cell_type_data[target_type] + (total_searches+distance_travelled))/2

# print(cell_type_data)

############################# Basic agent 1 data ############################################
# maps = 10
# runs = 10
# dim = 50

# total_score = 0

# for x in range(maps):
#     map, target = generate_environement_map()  
#     total_searches = 0
#     distance_travelled = 0  
#     for y in range(runs):
#         print("map#", x, "run#", y)
#         current = (rand.randrange(0, dim), rand.randrange(0, dim))
#         target = (rand.randrange(0, dim), rand.randrange(0, dim))
#         belief_map = np.full([dim,dim], 1/(dim*dim))
#         while True:
#             query_cell = next_cell(belief_map, current)
#             total_searches += 1
#             distance_travelled += manhattan_distance(query_cell, current)
#             query_result = query_environment_map(map, target, query_cell)
#             if query_result == True:
#                 current = query_cell
#                 break
#             else:
#                 current = query_cell
#                 update_belief(map, belief_map, current)
#     total_score += (total_searches+distance_travelled)/(runs)
#     print("map#", x, "average score:", (total_searches+distance_travelled)/(runs))

# print("Total average score:", total_score/maps)

############################# Basic agent 2 data ############################################
# maps = 10
# runs = 10
# dim = 50

# total_score = 0

# for x in range(maps):
#     map, target = generate_environement_map()  
#     total_searches = 0
#     distance_travelled = 0  
#     for y in range(runs):
#         print("map#", x, "run#", y)
#         current = (rand.randrange(0, dim), rand.randrange(0, dim))
#         target = (rand.randrange(0, dim), rand.randrange(0, dim))
#         belief_map = np.full([dim,dim], 1/(dim*dim))
#         belief_finding_map = get_belief_finding_map(map, belief_map) 
#         while True:
#             query_cell = next_cell(belief_finding_map, current)
#             total_searches += 1
#             distance_travelled += manhattan_distance(query_cell, current)
#             query_result = query_environment_map(map, target, query_cell)
#             if query_result == True:
#                 current = query_cell
#                 break
#             else:
#                 current = query_cell
#                 update_belief(map, belief_map, current)
#                 belief_finding_map = get_belief_finding_map(map, belief_map)

#     total_score += (total_searches+distance_travelled)/(runs)
#     print("map#", x, "average score:", (total_searches+distance_travelled)/(runs))

# print("Total average score:", total_score/maps)

############################# Improved agent data ############################################
# maps = 10
# runs = 10
# dim = 50

# total_score = 0

# for x in range(maps):
#     map, target = generate_environement_map()  
#     total_searches = 0
#     distance_travelled = 0  
#     for y in range(runs):
#         print("map#", x, "run#", y)
#         current = (rand.randrange(0, dim), rand.randrange(0, dim))
#         target = (rand.randrange(0, dim), rand.randrange(0, dim))
#         belief_map = np.full([dim,dim], 1/(dim*dim))
#         belief_finding_map = get_belief_finding_map_improved(map, belief_map, current) 
#         while True:
#             query_cell = next_cell(belief_finding_map, current)
#             total_searches += 1
#             distance_travelled += manhattan_distance(query_cell, current)
#             query_result = query_environment_map(map, target, query_cell)
#             if query_result == True:
#                 current = query_cell
#                 break
#             else:
#                 current = query_cell
#                 update_belief(map, belief_map, current)
#                 belief_finding_map = get_belief_finding_map_improved(map, belief_map, current)

#     total_score += (total_searches+distance_travelled)/(runs)
#     print("map#", x, "average score:", (total_searches+distance_travelled)/(runs))

# print("Total average score:", total_score/maps)

############################## Moving Bonus basic agent 1 #############################
# dim = 50
# map, target = generate_environement_map()
# belief_map = np.full([dim,dim], 1/(dim*dim))
# current = (rand.randrange(0, dim), rand.randrange(0, dim))

# print("Target cell type:", type_of_cell[map[target[0]][target[1]]])

# total_searches = 0
# distance_travelled = 0

# while True:
#     print_map(belief_map, "./TESTS/1.txt")
#     query_cell = next_cell(belief_map, current)
#     total_searches += 1
#     distance_travelled += manhattan_distance(query_cell, current)
#     query_result = query_environment_map(map, target, query_cell)
#     if query_result == True:
#         current = query_cell
#         break
#     else:
#         current = query_cell
#         update_belief(map, belief_map, current)
#         target = rand.choice(get_neighbours(target))
#         if within_five(target, current):
#             update_belief_within_five(map, belief_map, current)
#         else:
#             update_belief_not_within_five(map, belief_map, current)
        

# print(total_searches+distance_travelled)

############################# Moving Basic agent 1 data ############################################
# maps = 10
# runs = 10
# dim = 50

# total_score = 0

# for x in range(maps):
#     map, target = generate_environement_map()  
#     total_searches = 0
#     distance_travelled = 0  
#     for y in range(runs):
#         print("map#", x, "run#", y)
#         current = (rand.randrange(0, dim), rand.randrange(0, dim))
#         target = (rand.randrange(0, dim), rand.randrange(0, dim))
#         belief_map = np.full([dim,dim], 1/(dim*dim))
#         while True:
#             query_cell = next_cell(belief_map, current)
#             total_searches += 1
#             distance_travelled += manhattan_distance(query_cell, current)
#             query_result = query_environment_map(map, target, query_cell)
#             if query_result == True:
#                 current = query_cell
#                 break
#             else:
#                 current = query_cell
#                 update_belief(map, belief_map, current)
#                 target = rand.choice(get_neighbours(target))
#                 if within_five(target, current):
#                     update_belief_within_five(map, belief_map, current)
#                 else:
#                     update_belief_not_within_five(map, belief_map, current)

#     total_score += (total_searches+distance_travelled)/(runs)
#     print("map#", x, "average score:", (total_searches+distance_travelled)/(runs))

# print("Total average score:", total_score/maps)

# ############################ Moving Basic agent 2 data ############################################
# maps = 10
# runs = 10
# dim = 50

# total_score = 0

# for x in range(maps):
#     map, target = generate_environement_map()  
#     total_searches = 0
#     distance_travelled = 0  
#     for y in range(runs):
#         print("map#", x, "run#", y)
#         current = (rand.randrange(0, dim), rand.randrange(0, dim))
#         target = (rand.randrange(0, dim), rand.randrange(0, dim))
#         belief_map = np.full([dim,dim], 1/(dim*dim))
#         belief_finding_map = get_belief_finding_map(map, belief_map) 
#         while True:
#             query_cell = next_cell(belief_finding_map, current)
#             total_searches += 1
#             distance_travelled += manhattan_distance(query_cell, current)
#             query_result = query_environment_map(map, target, query_cell)
#             if query_result == True:
#                 current = query_cell
#                 break
#             else:
#                 current = query_cell
#                 update_belief(map, belief_map, current)
#                 target = rand.choice(get_neighbours(target))
#                 if within_five(target, current):
#                     update_belief_within_five(map, belief_map, current)
#                 else:
#                     update_belief_not_within_five(map, belief_map, current)
#                 belief_finding_map = get_belief_finding_map(map, belief_map)
                

#     total_score += (total_searches+distance_travelled)/(runs)
#     print("map#", x, "average score:", (total_searches+distance_travelled)/(runs))

# print("Total average score:", total_score/maps)

# ############################ Moving Improved agent data ############################################
# maps = 10
# runs = 10
# dim = 50

# total_score = 0

# for x in range(maps):
#     map, target = generate_environement_map()  
#     total_searches = 0
#     distance_travelled = 0  
#     for y in range(runs):
#         print("map#", x, "run#", y)
#         current = (rand.randrange(0, dim), rand.randrange(0, dim))
#         target = (rand.randrange(0, dim), rand.randrange(0, dim))
#         belief_map = np.full([dim,dim], 1/(dim*dim))
#         belief_finding_map = get_belief_finding_map_improved(map, belief_map, current) 
#         while True:
#             query_cell = next_cell(belief_finding_map, current)
#             total_searches += 1
#             distance_travelled += manhattan_distance(query_cell, current)
#             query_result = query_environment_map(map, target, query_cell)
#             if query_result == True:
#                 current = query_cell
#                 break
#             else:
#                 current = query_cell
#                 update_belief(map, belief_map, current)
#                 target = rand.choice(get_neighbours(target))
#                 if within_five(target, current):
#                     update_belief_within_five(map, belief_map, current)
#                 else:
#                     update_belief_not_within_five(map, belief_map, current)
#                 belief_finding_map = get_belief_finding_map_improved(map, belief_map, current)

#     total_score += (total_searches+distance_travelled)/(runs)
#     print("map#", x, "average score:", (total_searches+distance_travelled)/(runs))

# print("Total average score:", total_score/maps)