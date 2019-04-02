# Team ID: G5T01

def schedule1(locations, start_location, number_of_trucks, orders):
    """
    parameter format example:
    locations:["USA,CAN,731", "USA,BHM,1623", "USA,CUB,1813"...]
    start_location: "USA"
    number_of_trucks: 3
    orders : [(1, 100, 'RUS'), (2, 150, 'CAN'), (3, 250, 'SIN'), (4, 300, 'KOR'), (5, 200, 'CHN'), (6, 250, 'MEX'), (7, 350, 'AUS'), (8, 270, 'GMY'), (9, 180, 'FRN'), (10, 230, 'SPN')]
    """

    # Initialise the destination list
    destinations = [start_location]
    #format: destination : (order)
    orders_dict = {}

    for order in orders:
        destinations.append(order[2])
        orders_dict[order[2]] = order
        
    """
    expected outcome:
    destinations = ['USA', 'RUS', 'CAN', 'SIN', 'KOR', 'CHN', 'MEX', 'AUS', 'GMY', 'FRN', 'SPN']
    orders_dict = {'RUS': (1, 100, 'RUS'), 'CAN': (2, 150, 'CAN'), 'SIN': (3, 250, 'SIN')....}
    """

    distance_dict = {}
    """
    initialise a dict which store all the distance between different destinations
    expected outcome:
    {{'USA': {'CAN': 731, 'MEX': 3024, 'FRN': 6194, 'SPN': 6105, 'GMY': 6739, 'AUS': 7130, 'RUS': 7873, 'CHN': 11236, 'KOR': 11218, 'SIN': 15572}......}
    """
    
    #write a for-loop to add all the distances between destinations to the distance_dict
    for record in locations:
        attribute = record.split(',')
        # record: "USA,CAN,731"
        # attribute: ['USA', 'CAN', '731]
        if attribute[0] in destinations and attribute[1] in destinations:
            # only select locations which is in our destination list
            if attribute[0] not in distance_dict:
                distance_dict[attribute[0]] = {attribute[1]: int(attribute[2])}
            else:
                distance_dict[attribute[0]][attribute[1]] = int(attribute[2])
            # add the distances and country names into distance_dict

    sorted_destination_from_start = sorted(distance_dict[start_location].items(), key=lambda x: x[1], reverse=True)
    #sort all the destinations from start_location in decending order
    #expected output:
    #[('SIN', 15572), ('CHN', 11236), ('KOR', 11218), ('RUS', 7873), ('AUS', 7130), ('GMY', 6739), ('FRN', 6194), ('SPN', 6105), ('MEX', 3024), ('CAN', 731)]
 
    max_list = []
    
    #initialise a dict to give each truck an index and keep track of the location of the truck and the total distance travelled
    truck_dict = {}
    for i in range(number_of_trucks):
        max_list.append([])
        truck_dict[i] = (start_location, 0)
        #start from the start_location
        #expected outcome
        #{0: ('USA', 0), 1: ('USA', 0), 2: ('USA', 0)}

 
#**************************************************
#Use two for-loop to implement a greedy algorithm
#always find the truck with the smallest total travel distance
#assign the new task to it
#**************************************************

    for sorted_order in sorted_destination_from_start:
        # start from the furthest all the way to the nearest
        destination = sorted_order[0]
        order = orders_dict[destination]
        min_distance = 100000000000000000 #initialise min_distance

        for i in range(number_of_trucks):
            # loop through all the trucks
            distance = distance_dict[truck_dict[i][0]][destination]
            """
            truck_dict[i][0] is the current location of the truck
            distance_dict[truck_dict[i][0]][destination] will return the distance from the current location to the destination
            """

            current_truck_distance = distance + truck_dict[i][1]
            #truck_dict[i][1] is the todal distance that a truck has travelled
    
           
            if current_truck_distance < min_distance:
                truck_with_min_distance_index = i
                # assign this task to this truck if it's total travel distance will be the shortest
                min_distance = current_truck_distance
                #update min_distance
            
        truck_dict[truck_with_min_distance_index] = (destination, min_distance)
        max_list[truck_with_min_distance_index].append(order)

    return max_list
