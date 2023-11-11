from queue import SimpleQueue
from math import dist


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
        match cell_type:
            case "start":
                self.start = cell
                # self.blocked_points.discard(cell)
            case "end":
                self.end = cell
                # self.blocked_points.discard(cell)
            case "add":
                if cell != self.start and cell != self.end:
                    self.blocked_points.add(cell)
            case "remove":
                self.blocked_points.discard(cell)
            case _:
                return

    def find_adjacent(self, point, path_dict, adjacent_points, max_x, max_y):
        for x in range(-1, 2):
            for y in range(-1, 2):
                next_point = ((point[0] + x), (point[1] + y))
                if (max_x > point[0] + x >= 0 and max_y > point[1] + y >= 0 and
                        next_point not in path_dict):
                    if dist(next_point, point) > 1:
                        if not self.check_kitty_corners(point, next_point):
                            return
                    adjacent_points.put([next_point, point, dist(next_point, point)])


    def check_kitty_corners(self, point, next_point):
        x1, y1 = point
        x2, y2 = next_point
        if (x1, y2) in self.blocked_points and (x2, y1) in self.blocked_points:
            return False
        return True



    def generate_path_dictionary(self):
        p_dict = {}
        adjacent_points = SimpleQueue()

        # Fill in blocked spaces
        for point in self.blocked_points:
            p_dict[point] = None

        p_dict[self.start] = [self.start, 0.0]
        self.find_adjacent(self.start, p_dict, adjacent_points, self.width, self.height)

        while not adjacent_points.empty():
            point, prev_point, distance = adjacent_points.get()
            prev_point_distance = p_dict[prev_point][1]
            if point not in p_dict.keys():
                # p_dict[point] = [point coming from, total distance from start]
                p_dict[point] = [prev_point, distance + prev_point_distance]
                self.find_adjacent(point, p_dict, adjacent_points, self.width, self.height)
            else:
                known_distance = p_dict[point][1]
                # Check if new distance to point is less than already known distance. If so, update.
                if distance + prev_point_distance < known_distance:
                    p_dict[point] = [prev_point, distance + prev_point_distance]
                    self.find_adjacent(point, p_dict, adjacent_points, self.width, self.height)

        self.path_dict = p_dict


    def print_info(self):
        print("\nStart:", self.start)
        print("End:", self.end)
        print("Blocked:", self.blocked_points)
        print("Path:", type(self.path), self.path)
        print("Dict: ")
        print(self.path_dict)


    def find_distance(self, end_point, path=None, total=0):
        if path == None:
            path = []

        # path_dict[point] = [connected from point, distance from connected point]
        if end_point not in self.path_dict.keys():
            self.path.clear()
            return
        prev_point = self.path_dict[end_point][0]
        weight = self.path_dict[end_point][1]

        path.append(end_point)
        if weight == 0:
            self.path = set(path[::-1])
            return (total, path[::-1])  # Because path fills in reverse, we reorient it here
        total += weight

        return self.find_distance(prev_point, path, total)


    def calculate_path(self):
        self.generate_path_dictionary()
        self.find_distance(self.end)


    def __repr__(self):
        output = self.find_distance(self.end)
        if output:
            distance, path = output
            s = "Distance: " + str(distance) + "\n" + "Path: " + str(self.path)
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
