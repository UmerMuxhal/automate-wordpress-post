import os
import time
import requests
import subprocess
import pandas as pd
from time import sleep
from datetime import date
from bs4 import BeautifulSoup
from selenium import webdriver
from lxml.html import fromstring
from random_user_agent.user_agent import UserAgent
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from random_user_agent.params import SoftwareName, OperatingSystem


class Wordpress:
    url = ''
    url_login = ''
    user_agent = ''

    def __init__(self, url, url_login, chrome_driver_path, sleep_time=2, user_agent=False):
        self.url = url
        self.url_login = url_login
        self.chrome_options = Options()
        if user_agent:
            self.user_agent_generator()
            self.chrome_options.add_argument(f'user-agent={self.user_agent}')
        self.browser = webdriver.Chrome(executable_path=chrome_driver_path, chrome_options=self.chrome_options)
        self.sleep_time = sleep_time

    def chrome_options(self, window_size=None, gpu=False, user_agent=True, info_bars=False, extensions=False,
                       notification=False):
        if window_size:
            self.chrome_options.add_argument(f'--window-size={window_size[0]},{window_size[1]}')
        if not gpu:
            self.chrome_options.add_argument('--disable-gpu')
        if user_agent:
            self.user_agent_generator()
            self.chrome_options.add_argument(f'user-agent={self.user_agent}')
        if not info_bars:
            self.chrome_options.add_argument("--disable-infobars")
        if not extensions:
            self.chrome_options.add_argument("--disable-extensions")
        if not notification:
            self.chrome_options.add_experimental_option("prefs", {
                "profile.default_content_setting_values.notifications": 2
            })
        self.browser = webdriver.Chrome(chrome_options=self.chrome_options)

    def user_agent_generator(self):
        software_names = [SoftwareName.CHROME.value]
        operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
        user_agent_rotate = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)
        self.user_agent = user_agent_rotate.get_random_user_agent()

    def maximize_window(self):
        self.browser.maximize_window()

    def check_exists_by_id(self, element_id):
        try:
            self.browser.find_element_by_id(element_id)
        except NoSuchElementException:
            return False
        return True

    def check_exists_by_xpath(self, xpath):
        try:
            self.browser.find_element_by_xpath(xpath)
        except NoSuchElementException:
            return False
        return True

    def wp_login(self, email, password):
        self.browser.get(self.url_login)

        sleep(self.sleep_time)
        self.browser.find_element_by_id('user_login').send_keys(email)

        sleep(self.sleep_time)
        self.browser.find_element_by_id('user_pass').send_keys(password)

        self.browser.find_element_by_id('wp-submit').click()

    def open_page_posts(self):
        self.browser.get(self.url + "/wp-admin/edit.php")

    def post_title(self, title):
        if self.check_exists_by_id("post-title-0"):
            self.browser.find_element_by_id("post-title-0").send_keys(title)
        else:
            print("FAILURE: Unable to write post title!")

    def post_category(self, category):
        check_cat = '//button[text()="Add New Category"]'
        if not self.check_exists_by_xpath(check_cat):
            # Expand Categories
            self.browser.find_element_by_xpath('//button[text()="Categories"]').click()

        check_cat = "//label[text()='" + category + "']"
        if not self.check_exists_by_xpath(check_cat):
            # Add if category does not exist
            self.browser.find_element_by_xpath('//button[text()="Add New Category"]').click()

            self.browser.find_element_by_xpath(
                "//*[@id='editor-post-taxonomies__hierarchical-terms-input-0']").send_keys(category)
            self.browser.find_element_by_xpath('//button[@type="submit" and text()="Add New Category"]').click()
        else:
            # Select category
            self.browser.find_element_by_xpath(check_cat).click()

    def post_image(self, image_name):
        featured_img = '//button[text()="Set featured image"]'
        if not self.check_exists_by_xpath(featured_img):
            # Expand Featured Image
            self.browser.find_element_by_xpath('//button[text()="Featured Image"]').click()

        self.browser.find_element_by_xpath('//button[text()="Set featured image"]').click()

        sleep(self.sleep_time)
        self.browser.find_element_by_id('media-search-input').send_keys(image_name)

        sleep(self.sleep_time + 3)
        self.browser.find_element_by_xpath('//li[@role="checkbox"]').click()

        self.browser.find_element_by_xpath(
            '//button[contains(@class, "media-button-select") and text()="Set featured image"]').click()

    def post_new(self, title, category=None, image_name=None):
        self.browser.get(self.url + "/wp-admin/post-new.php")

        # Add title
        self.post_title(title)

        sleep(self.sleep_time)
        if category:
            self.post_category(category)

        sleep(self.sleep_time)
        if image_name:
            self.post_image(image_name)
