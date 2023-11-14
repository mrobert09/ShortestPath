from queue import SimpleQueue
from math import dist
import time


class ShortestPath:

    def __init__(self, start, end, width, height):
        self.start = start
        self.end = end
        self.width = width
        self.height = height
        self.blocked_points = set()
        self.path_dict = {}
        self.path = set()
        self.calculate_path()

    def update_cell(self, cell_type, cell):
        """
        Method for changing cell type between empty, start, end, and wall
        :param cell_type: string ("start", "end", "add", "remove")
        :param cell: tuple (x, y)
        :return: None
        """
        match cell_type:
            case "start":
                self.start = cell
            case "end":
                self.end = cell
            case "add":
                if cell != self.start and cell != self.end:
                    self.blocked_points.add(cell)
            case "remove":
                self.blocked_points.discard(cell)
            case _:
                return

    def find_adjacent(self, point, adjacent_points):
        """
        Method for adding adjacent cells to queue. Modifies adjacent_points directly.
        :param point: tuple (x, y)
        :param adjacent_points: Simple Queue
        :return: None
        """
        for x in range(-1, 2):
            for y in range(-1, 2):
                next_point = ((point[0] + x), (point[1] + y))
                if (self.width > point[0] + x >= 0 and self.height > point[1] + y >= 0 and
                        next_point not in self.path_dict):
                    if dist(next_point, point) > 1:
                        if not self.check_kitty_corners(point, next_point):
                            return
                    adjacent_points.put([next_point, point, dist(next_point, point)])

    def check_kitty_corners(self, point, next_point):
        """
        Helper method for find_adjacent to verify if a diagonal movement is legal.
        :param point: tuple (x, y) originiation point
        :param next_point: tuple (x, y) destination point
        :return: True if legal move, False otherwise
        """
        x1, y1 = point
        x2, y2 = next_point
        if (x1, y2) in self.blocked_points and (x2, y1) in self.blocked_points:
            return False
        return True

    def generate_path_dictionary(self):
        """
        Main logic for determining shortest path. Implements a version of Dijkstra's Algorithm
        in order to determine the distance to all other cells in the graph. Builds a dictionary
        self.path_dict that records every cell, the distance to that cell, and the cell travelled through
        to reach it. When the dictionary is complete, algorithm can take any destination cell and trace back
        through the dictionary to the starting cell to find the shortest route.
        :return: None
        """
        self.path_dict.clear()
        adjacent_points = SimpleQueue()

        # Fill in blocked spaces
        for point in self.blocked_points:
            self.path_dict[point] = None

        # Starting cell sets "previous cell" to itself with a distance of 0
        self.path_dict[self.start] = [self.start, 0.0]
        self.find_adjacent(self.start, adjacent_points)

        # Continue pulling from SimpleQueue until it is empty
        while not adjacent_points.empty():
            point, prev_point, distance = adjacent_points.get()
            prev_point_distance = self.path_dict[prev_point][1]
            if point not in self.path_dict.keys():
                # p_dict[point] = [point coming from, distance distance from start]
                self.path_dict[point] = [prev_point, distance + prev_point_distance]
                self.find_adjacent(point, adjacent_points)
            else:
                known_distance = self.path_dict[point][1]
                # Check if new distance to point is less than already known distance. If so, update.
                if distance + prev_point_distance < known_distance:
                    self.path_dict[point] = [prev_point, distance + prev_point_distance]
                    self.find_adjacent(point, adjacent_points)


    def print_info(self):
        """
        Used mostly for debugging. Prints some useful info to the console.
        :return: None
        """
        print(self)

    def find_path(self, end_point, path=None, distance=0):
        """
        Uses the path dictionary generated in self.generate_path_dictionary() to trace cells back
        to the starting cell, building the sequence of cells in the process.
        :param end_point: tuple (x, y) destination cell
        :param path: list of tuples [(x, y)] sequence of cells
        :param distance: distance to end point from start point
        :return:
        """
        if end_point not in self.path_dict.keys():
            self.path.clear()
            return

        if path is None:
            path = []
            distance = self.path_dict[end_point][1]

        # path_dict[point] = [connected from point, distance from connected point]
        prev_point = self.path_dict[end_point][0]
        weight = self.path_dict[end_point][1]

        path.append(end_point)
        if weight == 0:
            self.path = set(path[::-1])
            return distance, path[::-1]  # Because path fills in reverse, we reorient it here

        return self.find_path(prev_point, path, distance)

    def calculate_path(self):
        """
        Simple container for calling path functions.
        :return: None
        """
        start_time = time.perf_counter()
        self.generate_path_dictionary()
        self.find_path(self.end)
        end_time = time.perf_counter()
        print("Calculation time:", end_time - start_time)

    def __repr__(self):
        """
        Override for printing the ShortestPath object. Prints basic info about the object.
        :return: string
        """
        output = self.find_path(self.end)
        if output:
            distance, path = output
            s = "Start: " + str(self.start) + "\nEnd: " + str(self.end) + \
                "\nDistance: " + str(distance) + "\nPath: " + str(self.path)
            return s
        else:
            return "No valid path to end."


def main():
    max_grid_x = 3
    max_grid_y = 3
    starting_point = (0, 0)
    ending_point = (2, 2)

    sp = ShortestPath(starting_point, ending_point, max_grid_x, max_grid_y)
    print(sp)


if __name__ == '__main__':
    main()
