from src.robots.robot import Robot
import time

class NYTimesRobot(Robot):
    def __init__(self, url:str, auto_close:bool = False) -> None:
        super().__init__(url=url, auto_close=auto_close)

    def begin_search(self, search_phrase:str) -> None:
        self.browser.find_element("//button[@data-test-id='search-button']").click()
        self.browser.find_element("//input[@data-testid='search-input']").send_keys(search_phrase)
        self.browser.find_element("//button[@data-test-id='search-submit']").click()
        time.sleep(5)
