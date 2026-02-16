import matplotlib.pyplot as plt
import cv2 as cv
import numpy as np


class Plotting():
    BLUE: np.ndarray = np.array([255, 0, 0], dtype=np.uint8)
    RED: np.ndarray = np.array([0, 0, 255], dtype=np.uint8)

    def __init__(self):
        pass
    
    def show_grid(self, grid: list, path: list = None) -> None:
        plt.imshow(grid, cmap='gray')

        if np.any(path, None):
            x: list = path[:, 1]
            y: list = path[:, 0]
            plt.scatter(x[0], y[0], c='red', s=100, zorder=5, edgecolors='black')
            plt.scatter(x[-1], y[-1], c='blue', s=100, zorder=5, edgecolors='black')
            plt.plot(x, y, color='green', linewidth=3)
        
        plt.show()

    # TODO: Replace finding of sources with finding of centroids
    def get_centroid():
        pass


    def from_image(self, file: str) -> tuple:
        img: np.ndarray = cv.imread(file)[:,:,:3]
        # TODO: Replace this with finding centroids instead
        # TODO: Once centroid found, replace rest of srcs/dests with white
        src: tuple = np.argwhere(np.all(img == self.RED, axis=-1))[0]
        dest: tuple = np.argwhere(np.all(img == self.BLUE, axis=-1))[0]
        
        img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        img = np.where(img == 255, 1, 0).astype(np.uint8)

        img[src[0], src[1]] = 1
        img[dest[0], dest[1]] = 1

        return (img, src, dest)


if __name__ == "__main__":
    p: Plotting = Plotting()

    file: str = 'maze.png'

    grid, src, dest = p.from_image(file=file)
    
    print(f"{src} -> {dest}")

    p.show_grid(grid)

    print(grid)