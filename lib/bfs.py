from math import dist
from queue import SimpleQueue


class BFS:
    """
    Simple take on BFS algorithm.
    :param width: int - Width of grid
    :param height: int - Height of grid
    """
    def __init__(self, width, height):
        self.__came_from = {}  # __came_from[point] = [point coming from, distance from start]
        self.__neighbors = SimpleQueue()
        self.width = width
        self.height = height
        self.count = 0
        self.checking_cell = None
        self.queued_cells = []

    def tick(self, tick_rate, start, blocked_points):
        """
        Calculates the shortest route to every cell in a grid from a starting location.
        Runs algorithm in chunks moderated by tick rate.
        :param tick_rate: int || number of calculations per frame
        :param start: tuple || starting cell
        :param blocked_points: list(tuples) || list of cells that are walls
        :return:
        """
        if len(self.__came_from) == 0:
            # Reset data
            self.__neighbors = SimpleQueue()
            self.queued_cells.clear()

            # Fill in blocked spaces
            for point in blocked_points:
                self.__came_from[point] = None

            # Starting cell sets "previous cell" to itself with a distance of 0
            self.__came_from[start] = [start, 0.0]
            self.__find_neighbors(start, blocked_points)

        while tick_rate > 0:
            self.count = max(self.count, self.__neighbors.qsize())
            # print(self.count)
            tick_rate -= 1

            if not self.__neighbors.empty():
                cell, prev_cell, distance = self.__neighbors.get()
                self.checking_cell = cell
                self.queued_cells.remove(cell)
                prev_cell_distance = self.__came_from[prev_cell][1]  # distance connected cell is from start
                if cell not in self.__came_from.keys():
                    self.__came_from[cell] = [prev_cell, distance + prev_cell_distance]  # running total of distance
                    self.__find_neighbors(cell, blocked_points)
                else:
                    known_distance = self.__came_from[cell][1]

                    # Check if new distance to point is less than already known distance. If so, update.
                    if distance + prev_cell_distance < known_distance:
                        self.__came_from[cell] = [prev_cell, distance + prev_cell_distance]
                        self.__find_neighbors(cell, blocked_points)

    def __find_neighbors(self, point, blocked_points):
        """
        Method for adding adjacent cells to queue. Modifies adjacent_points directly.
        :param point: tuple || (x, y)
        :param blocked_points: list(tuples) || list of cells that are walls
        :return: None
        """
        for x in range(-1, 2):
            for y in range(-1, 2):
                next_point = ((point[0] + x), (point[1] + y))
                if (self.width > point[0] + x >= 0 and self.height > point[1] + y >= 0 and
                        next_point not in self.__came_from and next_point != point):
                    if dist(next_point, point) > 1:
                        if not self.__check_corner_move(point, next_point, blocked_points):
                            return
                    self.__neighbors.put([next_point, point, dist(next_point, point)])
                    self.queued_cells.append(next_point)

    def __check_corner_move(self, point, next_point, blocked_points):
        """
        Helper method for find_adjacent to verify if a diagonal movement is legal.
        :param point: tuple || (x, y) origination point
        :param next_point: tuple || (x, y) destination point
        :param blocked_points: list(tuples) || list of cells that are walls
        :return: True if legal move, False otherwise
        """
        x1, y1 = point
        x2, y2 = next_point
        if (x1, y2) in blocked_points and (x2, y1) in blocked_points:
            return False
        return True

    def public_find_path(self, end):
        """
        Public access to generating a path from starting cell to ending cell.
        :param end: tuple || (x, y) ending cell: tuple
        :return: (Distance: int, Path: set) or (None, None)
        """
        if len(self.__came_from) > 0 and self.__neighbors.empty():
            self.checking_cell = None
            return self.__find_path(end)

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
        Clears self.__came_from dictionary.
        :return:
        """
        self.__came_from.clear()
