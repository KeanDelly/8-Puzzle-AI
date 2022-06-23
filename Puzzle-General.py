
#Importing time module to help gauge performance
import time


"""
Calculates a nodes f(n) using the formula f(n) = g(n) + h(n)
"""
def calc_heuristic(method, unvisited_states, goal_state, node_index):
    current_state = unvisited_states[node_index]["state"]
    dist_from_start = unvisited_states[node_index]["level"]
    if method == 1:
        misplaced_tiles = 0
        for i in range(0,len(goal_state)):
            if current_state[i] == goal_state[i]:
                misplaced_tiles+=1
        return (dist_from_start + misplaced_tiles)
    if method == 2:
        total_travel = []
        for i in range(0,len(current_state)):
            current_dist = 0
            goal_pos = 0
            #calc position in goal
            for j in range(0,len(goal_state)):
                if current_state[i] == goal_state[j]:
                    goal_pos = j
                    break
            #Calc vertical
            ver_dist = (abs(i-j)//3)
            #cal Horizontal
            hor_dist = abs((i%3)-(j%3))
            #Sum and append
            total_travel.append(hor_dist+ver_dist)
        return (sum(total_travel)+dist_from_start)
"""
Function to determine the node with the lowest f(n) and return it
"""
def get_best_node(unvisited_states):
    best_node = list(unvisited_states.keys())[0] #get first key in dict
    for key in unvisited_states:
        if unvisited_states[key]["value"] < unvisited_states[best_node]["value"]:
            best_node = key
    return best_node


"""
Returns a carbon-copy of the solution state provided to it
""" 
def copy_state(state):
    new_state = []
    for num in state:
        new_state.append(num)
    return new_state


"""
Function that generates successor nodes from the current node using a process of elimination
"""
def generate_children(unvisited_states, node_index, goal_state, method):
    #Define and initialise empty lists for successor nodes and current state
    successor_nodes =[]
    current_state = []
    current_state = copy_state(unvisited_states[node_index]["state"])
    level = unvisited_states[node_index]["level"]
    
    #Find index of the blank square, set it equal to blank index
    for i in range(0,9):
        if current_state[i] == 0:
            blank_index = i
    #use elimination to generate children
    #Determine whether the blank space can be moved upwards 
    if blank_index-3 >= 0:
        current_state_temp = copy_state(current_state)
        current_state_temp[blank_index] = current_state_temp[blank_index-3]
        current_state_temp[blank_index-3] = 0
        successor_nodes.append(current_state_temp)
    #Determine if the Blank Space can be moved downwards
    if blank_index+3 <= 8:
        current_state_temp = copy_state(current_state)
        current_state_temp[blank_index] = current_state_temp[blank_index+3]
        current_state_temp[blank_index+3] = 0
        successor_nodes.append(current_state_temp)
    
    #Determine which column the blank space is in
    blank_col = (blank_index+1) % 3
    match blank_col:
        case 0: # the blank space can move to the left
            current_state_temp = copy_state(current_state)
            current_state_temp[blank_index] = current_state_temp[blank_index-1]
            current_state_temp[blank_index-1] = 0
            successor_nodes.append(current_state_temp)
        case 1: #The blank space can move to the right
            current_state_temp = copy_state(current_state)
            current_state_temp[blank_index] = current_state_temp[blank_index+1]
            current_state_temp[blank_index+1] = 0
            successor_nodes.append(current_state_temp)
        case 2: # The blank space can move both right and left
            current_state_temp = copy_state(current_state)
            current_state_temp[blank_index] = current_state_temp[blank_index+1]
            current_state_temp[blank_index+1] = 0
            successor_nodes.append(current_state_temp)

            current_state_temp = copy_state(current_state)
            current_state_temp[blank_index] = current_state_temp[blank_index-1]
            current_state_temp[blank_index-1] = 0
            successor_nodes.append(current_state_temp)
    return successor_nodes


"""
Function to determine whether an identical state exists in a previously explored node
"""
def is_In(visited_states, state):
    state_exists = False
    for key in visited_states:
        if visited_states[key]["state"] == state:
            state_exists = True
            break
    return state_exists
    

"""
Function that outputs the solution path for the Puzzle, from Start State to Goal State
"""
def display_path(visited_states, solution_index):
    root_found = False
    current_node = solution_index
    solution_path = []
    #Generates a solution path by appending recusively the parent of a child node from the dolution to the start state
    while root_found == False:
        solution_path.append(current_node)
        if visited_states[current_node]["parent"] == -1:
            root_found = True
        else:
            current_node = visited_states[current_node]["parent"]
    #Outputs the Solution path to the User
    print("Start Node")
    for node in solution_path[::-1]:
        state = visited_states[node]["state"]
        print("---------")
        print("{}|{}|{}".format(state[0], state[1], state[2]))
        print("{}|{}|{}".format(state[3], state[4], state[5]))
        print("{}|{}|{}".format(state[6], state[7], state[8]))
    print("---------")
    print("Goal Node")


def a_star(method, start_state, goal_state):
    #Defining and Initialising the Start State and Solution State of an 8-Puzzle Problem
    INITIAL_STATE = [int(x) for x in start_state]
    GOAL_STATE = [int(x) for x in goal_state]
    print("Confirming the Initial State is {}".format(INITIAL_STATE))
    print("Confirming the Goal State is".format(GOAL_STATE))

    #Defining and Initialising dictionaries to follow the explored(visited) and unexplored(unvisited) states
    unvisited_states = {}
    visited_states = {}

    #Defining and initialising the node index variable, this is used as an ambiguous key to store nodes under. 
    #Also allows for the backtracking of nodes in order to output the full solution path 
    node_index = 0
    
    #Creation of the Puzzles Initial State, aswell as calculating its f(n) value, and incrementing the node_index by 1, indicating a nodes creation
    unvisited_states.update({node_index:{"state": INITIAL_STATE, "level":0, "parent": -1, "value": -1 }})
    unvisited_states[node_index]["value"] = calc_heuristic(method, unvisited_states, GOAL_STATE, node_index)
    node_index +=1

    #Defining the while loop structure to handle the state by state generation of successor nodes, determination of the solution being reached, and determination of whether a solution exists.
    finished = False
    goal_index = 0
    while finished == False:
        #Determine if there are still nodes to explore, if not the Puzzle has no solution from its initial state, therefore program exits. 
        if len(unvisited_states) == 0:
            finished = True
            print("No more Nodes to explore")
        else:
            #Select the best node to explore from the dictionary of unexplored nodes, using the get_best_node function defined above
            current_node = get_best_node(unvisited_states)

            #determine whether current node is goal, indicated by an f(n) == 0,
            #If node is goal, add current node to dictionary of visited nodes and break out of the loop
            if unvisited_states[current_node]["state"] == GOAL_STATE:
                print("Goal node has been found with index ", current_node)
                visited_states.update({current_node:{"state":unvisited_states[current_node]["state"],"level":unvisited_states[current_node]["level"], "parent":unvisited_states[current_node]["parent"], "value":unvisited_states[current_node]["value"]}})
                del unvisited_states[current_node]
                finished=True
                break
            else:
                #Generate the successor nodes of the current node using the generate_children method
                successor_nodes = generate_children(unvisited_states, current_node, method, GOAL_STATE)
                #Determine whether each successor node should be explored further, or not based on whether a node has already been explored which contains an identical state
                for state in successor_nodes:
                    if is_In(visited_states, state) == False:  # Is_In Used to prevent program flow entering infinite loop
                        #Creating successor nodes with parent = current nodes id(index), calculating their f(n), and adding them to the dictionary of unexplored states, incrementing the node_index for each.
                        unvisited_states.update({node_index:{"state": state, "level":(unvisited_states[current_node]["level"] +1), "parent": current_node, "value": -1 }})
                        unvisited_states[node_index]["value"] = calc_heuristic(method, unvisited_states, GOAL_STATE, node_index)
                        node_index +=1

                #Add the current node to the visited_states dictionary, and remove it from the unexplored_states dictionary. 
                visited_states.update({current_node:{"state":unvisited_states[current_node]["state"],"level":unvisited_states[current_node]["level"], "parent":unvisited_states[current_node]["parent"], "value":unvisited_states[current_node]["value"]}})
                del unvisited_states[current_node]
    
    #pass the list of visited states, and solution node to display_path function to output solution path to user    
    display_path(visited_states, current_node)


"""
Function Allowing user to Select the heuristic to be used in the solving of the 8-Puzzle,
and to input both the initial state and the goal state
"""
def puzzle_intro():
    print("Welcome to the 8-Puzzle Problem Solver")
    print("This is a genral version of the 8-Puzzle Problem Solver")
    print("Please input the following as comma-seperated list of 9 items, with 0 representing a blank space.")
    print("Example Input: 0,1,2,3,4,5,6,7,8")
    start_state = input("Please input the start state")
    goal_state = input("Please enter the Goal state")
    print("[1] Hamming Method")
    print("[2] Manhatten Method")
    while True:
        method = int(input("Which of the above methods should be used to calculate the heuristic?"))
        match method:
            case 1:
                method = 1
                print("Hamming Method Script Started")
                start_time = time.time()
                a_star(1, start_state.split(","), goal_state.split(","))
                print("--- %s seconds ---" % (time.time() - start_time))
                break
            case 2:
                method = 2
                print("Manhatten method script started")
                start_time = time.time()
                a_star(2, start_state.split(","), goal_state.split(","))
                print("--- %s seconds ---" % (time.time() - start_time))
                break
            case _:
                print("Method Undefined, please enter either 1 or 2.")


if __name__ == "__main__":
    puzzle_intro()
