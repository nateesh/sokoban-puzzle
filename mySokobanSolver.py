
'''

    Sokoban assignment 
    IFN 680 - Artificial Intelligence and Machine Learning
    mySokobanSolver.py    

'''

import search 
from time import time, ctime
from sokoban import Warehouse


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def my_team():
    '''
    Return the list of the team members of this assignment submission as a list
    of triplet of the form (student_number, first_name, last_name)
    '''
    return [ ('Nina'), ('Nathan') ]
    

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -



class SokobanPuzzle(search.Problem):
    '''
    An instance of the class 'SokobanPuzzle' represents a Sokoban puzzle.
    An instance contains information about the walls, the targets, the boxes
    and the worker.

    Your implementation should be fully compatible with the search functions of 
    the provided module 'search.py'. 
    
    '''
    
    def __init__(self, warehouse):
        ''' Initialises the instance of the SokobanPuzzle class, which is 
        derived from the Search module Problem class
        
        @param: a valid Warehouse object
        - Initialises static features of problem instance (self.walls, self.targets, self.weights)
        - Initialises dynamic features of as problem as 'self.initial', the first frontier of the search tree/graph.
        '''
        
        # Check warehouse param is an instance of class sokoban.Warehouse
        assert isinstance(warehouse, Warehouse)
           
        self.weights = warehouse.weights
        self.walls = tuple(warehouse.walls)
        self.goal = tuple(warehouse.targets)
        self.initial = tuple([warehouse.worker] + warehouse.boxes)
        
        # Logic to initialise any warehouse corners into problem instance
        def find_corners():
            """ Finds all the corners in a given Warehouse class and returns a list of tuples
            
            @param: a valid Warehouse object
            @return: a list of  valid corners, of tuple type.
            """
        
            def corner_check(x_check: int, y_check: int):
                """ Nested function to check if given x, y coordinates are a valid corner.
                
                @params: an x coordinate (int), a y coordinate (int)
                @return: valid corner of type tuple
                """
                if ((x_check, y) in self.walls and 
                    (x, y_check) in self.walls and 
                    (x_check,y_check) not in self.goal):
                    corners.append((x_check, y_check))
                    
            corners = [] # initialise empty list of corners
            for wall in self.walls:
                x, y = wall
                
                # check for corners cases North-East, NW, SE and SW of a given wall
                corner_check(x+1, y+1)
                corner_check(x-1, y+1)
                corner_check(x+1, y-1)
                corner_check(x-1, y-1)
            return corners
        
        # Initialise all valid corners for the given warehouse instance
        self.corners = find_corners()
        # corners are used in the actions function to limit movements that result
        # in the box being pushed into a corner
    
    def actions(self, state):
        """ Function to compute valid actions (up, down, left, right) of a given state.
        
        @param: current state as defined by search.Node class
        @return: Return the list of legal actions that can be executed in the given state.
        """
                
        # Define state related variables
        
        x, y = state[0]         # Worker coordinates
        boxes = state[1:]       # Box coordinates
        
        # Initialise empty list of actions
        L = []
        
        # Enumerate possible worker offset coordinates based on movement 
        worker_up = [x, y-1]    # Up
        worker_down = [x, y+1]  # Down
        worker_left = [x-1, y]  # Left
        worker_right = [x+1, y] # Right
        
        # Enumerate possible box offset coordinates based on worker movement
        box_up = [x, y-2]       # Up
        box_down = [x, y+2]     # Down
        box_left = [x-2, y]     # Left
        box_right = [x+2, y]    # Right
        
        def worker_move(worker_offset: list[int, int]) -> bool:
            """ Nested function to check if a movement that only changes the coordinates of a worker is legal.
            
            @param: worker offet coordinates for given move direction
            
            @return: bool, True if criteria are met
            """

            return (tuple(worker_offset) not in self.walls and 
                    tuple(worker_offset) not in boxes)
        

        def worker_box_move(worker_offset: list[int, int], box_offset: list[int, int]) -> bool:
            """ Nested function to check if a movement that changes the coordinates of both the worker AND a box is legal.
            
            @param worker_offset: worker offset coordinates for given move direction
            @param box_offset: box offset cooordinates for 
            @return: bool, True if criteria are met
            """
            
            return (tuple(worker_offset) in boxes and
                    tuple(box_offset) not in self.walls and
                    tuple(box_offset) not in boxes and
                    tuple(box_offset) not in self.corners)
                                
        # Conditions for legal Up move  
        if (worker_move(worker_up) or
            worker_box_move(worker_up, box_up)):
            L.append('Up')
            
        # Conditions for legal Down move 
        if (worker_move(worker_down) or 
            worker_box_move(worker_down, box_down)):
            L.append('Down')
            
        # Conditions for legal left move
        if (worker_move(worker_left) or
            worker_box_move(worker_left, box_left)):
            L.append('Left')
            
        # Conditions for legal Right move
        if (worker_move(worker_right) or
            worker_box_move(worker_right, box_right)):
            L.append('Right')
               
        
        return L # Returns list of valid actions for given node
            
    def result(self, state, action):
        """
        Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state). 
        
        Applying action to state results in:
        next_state = worker_update + box_update
            where:
            worker_update = new worker coordinates after action
            box_update = new box coordinates (if any) after worker_update
        """
        
        # Define state related variables 
        x, y = state[0]     # worker coordinates
        boxes = state[1:]   # list of boxes
        
        # Define box variable in the case no boxes are moved
        box_update = state[1:]
        
        def boxes_update(newbox: tuple[int, int]) -> tuple[int, int]:
            """ Function to update the boxes when a worker moves a box
            @param: tuple with coordinates of new box location
            @return: list of updated boxes
            """
            index = state.index(worker_update)    
            new_boxes = tuple(state[1:index]) + (newbox,) + tuple(state[index+1:])
            return new_boxes
                
        if action == 'Up':
            worker_update = (x, y-1)
            if worker_update in boxes: # 
                box_update = boxes_update((x, y-2))
        
        if action == 'Down':
            worker_update = (x, y+1)
            if worker_update in boxes:
                box_update = boxes_update((x, y+2))
        
        if action == 'Left':
            worker_update = (x-1, y)
            if worker_update in boxes:
                box_update = boxes_update((x-2, y))
            
        if action == 'Right':
            worker_update = (x+1, y)
            if worker_update in boxes:
                box_update = boxes_update((x+2, y))

        next_state = (worker_update,) + box_update
                
        return tuple(next_state) # use tuple to make the state hashable

    def goal_test(self, state):
        """ Function to test if state matches goal
        @param: must be of type node.state
        
        @return: bool, True if state == goal
        """
        boxes_state = state[1:]
                
        goal_test = set(boxes_state) == set(self.goal)
        
        return goal_test
    
    def path_cost(self, c, state1, action, state2):
        """
        Return the cost of a solution path that arrives at state2 from
        state1, assuming cost c to get up to state1.
        
        @return: c + worker movement cost + box movement cost (if applicable)
        """
        
        cur_boxes = list(state1[1:])   # define boxes variable from current state
        new_boxes = list(state2[1:])   # define boxes variable from future state

        current_cost = c
        WORKER_MOVE_COST = 1
        box_move_cost = 0
        
        
        try: 
            # If a box has moved, get its index
            index_moved_box = list(set(new_boxes) - set(cur_boxes))[0]
            
            # Get the weight of the box that has moved and assign it a move cost variable
            box_move_cost = self.weights[new_boxes.index(index_moved_box)]
            
        except:
            None
        
        return current_cost + WORKER_MOVE_COST + box_move_cost
    
    def h(self, node):
        '''
        This function calculate the heuristic between given node
        Description: using Manhatan distance and select minimum distances between locations
            + Step 1: Calculate the mininmum distance between worker and boxes
            + Step 2: Calculate the mininmum distance between boxes and targets
            + Step 3: Sum those minimum distances to get heuristic for A* graph search module
    
        @param node: the warehouse's state
    
        @return: the heuristic value between given node 
                which is the minimum value between worker => boxes plus boxes => targets
        '''
        worker = node.state[0]
        boxes = node.state[1:]
        targets = self.goal
        
        sum = 0
        
        # Call calcluate_minimum_distance to get minimum distance between worker and boxes
        workerMin = calcluate_minimum_distance(worker, boxes)
        sum += workerMin
        
        for box in boxes:
            # Call calcluate_minimum_distance to get minimum distance between box and targets
            boxMin = calcluate_minimum_distance(box, targets)
            sum += boxMin
            
        return sum
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def check_elem_action_seq(warehouse, action_seq):
    '''
    
    Determine if the sequence of actions listed in 'action_seq' is legal or not.
    
    Important notes:
      - a legal sequence of actions does not necessarily solve the puzzle.
      - an action is legal even if it pushes a box onto a taboo cell, except valid corners. 
        
    @param warehouse: a valid Warehouse object

    @param action_seq: a sequence of legal actions.
           For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
           
    @return
        The string 'Impossible', if one of the action was not valid.
           For example, if the agent tries to push two boxes at the same time,
                        or push a box into a wall.
        Otherwise, if all actions were successful, return                 
               A string representing the state of the puzzle after applying
               the sequence of actions.  This must be the same string as the
               string returned by the method  Warehouse.__str__()
    '''

    boxes = list(warehouse.boxes)
    worker = list(warehouse.worker)
    cur_warehouse = warehouse.copy(worker, boxes)
    
    for action in action_seq:  
        # Check if the given action sequence is valid or not by calling is_possible_move()
        # If it's not valid move => return Impossible
        if is_possible_move(cur_warehouse, action):
            x, y = find_steps(action)
            worker[0] += x
            worker[1] += y
            
            # Make sure all boxes are the same with the new worker position
            # Make the box follow the same direction with worker's move
            for i, box in enumerate(boxes):
                if box == (worker[0], worker[1]):
                    box_x = box[0] + x
                    box_y = box[1] + y
                    boxes[i] = (box_x, box_y)
            cur_warehouse = warehouse.copy(worker, boxes)
        else:
            return "Impossible"
        
    cur_warehouse = warehouse.copy(worker, boxes)    
    return cur_warehouse.__str__()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def solve_weighted_sokoban(warehouse):
    '''
    This function analyses the given warehouse.
    It returns the two items. The first item is an action sequence solution. 
    The second item is the total cost of this action sequence.
    
    @param 
     warehouse: a valid Warehouse object

    @return
    
        If puzzle cannot be solved 
            return 'Impossible', None
        
        If a solution was found, 
            return S, C 
            where S is a list of actions that solves
            the given puzzle coded with 'Left', 'Right', 'Up', 'Down'
            For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
            If the puzzle is already in a goal state, simply return []
            C is the total cost of the action sequence C

    '''
    puzzle = SokobanPuzzle(warehouse)
    sol_gs = search.astar_graph_search(puzzle)
    
    S = []
    if sol_gs is None:
        return "Impossible", None
    if sol_gs.solution() is []:
        return S, 0
    else:
        S = sol_gs.solution()
        C = sol_gs.path_cost
    return S, C

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def is_possible_move(warehouse, action):
    '''
    This Function to check next move is valid or invalid
    Description: 
        Receive given action and check if those actions is possible in given warehouse or not.
        By checking behind or infront not in those cases:
                + Case 1: We need to check if the worker's position is inside wall or not
                + Case 2: The worker moves to a box to position where there is another box behind
                + Case 3: Worker moves box to the wall
    
    @param warehouse: Warehouse
    @param action: the sequnce of action. For example: ['Righ','Right','Down']
    
    @return
        True: if the move is possible
        False: if the move is impossible
    '''
    worker_x = warehouse.worker[0]
    worker_y = warehouse.worker[1]
    
    boxes = warehouse.boxes
    walls = warehouse.walls
    
    # Check the action in set
    # number to x and y
    # next_x and next_y is to check if there is anything behind/infront the worker destination
    x = 0 
    y = 0
    next_x = 0
    next_y = 0
    if (action == "Up"):
        y  -= 1
        next_y -= 2
    elif (action == "Down"):
        y  += 1
        next_y += 2
    elif (action == "Left"):
        x  -= 1
        next_x -= 2
    elif (action == "Right"):
        x  += 1
        next_x += 2
    else:
        return False
    
    # Check for every action
    # Case 1: We need to check if the worker's position is inside wall or not
    # Case 2: The worker moves to a box to position where there is another box behind
    # Case 3: Worker moves box to the wall
    if (worker_x + x, worker_y + y) in walls:
        return False
    elif (worker_x + x, worker_y + y) in boxes and (worker_x + next_x, worker_y + next_y) in boxes:
        return False
    elif (worker_x + x, worker_y + y) in boxes and (worker_x + next_x, worker_y + next_y) in walls:
        return False
    else:
        return True
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def find_steps(action):
    '''
    This function find the position of x and y in dimension with given actions
    
    @param action: the given action. For example: ['Right','Right','Down']
    
    @return
            x : the actual value of x from action in dimension
            y : the actual value of y from action in dimension
    '''
    x = 0
    y = 0
    if (action == "Up"):
        y -= 1
    elif (action == "Down"):
        y += 1
    elif (action == "Left"):
        x -= 1
    elif (action == "Right"):
        x += 1
    
    return x, y
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  
  
