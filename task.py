"""Template robot with Python."""
from src.robots.ny_times_robot import NYTimesRobot
import src.util.work_items as work_items
from src.util.logging import logger

variables = work_items.get_work_item_variables()
browser =  NYTimesRobot(url="https://www.nytimes.com/", data=variables, auto_close=False)

def minimal_task():
    try:
        browser.open_browser()
        #click on the search button
        browser.begin_search()\
                .configure_filters()\
                .scrape_information()\
                .create_output_file()
    except Exception as e:
        logger.warning(f"Error: {e}")
    finally:
        browser.close_browser()            
    
    
# data-testid="search-input"

if __name__ == "__main__":
    minimal_task()
