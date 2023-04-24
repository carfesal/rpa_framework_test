"""Template robot with Python."""
from src.robots.ny_times_robot import NYTimesRobot

browser =  NYTimesRobot(url="https://www.nytimes.com/", auto_close=False)

def minimal_task():
    browser.open_browser()
    #click on the search button
    browser.begin_search("Coronavirus")\
            .configure_filters()\
            .scrape_information()
            
    
    
# data-testid="search-input"

if __name__ == "__main__":
    minimal_task()
