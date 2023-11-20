from math import dist
from queue import SimpleQueue


class Dijkstra:
    """
    Simple take on Dijkstra's algorithm. Takes a graph object that requires the following data members:
    self.start = Starting cell : tuple,
    self.end = Ending cell : tuple,
    self.width = Width of graph : int,
    self.height = Height of graph : int,
    self.blocked_points = Unusable cells : set(tuple)
    """
    def __init__(self, graph):
        self.__graph = graph
        self.__path_dict = {}

    def __find_neighbors(self, point, neighbors):
        """
        Method for adding adjacent cells to queue. Modifies adjacent_points directly.
        :param point: tuple (x, y)
        :param neighbors: Simple Queue
        :return: None
        """
        for x in range(-1, 2):
            for y in range(-1, 2):
                next_point = ((point[0] + x), (point[1] + y))
                if (self.__graph.width > point[0] + x >= 0 and self.__graph.height > point[1] + y >= 0 and
                        next_point not in self.__path_dict):
                    if dist(next_point, point) > 1:
                        if not self.__check_corner_move(point, next_point):
                            return
                    neighbors.put([next_point, point, dist(next_point, point)])

    def __check_corner_move(self, point, next_point):
        """
        Helper method for find_adjacent to verify if a diagonal movement is legal.
        :param point: tuple (x, y) origination point
        :param next_point: tuple (x, y) destination point
        :return: True if legal move, False otherwise
        """
        x1, y1 = point
        x2, y2 = next_point
        if (x1, y2) in self.__graph.blocked_points and (x2, y1) in self.__graph.blocked_points:
            return False
        return True

    def __generate_path_dictionary(self):
        """
        Main logic for determining shortest path. Implements a version of Dijkstra's Algorithm
        in order to determine the distance to all other cells in the __graph. Builds a dictionary
        self.__path_dict that records every cell, the distance to that cell, and the cell travelled through
        to reach it. When the dictionary is complete, algorithm can take any destination cell and trace back
        through the dictionary to the starting cell to find the shortest route.
        :return: None
        """
        self.__path_dict.clear()
        neighbors = SimpleQueue()

        # Fill in blocked spaces
        for point in self.__graph.blocked_points:
            self.__path_dict[point] = None

        # Starting cell sets "previous cell" to itself with a distance of 0
        self.__path_dict[self.__graph.start] = [self.__graph.start, 0.0]
        self.__find_neighbors(self.__graph.start, neighbors)

        # Continue pulling from SimpleQueue until it is empty
        while not neighbors.empty():
            point, prev_point, distance = neighbors.get()
            prev_point_distance = self.__path_dict[prev_point][1]
            if point not in self.__path_dict.keys():
                # p_dict[point] = [point coming from, distance from start]
                self.__path_dict[point] = [prev_point, distance + prev_point_distance]
                self.__find_neighbors(point, neighbors)
            else:
                known_distance = self.__path_dict[point][1]
                # Check if new distance to point is less than already known distance. If so, update.
                if distance + prev_point_distance < known_distance:
                    self.__path_dict[point] = [prev_point, distance + prev_point_distance]
                    self.__find_neighbors(point, neighbors)

    def __find_path(self, end_point, path=None, distance=0):
        """
        Uses the path dictionary generated in self.generate_path_dictionary() to trace cells back
        to the starting cell, building the sequence of cells in the process.
        :param end_point: tuple (x, y) destination cell
        :param path: list of tuples [(x, y)] sequence of cells
        :param distance: distance to end point from start point
        :return: (Distance: int, Path: set) or (None, None)
        """
        if end_point not in self.__path_dict.keys():
            return None, None

        if path is None:
            path = []
            distance = self.__path_dict[end_point][1]

        # __path_dict[point] = [connected from point, distance from connected point]
        prev_point = self.__path_dict[end_point][0]
        weight = self.__path_dict[end_point][1]

        path.append(end_point)
        if weight == 0:
            return distance, set(path[::-1])  # Because path fills in reverse, we reorient it here

        return self.__find_path(prev_point, path, distance)

    def calculate(self):
        """
        Calculates the Dijkstra algorithm and returns the path.
        :return: (Distance: int, Path: set) or (None, None)
        """
        self.__generate_path_dictionary()
        return self.__find_path(self.__graph.end)
