from src.robots.robot import Robot
import time

class NYTimesRobot(Robot):
    def __init__(self, url:str, auto_close:bool = False) -> None:
        super().__init__(url=url, auto_close=auto_close)

    def begin_search(self, search_phrase:str):
        self.browser.click_button("//button[@data-test-id='search-button']")
        self.browser.input_text("//input[@data-testid='search-input']", search_phrase)
        self.browser.click_button("//button[@data-test-id='search-submit']")
        time.sleep(5)
        
        return self

    def configure_filters(self):
        self.configure_section_filter()
        self.order_results_by("newest")
        return self
    
    def configure_section_filter(self, sections:list=['Science', 'World']) -> None:
        #click the sections filter
        self.click_button_on_page("//div[@data-testid='section']//button[@data-testid='search-multiselect-button']")
        time.sleep(2)

        #select all sections checkboxes
        selection_checkboxes = self.browser.find_elements("//div[@data-testid='section']//input[@data-testid='DropdownLabelCheckbox']")

        for selection in selection_checkboxes:
            print(selection.get_attribute("value"))
            if (self.contains_text(selection, sections)):
                selection.click() #click checkboxes if there is a match with sections list
        
        #close the sections filter
        self.click_button_on_page("//div[@data-testid='section']//button[@data-testid='search-multiselect-button']")

    def order_results_by(self, order_by:str) -> None:
        self.browser.select_from_list_by_value("//select[@data-testid='SearchForm-sortBy']", order_by)        
        
    def click_button_on_page(self, button_xpath:str) -> None:
        self.browser.click_button(button_xpath)        

    def contains_text(self, element, sections:list = []) -> bool:
        value = element.get_attribute("value").split("|")
        return (element.get_attribute("value").split("|")[0] in sections) if len(value) > 0 else False
    
    def scrape_information(self) -> None:
        return super().scrape_information()
    
    def configure_date_range(since_date:str, to_date:str) -> None:
        pass