def calculate_manhattan(x_position, y_position):
    '''
    This function calculate the distance between worker and boxes,
    the distance between player and targets which is arguments 
    by applying Manhattan distance calculation.
        In a dimension d1 at (x1, y1) and d2 at (x2, y2), it is |x1 - x2| + |y1 - y2|

    @param x_position: the x position of boxes or targets
    @param y_position: the y position of boxes or targets

    @return: the distance between worker and boxes or player and targets
    '''
    return abs(x_position[0] - y_position[0]) + abs(x_position[1] - y_position[1])
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def calcluate_minimum_distance(start, locations):
    '''
    This function calculate the shortest or the minimum distance between start 
    and locations (worker and boxes, workers and target)

    @param start: the starting point
    @param locations: the destinations

    @return: the shortest distance 
    '''
    for i, item in enumerate(locations):
        # initial value for minimum distance by the first item in input locations
        if i==0:
            min_dist = calculate_manhattan(start, item)
        # get distance from manhanttan distance
        dist = calculate_manhattan(start, item)

        # select minimum distance from minimum distance and distance from Manhanttan
        min_dist = min(dist, min_dist)
            
    return min_dist
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
if __name__ == '__main__':
    
    wh = Warehouse()
    
    #path = "./warehouses/warehouse_09b.txt" # Test case for puzzle is already in a goal state
    path = "./warehouses/warehouse_149.txt"
    name = (path.split("/")[-1]).split(".")[0]
    
    wh.load_warehouse(path) ## wharehouse object

    t0 = time()
    print("- " * 30)
    print(f"- - - Testing {name} @ {ctime()} - - -")
    print("- " * 30)
    puzzle = SokobanPuzzle(wh)

    print(f"Corners: {puzzle.corners}")
    weights = puzzle.weights
    print(f"Weights: {weights}")
    
    boxes = puzzle.initial[1:]
    print(f"Boxes: {boxes}")

    #sol_gs = search.astar_graph_search(puzzle)
    #print(sol_gs.solution())
    # sol_gs = search.breadth_first_tree_search(puzzle)
    answer, cost = solve_weighted_sokoban(wh)
    t1 = time()
    
    
     
    print ("Solver took ",t1-t0, ' seconds')
    print(f"- - - Testing {name} @ {ctime()} - - -")
    print(answer)
    print(f"Path Cost: {cost}")

    #print("\n", check_elem_action_seq(wh, sol_gs.solution()))

