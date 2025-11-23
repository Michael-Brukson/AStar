import numpy as np
from AStar import AStar
from utils import Plotting
from drawing import GridMake

def main():
    p: Plotting = Plotting()

    # Define the grid (1 for unblocked, 0 for blocked)
    grid: np.ndarray = np.array([
        [1, 0, 1, 1, 1, 1, 0, 1, 1, 1],
        [1, 1, 1, 0, 1, 1, 1, 0, 1, 1],
        [1, 1, 1, 0, 1, 1, 0, 1, 0, 1],
        [0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
        [1, 1, 1, 0, 1, 1, 1, 0, 1, 0],
        [1, 0, 1, 1, 1, 1, 0, 1, 0, 0],
        [1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 0, 1, 1, 1],
        [1, 1, 1, 0, 0, 0, 1, 0, 0, 1]
    ])
    
    src: tuple = (1, 1)
    dest: tuple = (6, 9)

    gm = GridMake()
    gm.run()

    grid, src, dest = p.from_image(gm.get_filename(dir=True))
    # grid, src, dest = p.from_image("mazes/maze.png")
    print(f"{src} -> {dest}")

    a: AStar = AStar(x=grid.shape[0], y=grid.shape[1])

    # Run the A* search algorithm
    path: np.ndarray = np.array(a.search(grid, src, dest))
    print(f"The path is: \n{path}")

    p.show_grid(grid=grid)
    p.show_grid(grid=grid, path=path)



if __name__ == "__main__":
    main()