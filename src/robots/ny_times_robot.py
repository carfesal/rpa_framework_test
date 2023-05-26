import time
import src.util.helpers as helpers
import src.robots.helpers.selenium as selenium_helpers
from src.robots.robot import Robot
from RPA.Excel.Files import Files
from src.util.logging import logger
from src.util.exceptions import ImageCouldNotBeDownloadedError


class NYTimesRobot(Robot):
    def __init__(self, url: str, data: dict = {}, auto_close: bool = False) -> None:
        super().__init__(url=url, data=data, auto_close=auto_close)
        self.excel_file = self.create_output_file()

    def begin_search(self) -> None:
        """Begin the search using the search phrase"""
        self.click_button_on_page("//button[@data-test-id='search-button']")
        self.browser.input_text("//input[@data-testid='search-input']", self.search_phrase)
        self.click_button_on_page("//button[@data-test-id='search-submit']")
        return self

    def configure_filters(self) -> None:
        """Configure filters for the search of articles"""
       # Configure section filters
        if len(self.sections) == 0:
            self.click_button_on_page(
                "//div[@data-testid='section']//button[@data-testid='search-multiselect-button']")  # click the sections filter
            self.select_sections(self.sections)  # select all sections checkboxes
            self.click_button_on_page(
                "//div[@data-testid='section']//button[@data-testid='search-multiselect-button']")  # close the sections filter

        # Order Results by newest
        try:
            self.browser.wait_until_page_contains_element("//select[@data-testid='SearchForm-sortBy']")
            self.browser.select_from_list_by_value("//select[@data-testid='SearchForm-sortBy']", "newest")
        except Exception as e:
            logger.warning(f"The element cannot be selected: {e}")

        # configure date range
        date_range = helpers.get_date_range(self.number_of_months)
        since_date = date_range[0]
        to_date = date_range[1]
        self.click_button_on_page("//button[@data-testid='search-date-dropdown-a']")  # click the date filter
        self.click_button_on_page("//li/button[@value='Specific Dates']")
        time.sleep(2)  # click the specific dates option

        # input the dates
        self.browser.input_text("//input[@id='startDate']", since_date)
        self.browser.input_text("//input[@id='endDate']", to_date)
        self.click_button_on_page("//button[@data-testid='search-date-dropdown-a']")  # close the date filter

        return self

    def scrape_information(self) -> None:
        """Scrape information from the articles loaded in the page"""
        results_locator = "//ol[@data-testid='search-results']/li[@data-testid='search-bodega-result']"
        show_more_button_locator = "//button[@data-testid='search-show-more-button']"
        results = self.load_more_article_results(results_locator)
        last_result_counter = 0
        scraping_attempts = 5

        if len(results) == 0:
            logger.info("No results found")
            return

        while helpers.is_size_of_output_allowed(self.max_size_of_folder) \
                and (
                self.browser.does_page_contain_element(show_more_button_locator) or len(results) > last_result_counter) \
                and scraping_attempts > 0:

            try:
                for result in results[last_result_counter:]:
                    self.extract_information_from_article(result)
                last_result_counter = len(results)
                self.scroll_and_click_more_articles(show_more_button_locator)
                results = self.load_more_article_results(results_locator)
                if len(results) > last_result_counter:
                    scraping_attempts = 5
            except Exception as e:
                logger.warning(f"Error while scraping information: {e}")
            finally:
                if last_result_counter == len(results):
                    scraping_attempts -= 1
                    logger.info(f"Scraping attempts left: {scraping_attempts}")
        logger.info(f"Amount of articles: {len(self.recolected_data)}")
        return self

    def generate_output(self) -> None:
        """Generate the output file with the information scraped"""
        self.compress_images()
        helpers.delete_images_in_folder()
        return self

    def compress_images(self) -> None:
        """Compress the images downloaded from the articles"""
        try:
            helpers.zip_images_in_folder()
        except Exception as e:
            logger.warning(f"Error while compressing images: {e}")

    def create_output_file(self) -> Files:
        """Creates an excel file with the information scraped"""
        lib = Files()  # Create modern format workbook with a path set.
        lib.create_workbook(path="./output/articles.xlsx", fmt="xlsx", sheet_name="articles")
        lib.append_rows_to_worksheet(
            [["date", "title", "description", "counts_of_search_phase", "picture_filename", "contains_money"]],
            "articles")
        lib.save_workbook()

        return lib

    def select_sections(self, sections: list = []) -> None:
        """ Select the sections to filter by

        :param sections: list of sections to select. If empty, all sections will be selected
        """
        selection_checkboxes = self.find_elements("//div[@data-testid='section']"
                                                  "//input[@data-testid='DropdownLabelCheckbox']")  # select all sections checkboxes

        for selection in selection_checkboxes:
            if self.contains_text(selection, sections):
                selection.click()  # click checkboxes if there is a match with sections list

    def contains_text(self, element, sections: list = []) -> bool:
        """Check if the element contains the given text
        :param element: element to check if it contains the text
        :param sections: list of sections to check if the element contains any of them
        :return: True if the element contains the text, False otherwise
        """
        value = element.get_attribute("value").split("|")
        return (element.get_attribute("value").split("|")[0] in sections) if len(value) > 0 else False

    def load_more_article_results(self, articles_locator: str) -> list:
        """Loads more articles results

        :param articles_locator: locator of the articles
        """
        return self.browser.find_elements(locator=articles_locator)

    def scroll_and_click_more_articles(self, show_more_locator: str) -> None:
        """Scrolls to the show more button and clicks it tot try to load more articles

        :param show_more_locator: locator of the show more button
        """
        if self.browser.does_page_contain_element(show_more_locator):
            self.browser.scroll_element_into_view(show_more_locator)
            self.click_button_on_page(show_more_locator)

    def extract_information_from_article(self, article) -> None:
        """
        Extracts the information from an article and appends it to the recolected_data list

        :param article: article from which the information will be extracted
        """
        date = selenium_helpers.get_attribute(self.find_element("./div/span", article), "aria-label")
        title = selenium_helpers.get_attribute(self.find_element("./div/div/div/a/h4", article), "innerHTML")
        description = selenium_helpers.get_attribute(self.find_element("./div/div/div/a/p", article), "innerHTML")
        img_src = selenium_helpers.get_attribute(self.find_element("./div/div//img", article), "src")

        self.download_article_images(img_src)  # Trying to download the image

        # Appending the information to the recolected_data list
        extracted_data = helpers.fill_data_information(date, title, description, img_src, self.search_phrase)
        self.append_data_to_excel(extracted_data)
        self.recolected_data.append(extracted_data)

    def download_article_images(self, img_src: str = None) -> str:
        """
        Download the image of an article
        :param img_src: source of the image
        """
        img_path = None
        try:
            if self.number_of_files_processed < self.max_amount_files:
                if img_src is None:
                    raise ImageCouldNotBeDownloadedError(message="Image source is None")
                img_path = helpers.download_image(img_src, helpers.get_filename(img_src))
                self.number_of_files_processed += 1
                logger.info(f"Image created at path: {img_path}")
            else:
                logger.info("Max amount of files reached. The image will not be downloaded.")
        except ImageCouldNotBeDownloadedError as e:
            logger.warning(f"Error while downloading image: {e}")
        finally:
            return img_path
    
    def append_data_to_excel(self, data: dict) -> None:
        """Appends the recolected data to the excel file

        :param data: data to append
        """
        self.excel_file.append_rows_to_worksheet(data)
        self.excel_file.save_workbook()
    