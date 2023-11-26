from lib.bfs import BFS
import time


class ShortestPath:

    def __init__(self, start, end, width, height):
        self.start = start
        self.end = end
        self.width = width
        self.height = height
        self.blocked_points = set()
        self.distance = None
        self.path = set()
        self.bfs = BFS(width, height)

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

    # def calculate_path(self):
    #     """
    #     Simple container for calling path functions.
    #     :return: None
    #     """
    #     times = 0
    #     for x in range(100):
    #         start_time = time.perf_counter()
    #         self.distance, self.path = self.bfs.calculate()
    #         end_time = time.perf_counter()
    #         times += (end_time - start_time)
    #     print("Calculation time:", times/100)

    def calculate_path_with_ticks(self, tick_rate):
        # start_time = time.perf_counter()
        self.bfs.tick(tick_rate, self.start, self.end, self.blocked_points)
        self.distance, self.path = self.bfs.public_find_path(self.end) or (None, None)
        # end_time = time.perf_counter()
        # print("Calculation time:", end_time - start_time)

    def print_info(self):
        """
        Used mostly for debugging. Prints some useful info to the console.
        :return: None
        """
        print(self)

    def __repr__(self):
        """
        Override for printing the ShortestPath object. Prints basic info about the object.
        :return: string
        """
        if self.path:
            s = "Start: " + str(self.start) + "\nEnd: " + str(self.end) + \
                "\nDistance: " + str(self.distance) + "\nPath: " + str(self.path) + \
                "\nBlocked Cells: " + str(self.blocked_points)
            return s
        else:
            return "No valid path to end."


def main():

    max_grid_x = 50
    max_grid_y = 50
    starting_point = (0, 0)
    ending_point = (2, 2)

    times = 0
    for x in range(10):
        sp = ShortestPath(starting_point, ending_point, max_grid_x, max_grid_y)

        start_time = time.perf_counter()
        sp.calculate_path_with_ticks(1000)
        end_time = time.perf_counter()
        times += (end_time - start_time)
        # print(sp.bfs.count)
    print("Calc:", times / 10)
    # print(sp)


if __name__ == '__main__':
    main()
