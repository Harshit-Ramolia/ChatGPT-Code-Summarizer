from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from dataclasses import dataclass
import markdownify
import time
import random
import pyperclip


@dataclass
class Scrapper:
    driver: webdriver = None
    isRunning: bool = False
    counter: int = 2

    def start(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option(
            "excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        driver = webdriver.Chrome(options=options)
        driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        x = random.random()
        time.sleep(x)
        driver.get("https://www.google.com")
        self.isRunning = True
        self.driver = driver

    def __fill_textbox(self, textBox, input):
        pyperclip.copy(input)
        textBox.click()
        x = random.random()
        time.sleep(x)
        textBox.send_keys(Keys.CONTROL+"v")
        x = random.random()
        time.sleep(x)
        textBox.send_keys(Keys.ENTER)

    def chatGPT(self, input):
        
        for _ in range(2):
            driver = self.driver
            textBox = driver.find_element(
                by=By.XPATH, value="/html/body/div[1]/div[2]/div[2]/main/div[2]/form/div/div[2]/textarea")
            self.__fill_textbox(textBox, input)
            old = -1
            while True:
                try:
                    response = driver.find_element(
                        by=By.XPATH, value=f"/html/body/div[1]/div[2]/div[2]/main/div[1]/div/div/div/div[{self.counter}]/div/div[2]/div[1]/div/div")
                    if len(response.text) > old:
                        old = len(response.text)
                        time.sleep(5)
                    else:
                        self.counter += 2
                        break
                except:
                    time.sleep(1)

            if (len(response.text)>200):
                break

        return markdownify.markdownify(response.get_attribute("outerHTML"))
