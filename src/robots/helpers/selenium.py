from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


def get_method_of_search(by: str = 'xpath'):
    """Get the method of search for the element
        :param by: method of search string
        :return: method of search
        """
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


def get_attribute(element: WebElement, attribute: str) -> str:
    """Get the attribute of an element
        :param element: element to get the attribute
        :param attribute: attribute to get
        :return: attribute value
        """
    if element is None:
        return None
    return element.get_attribute(attribute)
