import math
import numpy as np

START = (0,0)
FINISH = (9, 9)
NEIGHBOURS = ((0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, 1), (1, -1), (-1,-1))

class NoOpenNodes(Exception):
    pass

class Node:
    """
    f = histuric value sum of g and h
    g = distance from start
    h = estimated distance from end
    """
    def __init__(self, row, col, parent = None):
        self.row = row
        self.col = col
        self.f = 0
        self.g = 0
        self.h = 0
        self.parent = parent

    def get_heuristic(self):
        """
        calculate the f, g and h values
        """
        self.h = math.sqrt(((self.row - FINISH[0])**2) + ((self.col - FINISH[1])**2))
        try:
            step = math.sqrt(2) if self.parent.row != self.row and self.parent.col != self.col else 1.0
        except AttributeError:
            self.g = 0
        else:
            self.g = step + self.parent.g
        self.f = self.g + self.h

class Node_container:
    """
    container object that holds the open and closed nodes
    also holds all the functions and actions that will be applied to the function
    """
    def __init__(self):
        """
        initialize the open and close lists
        """
        self.open = []
        self.close = []

    def add_to_open(self, node):
        """
        add the passed node to the open list
        """
        self.open.append(node)

    def lowest_f_val(self):
        """
        return the lowest f value cell
        """
        try:
            lowest = self.open[0]
        except IndexError:
            raise NoOpenNodes
        else:
            for val in self.open:
                if val.f < lowest.f:
                    lowest = val
                if val.f == lowest:
                    if val.g < lowest.g:
                        lowest = val
            return lowest

    def remove_from_open(self, node):
        """
        remove the passed node from the open list
        """
        self.open.pop(self.open.index(node))

    def add_to_close(self, node):
        """
        add the passed node to the closed list
        """
        self.close.append(node)

    def return_final_path(self, node):
        """
        return a list containing the path from the final node to the start cell
        """
        path = []
        current = node
        while current.parent != None:
            path.append([current.row, current.col])
            current = current.parent
        path.append([START[0],START[0]])
        return path

    def traverse_neighbours(self, current, MAZE):
        """
        this fuction takes a node looks at all it's neighbours and then based on this adds them to the open list
        the current node that we are looking at :param current:
        this is the full maze that we need to pass in to check for walls ect.:param MAZE:
        does not return anything but does add and remove stuff from the open and closed lists:return:
        """
        for n in NEIGHBOURS:
            # define the neighbour row and col
            test_row = current.row + n[0]
            test_col = current.col + n[1]

            #create the neighbour node
            nbr = Node(test_row, test_col, current)
            nbr.get_heuristic()
            #check to see that the neighbour cell is in range
            if nbr.row < 0 or nbr.row > 9:
                continue
            if nbr.col < 0 or nbr.col > 9:
                continue

            # check to see that the neighbour cell isn't a wall in the maze
            if MAZE[nbr.row][nbr.col] == 1:
                continue

            # check to see that the neighbour is not not in the closed list
            if self.check_closed(nbr.row, nbr.col):
                continue

            #check that the neighbour is in the open list if it is not append it to the open list and go onto the next neighbour
            if not self.check_open(nbr.row, nbr.col):
                self.add_to_open(nbr)
                continue

            # finally any remaining neighbours are already in open and so we check if the new path is shorter, it is is we want to replace the node
            # in the open list with the new neighbour
            self.check_path_shorter(nbr)


    def check_closed(self, test_row, test_col):
        """
        check to see if there is a cell at the row and column, returns true false
        """
        closed = False
        for c in self.close:
            if c.row == test_row and c.col == test_col:
                closed = True
                break
        return closed

    def check_open(self, test_row, test_col):
        """
        row of the cell to test :param test_row:
        column of the cell to test :param test_col:
        return True or false :return:
        """
        open = False
        for o in self.open:
            if o.row == test_row and o.col == test_col:
                open = True
                break
        return open

    def check_path_shorter(self, nbr):
        """
        check the neighbour to see if it is a shorter path :param nbr:
        """
        for o in self.open:
            if o.row == nbr.row and o.col == nbr.col:
                if nbr.g < o.g:
                    self.remove_from_open(o)
                    self.add_to_close(o)
                    self.add_to_open(nbr)

    def create_hesturic_matricies(self):
        """
        :return: matrices that have the g, h and f values
        """
        G = [[0 for i in range(10)] for j in range(10)]
        F = [[0 for i in range(10)] for j in range(10)]
        H = [[0 for i in range(10)] for j in range(10)]
        for o in self.open:
            row = o.row
            col = o.col
            G[row][col] = round(o.g, 1)
            F[row][col] = round(o.f, 1)
            H[row][col] = round(o.h, 1)

        for c in self.close:
            row = c.row
            col = c.col
            G[row][col] = round(c.g, 1)
            F[row][col] = round(c.f, 1)
            H[row][col] = round(c.h, 1)
        return F, G, H

    def closed_nodes(self):
        """
        :return: closed nodes matrix
        """
        C = [[0 for i in range(10)] for j in range(10)]
        for c in self.close:
            row = c.row
            col = c.col
            C[row][col] = 1
        return C

    def open_nodes(self):
        """
        :return: matrix of all the open nodes
        """
        O = [[0 for i in range(10)] for j in range(10)]
        for o in self.open:
            row = o.row
            col = o.col
            O[row][col] = 1
        return O


def run_astar(MAZE, START, FINISH):
    """
    :param MAZE: the 10 x 10 grid that will be output
    :param START: The starting cell
    :param FINISH: the finishing cell
    :return: yield the final path, closed, open, f, g and h matrices that will be output
    """
    # define an empty list to hold the final path from START to FINISH
    PATH = []

    # start the first cell at the start cell
    cell = Node(START[0], START[1])
    cell.get_heuristic()

    # add the first cell to the open list
    container = Node_container()
    container.add_to_open(cell)

    running = True
    fail_safe = 0
    while running:
        # get the current lowest f value
        current = container.lowest_f_val()
        # remove the lowest f value item from the current
        container.remove_from_open(current)
        # add the lowest f value item to the closed list
        container.add_to_close(current)

        if current.row == FINISH[0] and current.col == FINISH[1]:
            PATH = container.return_final_path(current)
            running = False

        container.traverse_neighbours(current, MAZE)
        F, G, H = container.create_hesturic_matricies()
        O = container.open_nodes()
        C = container.closed_nodes()
        if fail_safe >= (len(MAZE) * len(MAZE[0]) * 4):
            running = False
            print("NO PATH FOUND")

        yield PATH, C, O, F, G, H