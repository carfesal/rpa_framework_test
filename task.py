"""Template robot with Python."""
from RPA.Browser.Selenium import Selenium
import time
browser = Selenium(auto_close=False)


def minimal_task():
    browser.open_available_browser("https://www.nytimes.com/")
    time.sleep(5)
    #click on the search button
    browser.find_element("//button[@data-test-id='search-button']").click()
    
    #enter the search phrase
    browser.find_element("//input[@data-testid='search-input']").send_keys("coronavirus")

    #do the search
    browser.find_element("//button[@data-test-id='search-submit']").click()
    time.sleep(5)

    #search the table of articles
    
# data-testid="search-input"

if __name__ == "__main__":
    minimal_task()
