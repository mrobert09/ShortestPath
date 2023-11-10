from queue import SimpleQueue
from math import dist


class ShortestPath:

    def __init__(self, start, end, width, height):
        self.start = start
        self.end = end
        self.width = width
        self.height = height
        self.blocked_points = set()
        self.path_dict = self.generate_path_dictionary(self.start, self.width, self.height, self.blocked_points)


    def update_cell(self, cell_type, cell):
        match cell_type:
            case "start":
                self.start = cell
                self.blocked_points.discard(cell)
            case "end":
                self.end = cell
                self.blocked_points.discard(cell)
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
                    adjacent_points.put([next_point, point, dist(next_point, point)])


    def generate_path_dictionary(self, starting_point, max_x, max_y, blocked_points):
        path_dict = {}
        adjacent_points = SimpleQueue()

        # Fill in blocked spaces
        for point in blocked_points:
            path_dict[point] = None

        path_dict[starting_point] = [starting_point, 0.0]
        self.find_adjacent(starting_point, path_dict, adjacent_points, max_x, max_y)

        while not adjacent_points.empty():
            next_point = adjacent_points.get()
            if next_point[0] not in path_dict.keys():
                path_dict[next_point[0]] = [next_point[1], next_point[2]]
            self.find_adjacent(next_point[0], path_dict, adjacent_points, max_x, max_y)

        return path_dict


    def print_info(self):
        print("\nStart:", self.start)
        print("End:", self.end)
        print("Blocked:", self.blocked_points)


    def find_distance(self, start_point, end_point, path_dict, path=None, total=0):
        if path == None:
            path = []

        # path_dict[point] = [connected from point, distance from connected point]
        prev_point = path_dict[end_point][0]
        weight = path_dict[end_point][1]

        path.append(end_point)
        if weight == 0:
            return (total, path[::-1])  # Because path fills in reverse, we reorient it here
        total += weight

        return self.find_distance(start_point, prev_point, path_dict, path, total)


    def __repr__(self):
        distance, path = self.find_distance(self.start, self.end, self.path_dict)
        s = "Distance: " + str(distance) + "\n" + "Path: " + str(path)
        return s


def main():
    max_grid_x = 5
    max_grid_y = 5
    starting_point = (2, 0)
    ending_point = (0, 0)

    sp = ShortestPath(starting_point, ending_point, max_grid_x, max_grid_y)
    print(sp)


if __name__ == '__main__':
    main()
