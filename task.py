"""Template robot with Python."""
from src.robots.ny_times_robot import NYTimesRobot
import src.util.work_items as work_items
from src.util.env_variables_input import get_environment_input_data
from src.util.logging import logger
from src.util.helpers import print_variables

env_variables = get_environment_input_data(); print_variables(variables=env_variables)
work_items_variables = work_items.get_work_item_variables()

data = env_variables if bool(env_variables) else work_items_variables; print_variables(variables=data)
browser =  NYTimesRobot(url="https://www.nytimes.com/", data=data, auto_close=False)

def minimal_task():
    try:
        browser.open_browser()
        #click on the search button
        browser.begin_search()\
                .configure_filters()\
                .scrape_information()\
                .generate_output()
    except Exception as e:
        logger.warning(f"Error: {e}")
    finally:
        browser.close_browser()   

if __name__ == "__main__":
    minimal_task()
    