from abc import abstractmethod, ABC
from RPA.Browser.Selenium import Selenium

class Robot(ABC):
    def __init__(self, url:str, auto_close:bool = False) -> None:
        self.browser = Selenium(auto_close=auto_close)
        self.url = url
    
    def open_browser(self) -> None:
        self.browser.open_available_browser(self.url)

    @abstractmethod
    def begin_search(self, search_phrase:str) -> None:
        pass