
import click
from ai_controller import BattleshipAI
from site_controller import BattleshipSiteController


@click.group()
def cli():
    pass


@cli.command()
def start():
    click.echo('Starting game...')
    with BattleshipSiteController() as controller:
        ai = BattleshipAI(controller)
        ai.play()
