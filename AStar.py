import heapq
from Cell import Cell
from typing import Literal

class AStar:
    def __init__(self, width: int, height:int):
        self.ROW: int = width
        self.COL: int = height

    # Check if a cell is valid (within the grid)
    def _is_valid(self, row: int, col: int) -> bool:
        return (row >= 0) and (row < self.ROW) and (col >= 0) and (col < self.COL)

    # Check if a cell is unblocked
    def _is_unblocked(self, grid: list, row: int, col: int) -> bool:
        return grid[row][col] == 1

    # Check if a cell is the destination
    def _is_destination(self, row: int, col: int, dest: tuple) -> bool:
        return row == dest[0] and col == dest[1]

    # TODO: check if it's faster to remove the root operation entirely when root is 1
    def __euclidean_dist(self, row: int, col: int, dest: tuple, root: float = 0.5) -> float:
        x_dist: int = row - dest[0]
        y_dist: int = col - dest[1]
        return ((x_dist) ** 2 + (y_dist) ** 2) ** root

    def __manhattan_dist(self, row: int, col: int, dest: tuple) -> float:
        x_dist: int = abs(row - dest[0])
        y_dist: int = abs(col - dest[1])
        return x_dist + y_dist
    
    def __chebyschev_dist(self, row: int, col: int, dest: tuple) -> float:
        return max(abs(a - b) for a, b in zip([row, col], dest))

    def __move_cost(self, delta_row: int, delta_col: int) -> float:
        if delta_row != 0 and delta_col != 0:
            return 2 ** 0.5
        return 1.0

    # Calculate the heuristic value of a cell (Euclidean distance to destination)
    def _h_value(self, row: int, col: int, dest: tuple, method: Literal["euclidean", "manhattan", "chebyshev"] = "euclidean", weight: float = 1.0) -> float:
        if method == "euclidean":
            return weight * self.__euclidean_dist(row, col, dest)
        elif method == "manhattan":
            return weight * self.__manhattan_dist(row, col, dest)
        else:
            return weight * self.__chebyschev_dist(row, col, dest)

    # Trace the path from source to destination
    def _trace_path(self, cell_details: list, dest: tuple) -> list:
        path = []
        row, col = dest[0], dest[1]

        # Trace the path from destination to source using parent cells
        while not (cell_details[row][col].parent_i == row and cell_details[row][col].parent_j == col): # while the parent is not the destination
            path.append((row, col))
            temp_row = cell_details[row][col].parent_i
            temp_col = cell_details[row][col].parent_j
            row = temp_row
            col = temp_col

        # Add the source cell to the path
        path.append((row, col))
        # Reverse the path to get the path from source to destination
        path.reverse()

        return path

    # Implement the A* search algorithm
    def search(self, grid: list, src: tuple, dest: tuple, h_method: Literal["euclidean", "manhattan", "chebyshev"] = "euclidean", weight: float = 1.0) -> list:
        # Check if the source and destination are valid
        if not self._is_valid(src[0], src[1]) or not self._is_valid(dest[0], dest[1]):
            # print("Source or destination is out of reach")
            return []

        # Check if the source and destination are unblocked
        if not self._is_unblocked(grid, src[0], src[1]) or not self._is_unblocked(grid, dest[0], dest[1]):
            # print("Source or the destination is unreachable")
            return []

        # Check if we are already at the destination
        if self._is_destination(src[0], src[1], dest):
            # print("We are already at the destination")
            return []

        # Initialize the closed list (visited cells)
        closed_list = [[False for _ in range(self.COL)] for _ in range(self.ROW)]
        # Initialize the details of each cell
        cell_details = [[Cell() for _ in range(self.COL)] for _ in range(self.ROW)]

        # Initialize the start cell details
        i = src[0]
        j = src[1]
        cell_details[i][j].f = 0
        cell_details[i][j].g = 0
        cell_details[i][j].h = 0
        cell_details[i][j].parent_i = i
        cell_details[i][j].parent_j = j

        # Initialize the open list (cells to b e visited) with the start cell
        open_list = []
        heapq.heappush(open_list, (0.0, i, j))

        # Initialize the flag for whether destination is found
        found_dest = False

        # Main loop of A* search algorithm
        while len(open_list) > 0:
            # Pop the cell with the smallest f value from the open list
            p = heapq.heappop(open_list)

            # Mark the cell as visited
            i = p[1]
            j = p[2]
            if closed_list[i][j]:
                continue
            closed_list[i][j] = True

            # The first time the destination is popped, shortest path has been found.
            if self._is_destination(i, j, dest):
                return self._trace_path(cell_details, dest)

            # For each direction, check the successors
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
            for dir in directions:
                new_i = i + dir[0]
                new_j = j + dir[1]

                # If the successor is valid, unblocked, and not visited
                if self._is_valid(new_i, new_j) and self._is_unblocked(grid, new_i, new_j) and not closed_list[new_i][new_j]:
                    # Calculate the new f, g, and h values
                    g_new = cell_details[i][j].g + self.__move_cost(dir[0], dir[1])
                    h_new = self._h_value(new_i, new_j, dest, h_method, weight)
                    f_new = g_new + h_new

                    # If the cell is not in the open list or the new f value is smaller
                    if cell_details[new_i][new_j].f == float('inf') or cell_details[new_i][new_j].f > f_new:
                        # Add the cell to the open list
                        heapq.heappush(open_list, (f_new, new_i, new_j))
                        # Update the cell details
                        cell_details[new_i][new_j].f = f_new
                        cell_details[new_i][new_j].g = g_new
                        cell_details[new_i][new_j].h = h_new
                        cell_details[new_i][new_j].parent_i = i
                        cell_details[new_i][new_j].parent_j = j

        # If the destination is not found after visiting all cells
        if not found_dest:
            print("Failed to find the destination cell")

        return []
