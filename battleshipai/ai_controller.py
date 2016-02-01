
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
                print state
                # play move

    @property
    def controller(self):
        return self._controller
