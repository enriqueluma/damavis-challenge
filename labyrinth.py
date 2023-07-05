from queue import Queue

# Returns if a movement can be made. The conditions are the following:
# (1) the rod is inside the labyrinth
# (2) the rod does not move to positions with with blocked cells, ie. '#'
# (3) the position has not been visited before in this orientation
def valid_Movement(row, col, orientation, labyrinth, visited):
    is_valid = False
    if orientation:
        if row >= 0 and row < len(labyrinth) and col -1 >= 0 and col +1 < len(labyrinth[0]) \
        and labyrinth[row][col-1] != '#' and labyrinth[row][col] != '#' and labyrinth[row][col+1] != '#' \
        and not visited[orientation][row][col]:
            is_valid = True
    else:
        if row -1 >= 0 and row +1 < len(labyrinth) and col >= 0 and col < len(labyrinth[0]) \
        and labyrinth[row-1][col] != '#' and labyrinth[row][col] != '#' and labyrinth[row+1][col] != '#' \
        and not visited[orientation][row][col]:
            is_valid = True
    
    return is_valid

# Returns if a change of orientation can be made. The conditions are the following:
# (1) 3x3 area sorrunding center of the rod is clear from blocked cells and walls.
# (2) the position has not been visited before in this orientation.
def valid_Rotation(row, col, orientation, labyrinth, visited):
    is_valid = False
    if row > 0 and row < len(labyrinth) -1 and col > 0 and col < len(labyrinth[0]) -1 \
    and labyrinth[row-1][col-1] != '#' and labyrinth[row-1][col] != '#' and labyrinth[row-1][col+1] != '#' \
    and labyrinth[row][col -1] != '#' and labyrinth[row][col +1] != '#' \
    and labyrinth[row+1][col-1] != '#' and labyrinth[row+1][col] != '#' and labyrinth[row+1][col+1] != '#' \
    and not visited[orientation][row][col]:
        is_valid = True

    return is_valid

def bfs(labyrinth):
    # rod's center initial position. If orientation == True, the rod is horizontally placed. If not, it's vertically placed.
    row = 0
    col = 1
    orientation = True

    # Rod's center position for both possible solutions. It depends on how the rod arrives to the destination (horizontal or vertical).
    dest1_row = len(labyrinth) -2
    dest1_col = len(labyrinth[0]) -1
    dest2_row = len(labyrinth) -1
    dest2_col = len(labyrinth[0]) -2

    # Minimum required moves to get to the destination. -1 if it can't reach the destination. 
    min_moves = -1

    # Matrix of positions visited by rod's center. Initilized as False. 
    # It's 3Dimensional as I consider if the rod's been in a position in both of it's orientations (V or H)
    visited = [[[False for x in range(len(labyrinth[0]))] for y in range(len(labyrinth))] for z in range(2)]
    visited[orientation][row][col] = True

    # Queue (FIFO) of positions to explore. Initial position gets queued.
    # Third value stored (0) equals to the number of moves required to get to the current position from the start position.
    q_to_explore = Queue()
    q_to_explore.put((row, col, orientation, 0))
    
    # Loop until finding the destination or until exploring all possible positions. 
    while not q_to_explore.empty() and min_moves == -1:

        # First position on the queue gets dequed
        (row, col, orientation, moves) = q_to_explore.get()

        # Check if current position equals to one of the destinations 
        # If so, we update the min_moves value
        if (row == dest1_row and col == dest1_col) or (row == dest2_row and col == dest2_col):
            min_moves = moves
        
        # If not, we check which one of the 5 possible moves can be performed.
        # If the movement can be performed, we queue the affected position and we change the value to true on the visited positions matrix.
        else:
            # Check if the rod can move to the left
            if valid_Movement(row, col+1, orientation, labyrinth, visited):
                visited[orientation][row][col+1] = True
                q_to_explore.put((row, col+1, orientation, moves+1))
            
            # Check if the rod can move down
            if valid_Movement(row+1, col, orientation, labyrinth, visited):
                visited[orientation][row+1][col] = True
                q_to_explore.put((row+1, col, orientation, moves+1))

            # Check if the rod can move to the right
            if valid_Movement(row, col-1, orientation, labyrinth, visited):
                visited[orientation][row][col-1] = True
                q_to_explore.put((row, col-1, orientation, moves+1))

            # Check if the rod can move up
            if valid_Movement(row-1, col, orientation, labyrinth, visited):
                visited[orientation][row-1][col] = True
                q_to_explore.put((row-1, col, orientation, moves+1))
            
            # Check if the rod can change orientation. Vertical to Horizontal or viceversa.
            if valid_Rotation(row, col, not orientation, labyrinth, visited):
                visited[not orientation][row][col] = True
                q_to_explore.put((row, col, not orientation, moves+1)) 

    return min_moves

def solution(labyrinth):
    # Before solving the problem I check that the initial positions of the rod are not occupied by blocked cells as I don't wan't to assume that they are always free
    min_moves = -1

    if labyrinth[0][0] == '.' and labyrinth[0][1] == '.' and labyrinth[0][2] == '.':
         # Algorithm chosen to solve the minimum path of the labyrinth is BFS. It is done that way so I can implement other algorithms, such as A*,in the future. 
        min_moves = bfs(labyrinth)

    return min_moves 

def main():
    # Test labyrinths extracted for the challenge description
    test1 = [
        [".",".",".",".",".",".",".",".","."],
        ["#",".",".",".","#",".",".",".","."],
        [".",".",".",".","#",".",".",".","."],
        [".","#",".",".",".",".",".","#","."],
        [".","#",".",".",".",".",".","#","."]
    ]

    test2 = [
        [".",".",".",".",".",".",".",".","."],
        ["#",".",".",".","#",".",".","#","."],
        [".",".",".",".","#",".",".",".","."],
        [".","#",".",".",".",".",".","#","."],
        [".","#",".",".",".",".",".","#","."]
    ]

    test3 = [
        [".",".","."],
        [".",".","."],
        [".",".","."]
    ]

    test4 = [
        [".",".",".",".",".",".",".",".",".","."],
        [".","#",".",".",".",".","#",".",".","."],
        [".","#",".",".",".",".",".",".",".","."],
        [".",".",".",".",".",".",".",".",".","."],
        [".",".",".",".",".",".",".",".",".","."],
        [".","#",".",".",".",".",".",".",".","."],
        [".","#",".",".",".","#",".",".",".","."],
        [".",".",".",".",".",".","#",".",".","."],
        [".",".",".",".",".",".",".",".",".","."],
        [".",".",".",".",".",".",".",".",".","."]
    ]

    # We select one of the labyrinths and look for the solution. The solution, then, gets printed.
    labyrinth = test1
    moves = solution(labyrinth)
    print ("Result", moves)
    
main()

