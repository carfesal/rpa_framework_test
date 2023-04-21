from abc import abstractmethod, ABC
from RPA.Browser.Selenium import Selenium

class Robot(ABC):
    def __init__(self, url:str, auto_close:bool = False) -> None:
        self.browser = Selenium(auto_close=auto_close)
        self.url = url
        self.recolected_data = []
    
    def open_browser(self) -> None:
        self.browser.open_available_browser(self.url)

    def close_browser(self) -> None:
        self.browser.close_all_browsers()

    @abstractmethod
    def begin_search(self, search_phrase:str) -> None:
        pass

    @abstractmethod
    def configure_filters(self) -> None:
        pass
    
    @abstractmethod
    def scrape_information(self) -> None:
        pass