import heapq as min_heap_esque_queue
import copy

# because it sort of acts like a min heap
# Below are some built-in puzzles to allow quick testing.
class TreeNode:
    def __init__(self, parent, puzzle, cost, heuristic): # Initialize the TreeNode - constructor
        self.parent = parent
        self.puzzle = puzzle
        self.cost = cost  # g(n)
        self.heuristic = heuristic  # h(n)
        self.total_cost = cost + heuristic  # f(n)

    def __lt__(self, other):
        return self.total_cost < other.total_cost  # helps with the comparison on heapq

    def solvable(self): # Check if the puzzle is solvable
        inversions = 0
        for i in range(3):
            for j in range(3):
                if self.puzzle[i][j] == 0:
                    continue
                for k in range(i, 3):
                    l = j + 1 if k == i else 0
                    while l < 3:
                        if self.puzzle[k][l] == 0:
                            continue
                        if self.puzzle[i][j] > self.puzzle[k][l]:
                            inversions += 1 # Count the number of inversions to find out if its even and solvable
                        l += 1
        return inversions % 2 == 0
        
    def solved(self): # Check if the puzzle is solved - boolean
        return self.puzzle == eight_goal_state
    
    def puzzle_to_tuple(self): # Convert the puzzle to a tuple
        return tuple(tuple(row) for row in self.puzzle)
    
    def blank_spot(self): # Find the blank spot in the puzzle
        for i in range(3):
            for j in range(3):
                if self.puzzle[i][j] == 0:
                    return i, j
    
    def generate_children(self, heuristicName): # Generate children of the current node
        children = []
        x, y = self.blank_spot()
        moves = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # left, right, up, down
        
        for x_change, y_change in moves: 
            new_x, new_y = x + x_change, y + y_change 
            if 0 <= new_x < 3 and 0 <= new_y < 3:
                new_puzzle = copy.deepcopy(self.puzzle)
                new_puzzle[x][y], new_puzzle[new_x][new_y] = new_puzzle[new_x][new_y], new_puzzle[x][y]

                new_cost = self.cost + 1  # g(n) increases
                new_heuristic = 0 #UCS

                if heuristicName == "Misplaced Tile Heuristic":
                    new_heuristic = misplaced_tile_heuristic(new_puzzle)
                elif heuristicName == "Manhattan Distance Heuristic":
                    new_heuristic = manhattan_distance_heuristic(new_puzzle)

                child = TreeNode(self, new_puzzle, new_cost, new_heuristic)
                children.append(child)

        return children

# Given test case puzzles

trivial = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]

veryEasy = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 0, 8]
]

easy = [
    [1, 2, 0],
    [4, 5, 3],
    [7, 8, 6]
]

doable = [
    [0, 1, 2],
    [4, 5, 3],
    [7, 8, 6]
]

oh_boy = [
    [8, 7, 1],
    [6, 0, 2],
    [5, 4, 3]
]

eight_goal_state = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]

############################################################################################################

def init_default_puzzle_mode(): # This function allows the user to select a default puzzle from the given List
    selected_difficulty = input("You wish to use a default puzzle. Please enter a desired difficulty on a scale from 0 to 4." + '\n')
    if selected_difficulty == "0":
        print("Difficulty of 'Trivial' selected.")
        return trivial
    if selected_difficulty == "1":
        print("Difficulty of 'Very Easy' selected.")
        return veryEasy
    if selected_difficulty == "2":
        print("Difficulty of 'Easy' selected.")
        return easy
    if selected_difficulty == "3":
        print("Difficulty of 'Doable' selected.")
        return doable
    if selected_difficulty == "4":
        print("Difficulty of 'Oh Boy' selected.")
        return oh_boy 
    
############################################################################################################

def misplaced_tile_heuristic(puzzle): # Calculate the misplaced tiles heuristic
        return sum (
            1
            for i in range(3)
                for j in range(3)
                    if puzzle[i][j] != 0 and puzzle[i][j] != eight_goal_state[i][j] # Count tiles not in the goal position
        )

def manhattan_distance_heuristic(puzzle): # Calculate the manhattan distance heuristic
    distance = 0
    for i in range(3):
        for j in range(3):
            index = puzzle[i][j]
            if index != 0:  # Ignore the blank tile
                x_goal, y_goal = divmod(index - 1, 3)  # Goal position of value
                distance += abs(i - x_goal) + abs(j - y_goal)  # Manhattan distance
    return distance

