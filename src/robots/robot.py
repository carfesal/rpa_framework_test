import src.robots.helpers.selenium as selenium_helpers
import src.robots.helpers.validation as validation_helpers
from abc import abstractmethod, ABC
from RPA.Browser.Selenium import Selenium
from selenium.webdriver.remote.webelement import WebElement
from src.util.logging import logger
from selenium.common.exceptions import ElementNotVisibleException, NoSuchElementException, \
    ElementClickInterceptedException, StaleElementReferenceException, ElementNotInteractableException


class Robot(ABC):
    def __init__(self, url: str, data: dict = {}, auto_close: bool = False) -> None:
        self.browser = Selenium(auto_close=auto_close)
        self.url = url
        self.search_phrase, self.sections, self.number_of_months = validation_helpers.validate_data(data)
        self.recolected_data = []
        self.max_amount_files = 45
        self.max_size_of_folder = 20 * 1024 * 1024  # 20MB
        self.number_of_files_processed = 0

    def open_browser(self) -> None:
        """Open the browser and go to the url"""
        self.browser.open_available_browser(self.url)
        self.browser.maximize_browser_window();
        self.browser.set_selenium_timeout(10)

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

    def find_elements(self, locator: str, parent=None, wait: bool = True) -> list:
        """Find elements in the page

        :param locator: locator to find the elements
        :param parent: parent element to find the elements in
        :param wait: wait until the element is visible
        :return: list of elements
        """
        if wait:
            self.browser.wait_until_page_contains_element(locator)
        return self.browser.find_elements(locator, parent)

    def find_element(self, locator: str, parent: WebElement = None, by: str = 'xpath',
                     wait: bool = False) -> WebElement:
        """Find an element in the page

        :param locator: locator to find the element
        :param parent: parent element to find the element in
        :param by: method of search
        :param wait: wait until the element is visible
        :return: element
        """
        element = None
        try:
            if parent is not None:
                element = parent.find_element(selenium_helpers.get_method_of_search(by),
                                              locator)  # find element in parent
            else:
                element = self.browser.find_element(locator, parent)
        except (ElementNotVisibleException, NoSuchElementException) as e:
            logger.warning(f"Element not found: {e}")
            element = None
        except StaleElementReferenceException as e:
            logger.warning(f"Element references is not the exact: {e}")
            element = None
        finally:
            return element

    def click_button_on_page(self, button_xpath: str, wait_for_visibility: bool = True) -> None:
        """Click a button in the page
        :param button_xpath: xpath of the button
        :param wait_for_visibility: wait until the button is visible
        """
        try:
            if wait_for_visibility:
                self.browser.wait_and_click_button(button_xpath)
            else:
                self.browser.click_button(button_xpath)
        except (ElementClickInterceptedException, ElementNotInteractableException) as e:
            logger.warning(f"Element cannot be clicked: {e}")
            logger.info("Trying to click with javascript.... ")
            self.browser.driver.execute_script("arguments[0].click();", self.find_element(button_xpath))
        except NoSuchElementException as e:
            logger.warning(f"Element not found: {e}")
