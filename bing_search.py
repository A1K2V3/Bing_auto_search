import pathlib
import random_word
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.microsoft import EdgeChromiumDriverManager


class BingSearch:

    def __init__(self):
        directory_path = pathlib.Path('./usr_data')
        if not directory_path.exists():
            directory_path.mkdir(parents=True, exist_ok=True)
        self.options = Options()
        self.options.use_chromium = True
        self.options.add_argument("--headless=True")
        self.options.add_argument("--start-maximized")
        self.options.add_argument(r"user-data-dir=./usr_data")
        self.service = Service(EdgeChromiumDriverManager().install())
        self.driver = None

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

        for index, words in enumerate(random_word_generator.get_random_word() for _ in range(no_of_search)):
            bing_search_box = self.driver.find_element(By.NAME, "q")
            bing_search_box.clear()
            bing_search_box.send_keys(words)
            bing_search_box.submit()
            self.driver.implicitly_wait(5)

            # Print the search term in terminal
            print(f"device: {device}, index: {index+1}, word: {words}")

            # press back and start another search
            self.driver.back()

        # Quit the driver
        self.driver.quit()


BingSearch().search()
BingSearch().search(device="mobile")
