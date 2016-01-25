
from site_controller import BattleshipSiteController

if __name__ == "__main__":
    with BattleshipSiteController() as controller:
        controller.connect()
        controller.start_game(mode='friend')

        while True:
            print controller.get_battlefield_state()
