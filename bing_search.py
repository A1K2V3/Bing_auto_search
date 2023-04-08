import pathlib
import random_word
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.microsoft import EdgeChromiumDriverManager


class BingSearch:

    def __init__(self):

        self.options = self.configure_options()
        self.service = Service(EdgeChromiumDriverManager().install())
        self.driver = None


    @staticmethod
    def configure_options():

        # Create /usr_data directory is not alraedy exists
        directory_path = pathlib.Path('./usr_data')
        directory_path.mkdir(parents=True, exist_ok=True)

        # configure options
        options = Options()
        options.use_chromium = True
        options.add_argument("--headless=True")
        options.add_argument("--start-maximized")
        options.add_argument(r"user-data-dir=./usr_data")

        return options

    def configure_driver(self, device):
        if device == "mobile":
            self.options.add_argument("--user-agent=Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Mobile Safari/537.36")

        self.driver = webdriver.Edge(service=self.service, options=self.options)

        if device == "mobile":
            self.driver.execute_cdp_cmd("Emulation.setDeviceMetricsOverride", {
                "width": 393,
                "height": 851,
                "deviceScaleFactor": 1,
                "mobile": True,
                "fitWindow": True
            })


    def search(self, device="desktop", no_of_search=30):

        print(f"Configuring driver for {device} search")
        self.configure_driver(device)

        # open bing home page
        self.driver.get("https://www.bing.com/")
        self.driver.implicitly_wait(5)

        random_word_generator = random_word.RandomWords()

        for index in range(no_of_search):

            word = random_word_generator.get_random_word()

            # seaching the word in bing.com
            bing_search_box = self.driver.find_element(By.NAME, "q")
            bing_search_box.clear()
            bing_search_box.send_keys(word)
            bing_search_box.submit()

            self.driver.implicitly_wait(5)

            # Print the search term in terminal
            print(f"device: {device}, index: {index+1}, word: {word}")

            # press back and start another search
            self.driver.back()

        # Quit the driver
        self.driver.quit()


if __name__ == "__main__":
    bing_search = BingSearch()
    bing_search.search()
    bing_search.search("mobile")
