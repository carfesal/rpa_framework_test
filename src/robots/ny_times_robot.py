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
        self.configure_date_range("04/19/2023", "04/22/2023")
        #self.scrape_information()
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
        results_locator = "//ol[@data-testid='search-results']/li[@data-testid='search-bodega-result']"
        show_more_button_locator = "//button[@data-testid='search-show-more-button']"
        results = self.load_more_article_results(results_locator)
        last_result_counter = 0

        while self.browser.does_page_contain_element(show_more_button_locator) and len(results) > last_result_counter:
            for result in results[last_result_counter:]:
                self.recolected_data.append(self.extract_information(result))
            last_result_counter = len(results)
            self.scroll_and_click_more_articles(show_more_button_locator)
            results = self.load_more_article_results(results_locator)
        
        print(len(self.recolected_data))
            
    
    def configure_date_range(self, since_date:str, to_date:str) -> None:
        self.browser.click_button("//button[@data-testid='search-date-dropdown-a']")
        self.browser.click_button("//li/button[@value='Specific Dates']")
        self.browser.input_text("//input[@id='startDate']", since_date)
        time.sleep(2)
        self.browser.input_text("//input[@id='endDate']", to_date)
        time.sleep(2)
        self.browser.click_button("//button[@data-testid='search-date-dropdown-a']")

    def load_more_article_results(self, articles_locator:str) -> list:
        return self.browser.find_elements(locator=articles_locator)
        
    
    def scroll_and_click_more_articles(self, show_more_locator:str) -> None:
        if not self.browser.is_element_visible(show_more_locator):
            self.browser.scroll_element_into_view(show_more_locator)
            time.sleep(2)
        self.browser.click_button(show_more_locator)
    
