import logging
import numpy as np
from selenium import webdriver
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BattleshipSiteController(object):

    def __init__(self):
        self._site_address = "http://en.battleship-game.org"
        self._grid_size = 10

    def __enter__(self):
        self._driver = webdriver.Firefox()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self._driver is not None:
            self._driver.close()

    def connect(self):
            logger.info("Attempting to make connection to %s" % self._site_address)
            self._driver.get(self._site_address)

    def is_in_wait_mode(self):
        """ Check if we are waiting for the other player.

        If we're in wait mode then we are wating for the other player to make a
        move or connect if in friend mode.
        """
        battlefield = self.get_rival_battlefield()
        classnames = battlefield.get_attribute('class').split(' ')
        return ('battlefield__wait' in classnames)

    def get_battlefield_state(self):
        table = self.get_battlefield_table()
        table_html = BeautifulSoup(table.get_attribute('innerHTML'))

        def check_state(cell):
            return "battlefield-cell__empty" in cell['class']

        cells = [check_state(cell) for row in table_html.find_all("tr")
                      for cells in row.find_all("td")
                      for cell in cells]

        grid_state = np.array(cells).reshape(self._grid_size, self._grid_size)
        return grid_state

    def click_cell(self, i, j):
        # This is a terrible hack to click on a specifc cell in the rival's
        # table. For some reason beyond my understanding selenium doesn't do
        # anything when invoking .click() here.
        # This also had issues in selenium 2.49 forcing me to revert to 2.48
        # See: http://stackoverflow.com/questions/34969006/
        code = ("document.getElementsByClassName('battlefield__rival')[0]"
                ".childNodes[1].childNodes[1].childNodes[0]"
                ".rows[%d].cells[%d].children[0].click()" % (j, i))
        self._driver.execute_script(code)

    def get_rival_battlefield(self):
        classname = 'battlefield__rival'
        return self._driver.find_element_by_xpath("//div[contains(@class, '%s')]" % classname)

    def click_link(self, text):
        link = self._driver.find_element_by_link_text(text)
        link.click()

    def click_div_by_class_name(self, text):
        div = self.get_div_by_class_name(text)
        div.click()

    def get_battlefield_table(self):
        text = 'battlefield-table'
        return self._driver.find_element_by_xpath("//table[@class='%s']" % text)

    def get_div_by_class_name(self, text):
        return self._driver.find_element_by_xpath("//div[@class='%s']" % text)

    def start_game(self, mode='random'):
        if mode == 'friend':
            self.click_link('friend')
        self.click_div_by_class_name('battlefield-start-button')
