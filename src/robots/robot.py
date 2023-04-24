from abc import abstractmethod, ABC
from RPA.Browser.Selenium import Selenium
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from src.util.logging import logger


class Robot(ABC):
    def __init__(self, url:str, data:dict = {}, auto_close:bool = False) -> None:
        self.browser = Selenium(auto_close=auto_close)
        self.url = url
        self.recolected_data = []
        self.search_phrase = data['search_phrase'] if 'search_phrase' in data.keys() else ""
        self.sections = data['section'] if 'section' in data.keys() else []
        self.number_of_months = int(data['number_of_months']) if 'number_of_months' in data.keys() else 0
    
    def open_browser(self) -> None:
        self.browser.open_available_browser(self.url)
        self.browser.maximize_browser_window()

    def close_browser(self) -> None:
        self.browser.close_all_browsers()

    @abstractmethod
    def begin_search(self) -> None:
        pass

    @abstractmethod
    def configure_filters(self) -> None:
        pass
    
    @abstractmethod
    def scrape_information(self) -> None:
        pass

    def find_elements(self, locator:str, parent = None) -> list:
        return self.browser.find_elements(locator, parent)
    
    def find_element(self, locator:str, parent:WebElement = None, by:str = 'xpath', wait:int = 0) -> WebElement:
        try:
            if parent is not None:
                element = parent.find_element(self._get_method_of_search(by), locator) #find element in parent
            else: 
                element = self.browser.find_element(locator, parent)
        except Exception as e:
            logger.error(f"Element not found: {e}")
            element = None
        finally:
            return element
        
    def _get_method_of_search(self, by: str = 'xpath'): 
        if by == 'id':
            return By.ID
        elif by == 'css':
            return By.CSS_SELECTOR
        elif by == 'name':
            return By.NAME
        elif by == 'link':
            return By.LINK_TEXT
        elif by == 'tag_name':
            return By.TAG_NAME
        elif by == 'class':
            return By.CLASS_NAME
        elif by == 'partial_link':
            return By.PARTIAL_LINK_TEXT
        else:
            return By.XPATH
        
    def get_attribute(self, element:WebElement, attribute:str) -> str:
        if element is None: return None
        return element.get_attribute(attribute)

