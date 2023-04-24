from src.robots.robot import Robot
import time
import src.util.helpers as helpers
from RPA.Excel.Files import Files


class NYTimesRobot(Robot):
    def __init__(self, url:str, auto_close:bool = False) -> None:
        super().__init__(url=url, auto_close=auto_close)

    def begin_search(self, search_phrase:str):
        '''
        Begin the search using the search phrase
        search_phrase: phrase to search for
        '''
        self.search_phrase = search_phrase
        self.browser.click_button("//button[@data-test-id='search-button']")
        self.browser.input_text("//input[@data-testid='search-input']", search_phrase)
        self.browser.click_button("//button[@data-test-id='search-submit']")
        time.sleep(5)
        
        return self

    def configure_filters(self):
        '''Configure filters for the search of articles'''

        self.configure_section_filter()
        self.order_results_by("newest")
        self.configure_date_range("04/19/2023", "04/22/2023")
        time.sleep(2)
        #self.scrape_information()
        return self
    
    def configure_section_filter(self, sections:list=[]) -> None:
        '''
        sections: list of sections to filter by. If empty, all sections will be selected
        '''
        if len(sections) == 0 : return

        #click the sections filter
        self.click_button_on_page("//div[@data-testid='section']//button[@data-testid='search-multiselect-button']")
        time.sleep(2)

        #select all sections checkboxes
        self.select_sections(sections)
        
        #close the sections filter
        self.click_button_on_page("//div[@data-testid='section']//button[@data-testid='search-multiselect-button']")

    def select_sections(self, sections:list = []) -> None:
        '''
        sections: list of sections to select. If empty, all sections will be selected
        '''
        #select all sections checkboxes
        selection_checkboxes = self.browser.find_elements("//div[@data-testid='section']//input[@data-testid='DropdownLabelCheckbox']")

        for selection in selection_checkboxes:
            print(selection.get_attribute("value").split("|"))
            if (self.contains_text(selection, sections)):
                selection.click() #click checkboxes if there is a match with sections list

    def order_results_by(self, order_by:str) -> None:
        '''
        :param order_by: order by which the results will be displayed
        '''
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

        if len(results) == 0:
            print("No results found")
            return
        
        while self.browser.does_page_contain_element(show_more_button_locator) or len(results) > last_result_counter:
            for result in results[last_result_counter:]:
                self.extract_information_from_article(result)                      
            last_result_counter = len(results)
            self.scroll_and_click_more_articles(show_more_button_locator)
            results = self.load_more_article_results(results_locator)
        
        print("Amount of articles: ", len(self.recolected_data))
        self.create_excel_file()
        return self
            
    
    def configure_date_range(self, since_date:str, to_date:str) -> None:
        '''
        :param since_date: date from which the articles will be displayed
        :param to_date: date until which the articles will be displayed
        '''
        #click the date filter
        self.browser.click_button("//button[@data-testid='search-date-dropdown-a']")

        #click the specific dates option
        self.browser.click_button("//li/button[@value='Specific Dates']")

        #input the dates
        self.browser.input_text("//input[@id='startDate']", since_date); time.sleep(1)        
        self.browser.input_text("//input[@id='endDate']", to_date); time.sleep(1)

        #close the date filter
        self.click_button_on_page("//button[@data-testid='search-date-dropdown-a']"); time.sleep(2)

    def load_more_article_results(self, articles_locator:str) -> list:
        return self.browser.find_elements(locator=articles_locator)
        
    
    def scroll_and_click_more_articles(self, show_more_locator:str) -> None:
        if self.browser.does_page_contain_element(show_more_locator):
            self.browser.scroll_element_into_view(show_more_locator); time.sleep(2)
            self.click_button_on_page(show_more_locator); time.sleep(2)
            
    
    def extract_information_from_article(self, article):
        date = self.get_attribute(self.find_element("./div/span", article), "innerHTML")
        title = self.get_attribute(self.find_element("./div/div/div/a/h4", article), "innerHTML")
        description = self.get_attribute(self.find_element("./div/div/div/a/p", article), "innerHTML")
        img_src = self.get_attribute(self.find_element("./div/div//img", article), "src")
        
        self.recolected_data.append(self.fill_data_information(date, title, description, img_src))

    def fill_data_information(self, date, title, description, img_src):
        data = {
            "date": date,
            "title": title,
            "description": description,
            "counts_of_search_phase" : helpers.count_of_ocurrences_in_text(self.search_phrase, title) + helpers.count_of_ocurrences_in_text(self.search_phrase, description),
            "picture_filename": helpers.get_filename(img_src),
            "contains_money": helpers.check_if_text_contains_money(title) or helpers.check_if_text_contains_money(description)
        }
        return data
        
    def create_excel_file(self):
        if len(self.recolected_data) == 0:
            print("No data to create excel file")
            return
        
        # Create modern format workbook with a path set.
        lib = Files()
        lib.create_workbook(path="./output/articles.xlsx", fmt="xlsx")
        lib.save_workbook()

        # Create a worksheet with a name set.
        lib.create_worksheet(name="articles",content=self.recolected_data)
        lib.save_workbook()               
        
        return self

