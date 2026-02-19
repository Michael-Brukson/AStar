import matplotlib.pyplot as plt
import cv2 as cv
import numpy as np


class Plotting():
    BLUE: np.ndarray = np.array([255, 0, 0], dtype=np.uint8)
    RED: np.ndarray = np.array([0, 0, 255], dtype=np.uint8)

    def __init__(self):
        pass
    
    def show_grid(self, grid: list[int], path: list[tuple[int, int]] = []) -> None:
        plt.imshow(grid, cmap='gray')

        if np.any(path, None):
            x: list = path[:, 1]
            y: list = path[:, 0]
            plt.scatter(x[0], y[0], c='red', s=100, zorder=5, edgecolors='black')
            plt.scatter(x[-1], y[-1], c='blue', s=100, zorder=5, edgecolors='black')
            plt.plot(x, y, color='green', linewidth=3)
        
        plt.show()

    # return a tuple of ints representing a single coordinate that is the centroid of a groupd of coords.
    def _centroid(self, coords: np.ndarray) -> tuple[int, int]:
        # get all x and y coordinates
        xs = coords[:, 1]
        ys = coords[:, 0]

        # simple average
        x: int = int(np.mean(xs))
        y: int = int(np.mean(ys))

        return (y, x)

    # in a black/white image with normalized values 0/1, set a list of coordinates to white (1)
    def _set_available(self, img: np.ndarray, coords: np.ndarray) -> np.ndarray:
        for coord in coords:
            img[coord[0], coord[1]] = 1

        return img


    def from_image(self, file: str) -> tuple:
        img: np.ndarray = cv.imread(file)[:,:,:3] # type: ignore

        # get all pixels that represent sources and destinations
        srcs: np.ndarray = np.argwhere(np.all(img == self.RED, axis=-1))
        dests: np.ndarray = np.argwhere(np.all(img == self.BLUE, axis=-1))

        # get centroid for src and destination
        src = self._centroid(srcs)
        dest = self._centroid(dests)
        
        # convert to black/white 0/255
        img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        _, img = cv.threshold(img, 128, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
        # convert to black/white 0/1
        img = np.where(img == 255, 1, 0).astype(np.uint8)

        # set source and destination to available
        img = self._set_available(img=img, coords=srcs)
        img = self._set_available(img=img, coords=dests)

        return (img, src, dest)


if __name__ == "__main__":
    p: Plotting = Plotting()

    file: str = 'mazes/2026-02-19T003933.795Z.png'

    grid, src, dest = p.from_image(file=file)
    
    print(f"{src} -> {dest}")

    p.show_grid(grid)