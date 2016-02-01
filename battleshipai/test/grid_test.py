
import unittest
import numpy as np
from battleshipai.ai_controller import Grid


class GridTest(unittest.TestCase):

    def test_compute_horizontal(self):
        grid = Grid(4)
        state = np.zeros((10, 10)).astype(bool)
        state[3, 3] = True
        grid.compute_horizontal(state)
        print grid.grid
        assert False

    def test_compute_normalise(self):
        grid = Grid(3)
        state = np.zeros((10, 10)).astype(bool)
        state[3, 3] = True
        grid.compute_pmf(state)
        print grid.grid

        import matplotlib.pyplot as plt

        plt.imshow(grid.grid, interpolation="nearest")
        plt.show()
        assert False
