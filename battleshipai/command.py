
import click
from site_controller import BattleshipSiteController


@click.group()
def cli():
    pass


@cli.command()
def start():
    click.echo('Starting game...')
    with BattleshipSiteController() as controller:
        controller.connect()
        controller.start_game(mode='friend')

        while True:
            if not controller.is_in_wait_mode():
                controller.click_cell(1, 1)
