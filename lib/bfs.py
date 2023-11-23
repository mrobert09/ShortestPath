from math import dist
from queue import SimpleQueue


class BFS:
    """
    Simple take on BFS algorithm. Takes a graph object that requires the following data members:
    self.start = Starting cell : tuple,
    self.end = Ending cell : tuple,
    self.width = Width of graph : int,
    self.height = Height of graph : int,
    self.blocked_points = Unusable cells : set(tuple)
    """
    def __init__(self, graph):
        self.__came_from = {}  # __came_from[point] = [point coming from, distance from start]
        self.__neighbors = SimpleQueue()
        self.count = 0

        self.__graph = graph  # goal to remove the need for this

    def tick(self, tick_rate):
        """
        Calculates the BFS algorithm and returns the path.
        :return: (Distance: int, Path: set) or (None, None)
        """
        if len(self.__came_from) == 0:
            # Reset data
            self.__neighbors = SimpleQueue()
            self.__graph.queued_points.clear()

            # Fill in blocked spaces
            for point in self.__graph.blocked_points:
                self.__came_from[point] = None

            # Starting cell sets "previous cell" to itself with a distance of 0
            self.__came_from[self.__graph.start] = [self.__graph.start, 0.0]
            self.__find_neighbors(self.__graph.start)

        while tick_rate > 0:
            self.count = max(self.count, self.__neighbors.qsize())
            # print(self.count)
            tick_rate -= 1

            if not self.__neighbors.empty():
                cell, prev_cell, distance = self.__neighbors.get()
                self.__graph.checking_cell = cell
                self.__graph.queued_points.remove(cell)
                prev_cell_distance = self.__came_from[prev_cell][1]  # distance connected cell is from start
                if cell not in self.__came_from.keys():
                    self.__came_from[cell] = [prev_cell, distance + prev_cell_distance]  # running total of distance
                    self.__find_neighbors(cell)
                else:
                    known_distance = self.__came_from[cell][1]

                    # Check if new distance to point is less than already known distance. If so, update.
                    if distance + prev_cell_distance < known_distance:
                        self.__came_from[cell] = [prev_cell, distance + prev_cell_distance]
                        self.__find_neighbors(cell)

    def __find_neighbors(self, point):
        """
        Method for adding adjacent cells to queue. Modifies adjacent_points directly.
        :param point: tuple (x, y)
        :return: None
        """
        for x in range(-1, 2):
            for y in range(-1, 2):
                next_point = ((point[0] + x), (point[1] + y))
                if (self.__graph.width > point[0] + x >= 0 and self.__graph.height > point[1] + y >= 0 and
                        next_point not in self.__came_from and next_point != point):
                    if dist(next_point, point) > 1:
                        if not self.__check_corner_move(point, next_point):
                            return
                    self.__neighbors.put([next_point, point, dist(next_point, point)])
                    self.__graph.queued_points.append(next_point)

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

    def public_find_path(self):
        if len(self.__came_from) > 0 and self.__neighbors.empty():
            self.__graph.checking_cell = None
            return self.__find_path(self.__graph.end)

    def __find_path(self, end_point, path=None, distance=0):
        """
        Uses the path dictionary generated in self.generate_path_dictionary() to trace cells back
        to the starting cell, building the sequence of cells in the process.
        :param end_point: tuple (x, y) destination cell
        :param path: list of tuples [(x, y)] sequence of cells
        :param distance: distance to end point from start point
        :return: (Distance: int, Path: set) or (None, None)
        """
        if end_point not in self.__came_from.keys():
            return None, None

        if path is None:
            path = []
            distance = self.__came_from[end_point][1]

        # __came_from[point] = [connected from point, distance from connected point]
        prev_point = self.__came_from[end_point][0]
        weight = self.__came_from[end_point][1]

        path.append(end_point)
        if weight == 0:
            return distance, set(path[::-1])  # Because path fills in reverse, we reorient it here

        return self.__find_path(prev_point, path, distance)

    def clear_came_from_dict(self):
        """
        :return:
        """
        self.__came_from.clear()
