# Team ID: G5T01

def schedule2(locations, start_location, capacities, orders):     
    # prepare for retrieval of information: orders, location loads
    order_locations = [start_location]
    location_load_dict = {}
    for i in range(len(orders)):
        order_locations.append(orders[i][2])
        location_load_dict[orders[i][2]] = orders[i][1]

    # locations dictionary to store distances between different locations
    locations_dict = {}
    for i in range(len(locations)):
        l = locations[i].split(',')
        l_from = l[0]
        l_to = l[1]
        l_dist = int(l[2])

        if l_from in order_locations and l_to in order_locations:
            if l_from not in locations_dict:
                locations_dict[l_from] = {l_to: l_dist}
            else:
                locations_dict[l_from].update({l_to: l_dist})   

    # lists to keep track of visited locations and unvisited locations
    route_list = []
    number_of_trucks = len(capacities)
    visited_destinations = [start_location]
    unvisited_dict = location_load_dict
    
    # sorting backwards (largest capacities first for better optimisation [we use the better trucks])
    ordered_capacities = sorted(capacities, reverse=True)
    
    for i in range(number_of_trucks):
        next_best_l = next_best_location(locations_dict, start_location, visited_destinations, location_load_dict, capacities[i])
        if next_best_l != ():
            # next best location
            l_location = next_best_l[0]
            # next best location's load
            l_load = next_best_l[1]
            # we remove the location as we have now visited it
            unvisited_dict.pop(l_location)
            # we add it to our visited destinations
            visited_destinations.append(l_location)
            
            next_min_load_destination = min(unvisited_dict, key=unvisited_dict.get)
            next_min_destination_load = unvisited_dict[next_min_load_destination]

            remaining_capacity = ordered_capacities[i] - l_load
            # we keep track of the truck current location, with its remaining capacity
            truck = [remaining_capacity, l_location]
            
            while remaining_capacity > next_min_destination_load and len(visited_destinations) < len(order_locations):              
                from_loc = truck[-1]
                next_best_l = next_best_location(locations_dict, from_loc, visited_destinations, location_load_dict, remaining_capacity)
                # possibility that there is none, if there is none, we get out of the while loop
                if next_best_l != ():
                    l_location = next_best_l[0]
                    l_load = next_best_l[1]
                    visited_destinations.append(l_location)
                    unvisited_dict.pop(l_location)
                    # update truck's capacity
                    truck[0] -= l_load
                    remaining_capacity = truck[0]
                    # add on the individual truck's schedule
                    truck.append(l_location)
                    
                    if len(visited_destinations) < len(order_locations):
                        next_min_load_destination = min(unvisited_dict, key=unvisited_dict.get)
                        next_min_destination_load = unvisited_dict[next_min_load_destination]
                else:
                    break
                     
            route_list.append(truck)

    # reordering list of trucks with sorted truck capacities for final schedule - as we first filled the highest capacity trucks first
    reordered_list_of_trucks = []
    for i in range(len(capacities)):
        reordered_list_of_trucks.append([])

    # to find the capacity from ordered capacity, to match with the index of the truck no. with the same capacity
    used_trucks_index = []
    for i in range(len(route_list)):
        route = route_list[i]
        truck_capacity = ordered_capacities[i]
        max_capacity_index = capacities.index(truck_capacity)
        
        # to handle multiple trucks with the same capacity
        while max_capacity_index in used_trucks_index:
            # to assign the route to the next truck with the same capacity
            max_capacity_index = capacities.index(truck_capacity, max_capacity_index + 1)
        
        used_trucks_index.append(max_capacity_index)
        reordered_list_of_trucks[max_capacity_index] = route

    # append the schedule based on requirements of answer
    final_schedule = []
    for truck in reordered_list_of_trucks:
        truck_order = []
        truck_location = truck[1:]
        for location in truck_location:
            for order in orders:
                if location == order[2]:
                    truck_order.append(order)
        final_schedule.append(truck_order)
    
    return final_schedule

    
# to iterate through locations to obtain the next best location and load required based off capacity of truck
def next_best_location(locations_dict, from_loc, visited, location_load_dict, capacity):
    # min helps us keep track of the next best minimum distance
    min = 100000000000000000
    # to initialise an output in the case where there is no next best location
    next_best_location = ()
    for location, dist in locations_dict[from_loc].items():
        if location not in visited and location_load_dict[location] <= capacity and dist <= min:
            min = dist
            load = location_load_dict[location]
            next_best_location = (location, load)
    return next_best_location