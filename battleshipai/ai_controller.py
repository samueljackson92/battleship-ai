
import logging
import numpy as np

logging.basicConfig(level=logging.INFO)


class Grid(object):

    def __init__(self, shape_size):
        self.grid_width = 10
        self.shape_size = shape_size
        self.grid = np.zeros((self.grid_width, self.grid_width)).astype(float)

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
        self._logger = logging.getLogger(__name__)
        self._controller = controller
        self._ship_sizes = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
        self._grids = [Grid(x) for x in self._ship_sizes]

    def play(self):
        self.controller.connect()
        self.controller.start_game(mode='friend')

        while True:
            if not self.controller.is_in_wait_mode():
                # calculate the best move from the current state
                state = self.controller.get_battlefield_state()
                joint = self.compute_joint_pmf(state)
                point = self.find_next_target(joint)
                self.controller.click_cell(*point)

    def compute_joint_pmf(self, state):
        for g in self._grids:
            g.compute_pmf(state)

        joint = np.zeros((10, 10)).astype(float)
        joint = reduce(lambda x, y: x+y.grid, self._grids, joint)
        total = joint.sum()
        if total > 0:
            joint /= total
        return joint

    def find_next_target(self, joint):
        self._logger.info("Best probability is %f" % np.max(joint))
        idx = np.argmax(joint)
        x = idx % 10
        y = idx / 10
        return x, y

    @property
    def controller(self):
        return self._controller
