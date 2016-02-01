
from site_controller import BattleshipSiteController

if __name__ == "__main__":
    with BattleshipSiteController() as controller:
        controller.connect()
        controller.start_game(mode='friend')

        while True:
            if not controller.is_in_wait_mode():
                controller.click_cell(1, 1)
