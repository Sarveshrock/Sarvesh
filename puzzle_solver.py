from copy import deepcopy
from colorama import Fore, Back, Style
import heapq

# Direction matrix
DIRECTIONS = {"U": [-1, 0], "D": [1, 0], "L": [0, -1], "R": [0, 1]}
# Target matrix
END = [[1, 2, 3], [4, 5, 0]]

# Unicode for drawing puzzle in the command prompt or terminal
left_down_angle = '\u2514'
right_down_angle = '\u2518'
right_up_angle = '\u2510'
left_up_angle = '\u250C'

middle_junction = '\u253C'
top_junction = '\u252C'
bottom_junction = '\u2534'
right_junction = '\u2524'
left_junction = '\u251C'

# Bar color
bar = Style.BRIGHT + Fore.CYAN + '\u2502' + Fore.RESET + Style.RESET_ALL
dash = '\u2500'

# Line draw code
first_line = Style.BRIGHT + Fore.CYAN + left_up_angle + dash + dash + top_junction + dash + dash + right_up_angle + Fore.RESET + Style.RESET_ALL
middle_line = Style.BRIGHT + Fore.CYAN + left_junction + dash + dash + middle_junction + dash + dash + right_junction + Fore.RESET + Style.RESET_ALL
last_line = Style.BRIGHT + Fore.CYAN + left_down_angle + dash + dash + bottom_junction + dash + dash + right_down_angle + Fore.RESET + Style.RESET_ALL

# Puzzle print function
def print_puzzle(array):
    print(first_line)
    for a in range(len(array)):
        for i in array[a]:
            if i == 0:
                print(bar, Back.RED + ' ' + Back.RESET, end=' ')
            else:
                print(bar, i, end=' ')
        print(bar)
        if a == 0:
            print(middle_line)
    print(last_line)

# Node class to store each state of the puzzle
class Node:
    def __init__(self, current_node, previous_node, g, h, dir):
        self.current_node = current_node
        self.previous_node = previous_node
        self.g = g
        self.h = h
        self.dir = dir

    def f(self):
        return self.g + self.h

def get_pos(current_state, element):
    for row in range(len(current_state)):
        if element in current_state[row]:
            return (row, current_state[row].index(element))
    raise ValueError(f"Element {element} not found in the current state")

# Distance calculation algorithm (Manhattan distance)
def manhattan_cost(current_state):
    cost = 0
    for row in range(len(current_state)):
        for col in range(len(current_state[0])):
            pos = get_pos(END, current_state[row][col])
            cost += abs(row - pos[0]) + abs(col - pos[1])
    return cost

# Get adjacent nodes
def get_adj_nodes(node):
    list_node = []
    empty_pos = get_pos(node.current_node, 0)

    for dir in DIRECTIONS.keys():
        new_pos = (empty_pos[0] + DIRECTIONS[dir][0], empty_pos[1] + DIRECTIONS[dir][1])
        if 0 <= new_pos[0] < len(node.current_node) and 0 <= new_pos[1] < len(node.current_node[0]):
            new_state = deepcopy(node.current_node)
            new_state[empty_pos[0]][empty_pos[1]] = node.current_node[new_pos[0]][new_pos[1]]
            new_state[new_pos[0]][new_pos[1]] = 0
            list_node.append(Node(new_state, node.current_node, node.g + 1, manhattan_cost(new_state), dir))

    return list_node

# Get the best node available among nodes
def get_best_node(open_set):
    return heapq.heappop(open_set)

# Build the smallest path
def build_path(closed_set):
    node = closed_set[str(END)]
    branch = []

    while node.dir:
        branch.append({
            'dir': node.dir,
            'node': node.current_node
        })
        node = closed_set[str(node.previous_node)]
    branch.append({
        'dir': '',
        'node': node.current_node
    })
    branch.reverse()

    return branch

# Main function to solve the puzzle
def main(puzzle):
    open_set = [(0, str(puzzle), Node(puzzle, puzzle, 0, manhattan_cost(puzzle), ""))]
    closed_set = {}

    while open_set:
        _, _, test_node = get_best_node(open_set)
        closed_set[str(test_node.current_node)] = test_node

        if test_node.current_node == END:
            return build_path(closed_set)

        adj_nodes = get_adj_nodes(test_node)
        for node in adj_nodes:
            node_key = str(node.current_node)
            if node_key in closed_set or any(n[2].current_node == node.current_node for n in open_set):
                continue
            heapq.heappush(open_set, (node.f(), node_key, node))

    raise ValueError("No solution found.")


if __name__ == '__main__':
    # Start matrix for a 2x3 puzzle
    br = main([[3, 2, 5],
               [4, 0, 1]])

    print('Total steps:', len(br) - 1)
    print()
    print(dash + dash + right_junction, "INPUT", left_junction + dash + dash)
    for b in br:
        if b['dir'] != '':
            letter = ''
            if b['dir'] == 'U':
                letter = 'UP'
            elif b['dir'] == 'R':
                letter = "RIGHT"
            elif b['dir'] == 'L':
                letter = 'LEFT'
            elif b['dir'] == 'D':
                letter = 'DOWN'
            print(dash + dash + right_junction, letter, left_junction + dash + dash)
        print_puzzle(b['node'])
        print()

    print(dash + dash + right_junction, 'ABOVE IS THE OUTPUT', left_junction + dash + dash)
