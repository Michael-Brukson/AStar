import numpy as np
from AStar import AStar
from utils import Plotting
from flask import Flask

def astar_tkinter(plotter: Plotting = Plotting()) -> None:
    from drawing import GridMake

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
    ]) # type: ignore
    
    src: tuple = (1, 1)
    dest: tuple = (6, 9)

    # gm: GridMake = GridMake()
    # gm.run()

    # grid, src, dest = plotter.from_image(gm.get_filename(dir=True))
    grid, src, dest = plotter.from_image("mazes/2026-02-19T003933.795Z.png")
    print(f"{src} -> {dest}")

    a: AStar = AStar(*grid.shape)

    # Run the A* search algorithm
    path: np.ndarray = np.array(a.search(grid, src, dest))
    # print(f"The path is: \n{path}")

    # plotter.show_grid(grid=grid)
    plotter.show_grid(grid=grid, path=path)

def astar_flask() -> None:
    from __init__ import create_app
    
    app: Flask = create_app()
    app.run(host='0.0.0.0', port=55317, debug=True)
    

def main():
    p: Plotting = Plotting()

    astar_flask()
    # astar_tkinter()


if __name__ == "__main__":
    main()