def print_puzzle(puzzle): # Print the puzzle
    for i in range(0, 3):
        print(puzzle[i])
    print('\n')

############################################################################################################

def select_and_init_algorithm(puzzle): # Select and initialize the algorithm, and find out which algorithm the user wants to use
    algorithm = input("Select algorithm. (1) for Uniform Cost Search, (2) for the Misplaced Tile Heuristic, "
    "or (3) the Manhattan Distance Heuristic." + '\n')
    
    if algorithm == "1":
        uniform_cost_search(puzzle, 0, "Uniform Cost Search")
    elif algorithm == "2":
        uniform_cost_search(puzzle, misplaced_tile_heuristic(puzzle), "Misplaced Tile Heuristic")
    elif algorithm == "3":
        uniform_cost_search(puzzle, manhattan_distance_heuristic(puzzle), "Manhattan Distance Heuristic")
    else:
        print("Invalid selection. Please try again.")
        select_and_init_algorithm(puzzle)

############################################################################################################
 
def uniform_cost_search(puzzle, heuristic, heuristicName): 
    starting_node = TreeNode(None, puzzle, 0, heuristic) # initialize the root node
    working_queue = []
    repeated_states = {}

    min_heap_esque_queue.heappush(working_queue, starting_node) # push the root node to the queue
    num_nodes_expanded = 0
    max_queue_size = 0
    repeated_states[starting_node.puzzle_to_tuple()] = starting_node.cost
    depthcounter = 0
    
    while len(working_queue) > 0: # while the queue is not empty
        max_queue_size = max(len(working_queue), max_queue_size)
        node_from_queue = min_heap_esque_queue.heappop(working_queue)

        if node_from_queue.solved(): # if the goal state is reached
            solution_path = []
            while node_from_queue:
                solution_path.append(node_from_queue)
                node_from_queue = node_from_queue.parent
            
            for node in reversed(solution_path): # print the solution path by backtracking from the parent pointers
                depthcounter += 1
                print(f"The best state to expand with a g(n) of 1 and h(n) of {node.heuristic} is...")                
                print_puzzle(node.puzzle)

            print("Goal State Reached!") 
            print("Depth of solution:", depthcounter)
            print("Number of nodes expanded:", num_nodes_expanded)
            print("Max queue size:", max_queue_size)
            return solution_path

        num_nodes_expanded += 1

        for child in node_from_queue.generate_children(heuristicName): # generate children of the current node
            child_tuple = child.puzzle_to_tuple()

            if child_tuple not in repeated_states or child.cost < repeated_states[child_tuple]:
                repeated_states[child_tuple] = child.cost
                min_heap_esque_queue.heappush(working_queue, child)

    ############################################################################################################

def main(): # given code by Dr. Keogh
    puzzle_mode = input("Welcome to an 8 Puzzle Solver. Type '1' to use a default puzzle, or '2' to create your own." + '\n')

    if puzzle_mode == "1":
        select_and_init_algorithm(init_default_puzzle_mode())

    if puzzle_mode == "2":

        print("Enter your puzzle, using a zero to represent the blank. " + "Please only enter valid 8 puzzles. Enter the puzzle demilimiting " +
        "the numbers with a space. RET only when finished." + '\n')

        puzzle_row_one = input("Enter the first row: ")
        puzzle_row_two = input("Enter the second row: ")
        puzzle_row_three = input("Enter the third 1row: ")
        puzzle_row_one = puzzle_row_one.split()
        puzzle_row_two = puzzle_row_two.split()
        puzzle_row_three = puzzle_row_three.split()
    
        for i in range(0, 3):
            puzzle_row_one[i] = int(puzzle_row_one[i])
            puzzle_row_two[i] = int(puzzle_row_two[i])
            puzzle_row_three[i] = int(puzzle_row_three[i])
       
        user_puzzle = [puzzle_row_one, puzzle_row_two, puzzle_row_three]
        if not TreeNode(None, user_puzzle, 0, 0).solvable():
            print("Invalid puzzle. Please try again.")
            main()
        else:
            select_and_init_algorithm(user_puzzle)

if __name__ == "__main__": #just here to call the main function
    main()