import heapq

def state_check(state):
    """check the format of state, and return corresponding goal state.
       Do NOT edit this function.
       This function was created by the Staff of the University of Wisconsin-Madison"""
    non_zero_numbers = [n for n in state if n != 0]
    num_tiles = len(non_zero_numbers)
    if num_tiles == 0:
        raise ValueError('At least one number is not zero.')
    elif num_tiles > 9:
        raise ValueError('At most nine numbers in the state.')
    matched_seq = list(range(1, num_tiles + 1))
    if len(state) != 9 or not all(isinstance(n, int) for n in state):
        raise ValueError('State must be a list contain 9 integers.')
    elif not all(0 <= n <= 9 for n in state):
        raise ValueError('The number in state must be within [0,9].')
    elif len(set(non_zero_numbers)) != len(non_zero_numbers):
        raise ValueError('State can not have repeated numbers, except 0.')
    elif sorted(non_zero_numbers) != matched_seq:
        raise ValueError('For puzzles with X tiles, the non-zero numbers must be within [1,X], '
                          'and there will be 9-X grids labeled as 0.')
    goal_state = matched_seq
    for _ in range(9 - num_tiles):
        goal_state.append(0)
    return tuple(goal_state)


def H(state):
    """
    INPUT: 
        A state (list of length 9)

    RETURNS:
        An estimate of how many moves away it is from the goal state
    """
    hSum = 0
    for i in range(len(state)):
        if(state[i] == i+1 or state[i] == 0):
            hSum += 0
        else:
            across = abs((state[i]-1)%3 - i%3)
            down = abs(int((state[i]-1)/3) - int(i/3))
            hSum += across + down
    return hSum

def print_succ(state):
    """
    INPUT: 
        A state (list of length 9)

    WHAT IT DOES:
        Prints the list of all the valid successors in the puzzle. 
    """

    # given state, check state format and get goal_state.
    goal_state = state_check(state)


    succ_states = get_succ(state)
    for succ_state in succ_states:
        print(succ_state, "h={}".format(H(succ_state)))


def get_succ(state):
    """
    INPUT: 
        A state (list of length 9)

    RETURNS:
        A list of all the valid successors in the puzzle (don't forget to sort the result as done below). 
    """
    temp = state.copy()
    zeros = []
    repeat = True
    offset = 0
    try:
        while(repeat):
            zeros.append(temp.index(0) + offset)
            temp.pop(temp.index(0))
            offset += 1
    except ValueError:
        repeat = False
    lists = []
    for zero in zeros:
        addSwaps(state, lists, zero)
    lists.sort()
    return lists


def solve(state):
    """
    INPUT: 
        An initial state (list of length 9)

    WHAT IT SHOULD DO:
        Prints a path of configurations from initial state to goal state along  h values, number of moves, and max queue number in the format specified in the pdf.
    """

    # given state, check state format and get goal_state.
    goal_state = list(state_check(state))


    pq = []
    frontier = []
    saved = []
    heapq.heappush(pq,(H(state), state, (0, H(state), None)))
    found = None
    maxQueue = 0
    while(len(pq) != 0):
        if(len(pq) > maxQueue):
            maxQueue = len(pq)
        current = heapq.heappop(pq)
        if(current[1] == goal_state):
            found = current
            break
        if(maxQueue >= 10000):
            break
        if(saved.count(current[1]) != 0):
            continue
        frontier.append(current)
        saved.append(current[1])

        options = get_succ(current[1])
        for i in options:
            h = H(i)
            g = current[2][0] + 1
            pred = len(frontier) - 1
            heapq.heappush(pq, (h+g, i, (g, h, pred)))
    if(found == None):
        print(False)
    else:
        print(True)
        toPrint = []
        while(found != None):
            toPrint.append((found[1], found[2][1], found[2][0]))
            if(found[2][2] != None):
                found = frontier[found[2][2]]
            else:
                found = None
        toPrint.reverse()
        for state_info in toPrint:
            current_state = state_info[0]
            h = state_info[1]
            move = state_info[2]
            print(current_state, "h={}".format(h), "moves: {}".format(move))

def addSwaps(state, lists, zero):
    """
    INPUT: 
        A state (list of length 9)
        A list that contains states
        A list that keeps track of the zeros

    WHAT IT DOES:
        Adds all possible successors to lists
    """
    if(zero + 1 < 9):
        if(state[zero+1] != 0 and zero%3 != 2):
            tempState = state.copy()
            tempState[zero] = tempState[(zero+1)]
            tempState[zero+1] = 0 
            lists.append(tempState)
        if(zero + 3 < 9):
            if(state[zero+3] != 0):
                tempState = state.copy()
                tempState[zero] = tempState[zero+3]
                tempState[zero+3] = 0 
                lists.append(tempState)
    
    if(zero - 1 > -1):
        if(state[zero-1] != 0 and zero%3 != 0):
            tempState = state.copy()
            tempState[zero] = tempState[zero-1]
            tempState[zero-1] = 0 
            lists.append(tempState)
        if(zero - 3 > -1):
            if(state[zero-3] != 0):
                tempState = state.copy()
                tempState[zero] = tempState[zero-3]
                tempState[zero-3] = 0 
                lists.append(tempState)

