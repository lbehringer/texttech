import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

numbeo_urls = []


class Selenium(numbeo_urls):
    driver = webdriver.Chrome('path/to/chromedriver')
    for i in numbeo_urls:
        driver.get(numbeo_urls[i])
        if
    close_button = driver.find_element_by_xpath(
        '//button[@class="ui-button ui-widget ui-state-default ui-corner-all ui-button-icon-only ui-dialog-titlebar-close"]')
    close_button.click()
    time.sleep(1)
