from src.robots.robot import Robot
import time
import src.util.helpers as helpers
from RPA.Excel.Files import Files
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from src.util.logging import logger


class NYTimesRobot(Robot):
    def __init__(self, url:str, data:dict = {}, auto_close:bool = False) -> None:
        super().__init__(url=url, data=data, auto_close=auto_close)
        self.excel_file = self.create_output_file()

    def begin_search(self):
        '''
        Begin the search using the search phrase        
        '''         
        self.click_button_on_page("//button[@data-test-id='search-button']")
        self.browser.input_text("//input[@data-testid='search-input']", self.search_phrase)
        self.click_button_on_page("//button[@data-test-id='search-submit']")
        return self

    def configure_filters(self):
        '''
        Configure filters for the search of articles
        '''
        self.configure_section_filter(self.sections)
        self.order_results_by("newest")
        #configure date range
        date_range = self.get_date_range()
        self.configure_date_range(date_range[0], date_range[1])
        return self
    
    def scrape_information(self) -> None:
        '''
        Scrape information from the articles loaded in the page
        '''
        results_locator = "//ol[@data-testid='search-results']/li[@data-testid='search-bodega-result']"
        show_more_button_locator = "//button[@data-testid='search-show-more-button']"
        results = self.load_more_article_results(results_locator)
        last_result_counter = 0
        scraping_attempts = 5

        if len(results) == 0:
            logger.info("No results found")
            return
        
        while (self.is_size_of_output_allowed() and \
              (self.browser.does_page_contain_element(show_more_button_locator) or len(results) > last_result_counter) and \
              scraping_attempts > 0):
            
            try:
                for result in results[last_result_counter:]:
                    self.extract_information_from_article(result)
                last_result_counter = len(results)
                self.scroll_and_click_more_articles(show_more_button_locator)
                results = self.load_more_article_results(results_locator)
            except Exception as e:
                logger.warning(f"Error while scraping information: {e}")
            finally:
                if last_result_counter == len(results): 
                    scraping_attempts -= 1
                    logger.info(f"Scraping attempts left: {scraping_attempts}")
                    
        
        logger.info(f"Amount of articles: {len(self.recolected_data)}")        
        return self
    
    def generate_output(self) -> None:
        # self.create_output_file()
        # self.compress_images() #commented because it is not that the client wants. No need to compress images
        return self

    def compress_images(self) -> None:
        try:
            helpers.zip_folder()
        except Exception as e:
            logger.warning(f"Error while compressing images: {e}")

    def create_output_file(self) -> Files:
        '''
        Creates an excel file with the information scraped
        '''
        # Create modern format workbook with a path set.
        lib = Files()
        lib.create_workbook(path="./output/articles.xlsx", fmt="xlsx")
        lib.save_workbook()

        # Create a worksheet with a name set.
        lib.create_worksheet(name="articles", header=True)
        lib.save_workbook()               
        
        return lib
    
    def configure_section_filter(self, sections:list=[]) -> None:
        '''
        sections: list of sections to filter by. If empty, all sections will be selected
        '''
        if len(sections) == 0 : return
        #click the sections filter
        self.click_button_on_page("//div[@data-testid='section']//button[@data-testid='search-multiselect-button']")
        #select all sections checkboxes
        self.select_sections(sections)        
        #close the sections filter
        self.click_button_on_page("//div[@data-testid='section']//button[@data-testid='search-multiselect-button']")

    def select_sections(self, sections:list = []) -> None:
        '''
        sections: list of sections to select. If empty, all sections will be selected
        '''
        #select all sections checkboxes
        selection_checkboxes = self.find_elements("//div[@data-testid='section']//input[@data-testid='DropdownLabelCheckbox']")

        for selection in selection_checkboxes:
            if (self.contains_text(selection, sections)):
                selection.click() #click checkboxes if there is a match with sections list

    def order_results_by(self, order_by:str) -> None:
        '''
        :param order_by: order by which the results will be displayed
        '''
        self.browser.select_from_list_by_value("//select[@data-testid='SearchForm-sortBy']", order_by)

    def contains_text(self, element, sections:list = []) -> bool:
        value = element.get_attribute("value").split("|")
        return (element.get_attribute("value").split("|")[0] in sections) if len(value) > 0 else False
    
    def configure_date_range(self, since_date:str, to_date:str) -> None:
        '''
        :param since_date: date from which the articles will be displayed
        :param to_date: date until which the articles will be displayed
        '''
        #click the date filter
        self.click_button_on_page("//button[@data-testid='search-date-dropdown-a']")

        #click the specific dates option
        self.click_button_on_page("//li/button[@value='Specific Dates']")

        #input the dates
        self.browser.input_text("//input[@id='startDate']", since_date)   
        self.browser.input_text("//input[@id='endDate']", to_date) 

        #close the date filter
        self.click_button_on_page("//button[@data-testid='search-date-dropdown-a']")

    def load_more_article_results(self, articles_locator:str) -> list:
        return self.browser.find_elements(locator=articles_locator)        
    
    def scroll_and_click_more_articles(self, show_more_locator:str) -> None:
        if self.browser.does_page_contain_element(show_more_locator):
            self.browser.scroll_element_into_view(show_more_locator)
            self.click_button_on_page(show_more_locator)
            
    
    def extract_information_from_article(self, article):
        '''
        Extracts the information from an article and appends it to the recolected_data list
        :param article: article from which the information will be extracted
        '''
        date = self.get_attribute(self.find_element("./div/span", article), "innerHTML")
        title = self.get_attribute(self.find_element("./div/div/div/a/h4", article), "innerHTML")
        description = self.get_attribute(self.find_element("./div/div/div/a/p", article), "innerHTML")
        img_src = self.get_attribute(self.find_element("./div/div//img", article), "src")
        
        #Trying to download the image
        self.download_article_images(img_src)
        
        #Appending the information to the recolected_data list
        extracted_data = self.fill_data_information(date, title, description, img_src)
        self.append_data_to_excel(extracted_data)
        self.recolected_data.append(extracted_data)

    def download_article_images(self, img_src:str = None) -> str:
        '''
        Download the image of an article
        :param img_src: source of the image
        '''
        img_path = None
        try:
            if self.number_of_files_processed < self.max_amount_files:
                if (img_src is None): 
                    raise Exception("Image source is None")
                img_path = helpers.download_image(img_src, helpers.get_filename(img_src)); self.number_of_files_processed += 1
                logger.info(f"Image created at path: {img_path}")
            else: 
                logger.info("Max amount of files reached. The image will not be downloaded.")
        except Exception as e:
            logger.warning(f"Error while downloading image: {e}")            
        finally:
            return img_path
        
    def fill_data_information(self, date, title, description, img_src):
        '''
        Fills the data information of an article
        :param date: date of the article
        :param title: title of the article
        :param description: description of the article
        :param img_src: image source of the article
        '''
        data = {
            "date": date,
            "title": title,
            "description": description,
            "counts_of_search_phase" : helpers.count_of_ocurrences_in_text(title, self.search_phrase) + helpers.count_of_ocurrences_in_text(description, self.search_phrase),
            "picture_filename": helpers.get_filename(img_src),
            "contains_money": helpers.check_if_text_contains_money(title) or helpers.check_if_text_contains_money(description)
        }
        return data

    def get_date_range(self) -> tuple:
        '''
        Returns the date range based on the number of months to search
        '''
        date_until = datetime.today()

        if self.number_of_months in [0,1]:
            date_from = datetime.today().replace(day=1)
        else:
            date_from = (date_until - relativedelta(months=self.number_of_months - 1)).replace(day=1)

        return (datetime.strftime(date_from, '%m/%d/%Y'), datetime.strftime(date_until, '%m/%d/%Y'))
        
    def append_data_to_excel(self, data:dict) -> None:
        '''
        Appends the recolected data to the excel file
        :param data: data to append
        '''
        self.excel_file.append_rows_to_worksheet(data)
        self.excel_file.save_workbook()

    def is_size_of_output_allowed(self):
        '''
        Checks if the output is greater than the max amount of rows allowed
        '''
        output_folder_size = helpers.get_size_of_folder()
        logger.info(f"Output folder size: {output_folder_size}")
        if output_folder_size >= self.max_size_of_folder:
            logger.info("Output folder size is greater than the max output size. Deleting output folder...")
            return False
        return True
            
    
