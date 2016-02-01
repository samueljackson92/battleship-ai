
import numpy as np


class Grid(object):

    def __init__(self, shape_size):
        self.grid_width = 10
        self.shape_size = shape_size
        self.grid = np.zeros((self.grid_width, self.grid_width))

    def compute_pmf(self, state):
        self.compute_horizontal(state)
        self.compute_vertical(state)
        self.normalise()

    def normalise(self):
        total = self.grid.sum()
        if total > 0:
            self.grid = self.grid / total

    def compute_vertical(self, state):
        for (x, y), element in np.ndenumerate(state):
            cannot_fit = False
            for k in xrange(x, x+self.shape_size):
                # check if the block crosses an already tested space
                # and it is within the bounds of the grid
                if k >= self.grid_width or state[k, y]:
                    cannot_fit = True
                    break

            # the block has passed all checks, it can fit here.
            if not cannot_fit:
                for k in xrange(x, x+self.shape_size):
                    self.grid[k, y] += 1

    def compute_horizontal(self, state):
        for (x, y), element in np.ndenumerate(state):
            cannot_fit = False
            for k in xrange(y, y+self.shape_size):
                # check if the block crosses an already tested space
                # and it is within the bounds of the grid
                if k >= self.grid_width or state[x, k]:
                    cannot_fit = True
                    break

            # the block has passed all checks, it can fit here.
            if not cannot_fit:
                for k in xrange(y, y+self.shape_size):
                    self.grid[x, k] += 1


class BattleshipAI(object):

    def __init__(self, controller):
        self._controller = controller

    def play(self):
        self.controller.connect()
        self.controller.start_game(mode='friend')

        while True:
            if not self.controller.is_in_wait_mode():
                # calculate the best move from the current state
                state = self.controller.get_battlefield_state()
                self.compute_horizontal(state)

                print state
                # play move

    @property
    def controller(self):
        return self._controller
