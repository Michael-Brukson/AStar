class Cell:
    def __init__(self):
        self.parent_i: int = 0  # Parent cell's row index
        self.parent_j: int = 0  # Parent cell's column index
        self.f: float = float('inf')  # Total cost of the cell (g + h)
        self.g: float = float('inf')  # Cost from start to this cell
        self.h: int = 0  # Heuristic cost from this cell to destination
