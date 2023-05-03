from abc import abstractmethod, ABC
from RPA.Browser.Selenium import Selenium
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from src.util.logging import logger
from selenium.common.exceptions import ElementNotVisibleException, NoSuchElementException, ElementClickInterceptedException

class Robot(ABC):
    def __init__(self, url:str, data:dict = {}, auto_close:bool = False) -> None:
        self.browser = Selenium(auto_close=auto_close)
        self.url = url
        self.search_phrase, self.sections, self.number_of_months = self._validate_data(data)        
        self.recolected_data = []
        self.max_amount_files = 46
        self.max_size_of_folder = 20 * 1024 * 1024 #20MB
        self.number_of_files_processed = 0
    
    def open_browser(self) -> None:
        self.browser.open_available_browser(self.url)
        self.browser.maximize_browser_window(); self.browser.set_selenium_timeout(10)

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
    
    @abstractmethod
    def generate_output(self) -> None:
        pass

    def find_elements(self, locator:str, parent = None, wait:bool = True) -> list:
        if wait:
            self.browser.wait_until_page_contains_element(locator)
        return self.browser.find_elements(locator, parent)
    
    def find_element(self, locator:str, parent:WebElement = None, by:str = 'xpath', wait:bool = False) -> WebElement:
        try:
            if parent is not None:
                element = parent.find_element(self._get_method_of_search(by), locator) #find element in parent
            else: 
                element = self.browser.find_element(locator, parent)                
        except Exception as e:
            logger.warning(f"Element not found: {e}")
            element = None
        finally:
            return element
    
    def click_button_on_page(self, button_xpath:str, wait_for_visibility:bool=True) -> None:
        try:
            if wait_for_visibility:
                self.browser.wait_and_click_button(button_xpath)
            else:
                self.browser.click_button(button_xpath)
        except Exception as e:
            logger.warning(f"Element cannot be clicked: {e}")
            logger.info("Trying to click with javascript.... ")
            self.browser.driver.execute_script("arguments[0].click();", self.find_element(button_xpath))
        
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

    def _validate_data(self, data:dict) -> tuple:
        search_phrase = "rpachallenge"
        sections = []
        number_of_months = 0

        if ('search_phrase' in data.keys()) and type(data['search_phrase']) == str:
            search_phrase = data['search_phrase']
        
        if ('section' in data.keys()):
            if (type(data['section']) == list):
                sections = data['section']
            elif type(data['section']) == str:
                sections.append(data['section'])
        
        if ('number_of_months' in data.keys()) and (type(data['number_of_months']) == int) and data['number_of_months'] >= 0 :
            number_of_months = data['number_of_months']
        
        return (search_phrase, sections, number_of_months)
