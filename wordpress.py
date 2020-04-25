import os
import time
import requests
import subprocess
import pandas as pd
from time import sleep
from datetime import date
from bs4 import BeautifulSoup
from numpy import ufunc
from selenium import webdriver
from lxml.html import fromstring
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from random_user_agent.user_agent import UserAgent
from selenium.webdriver.chrome.options import Options
import selenium.common.exceptions as selenium_exception
from selenium.common.exceptions import NoSuchElementException
from random_user_agent.params import SoftwareName, OperatingSystem


class Wordpress:
    url = ''
    url_login = ''
    user_agent = ''
    chrome_options = ''
    success = ''
    error = ''
    sleep_time_page_load = 5

    def __init__(self, url, url_login, chrome_driver_path, sleep_time=2, user_agent=False):
        self.url = url
        self.url_login = url_login
        self.chrome_options = Options()
        if user_agent:
            self.user_agent_generator()
            self.chrome_options.add_argument(f'user-agent={self.user_agent}')
        self.browser = webdriver.Chrome(executable_path=chrome_driver_path, chrome_options=self.chrome_options)
        self.sleep_time = sleep_time

    def chrome_options_edit(self, window_size=None, gpu=False, user_agent=True, info_bars=False, extensions=False,
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

    def close(self):
        self.browser.close()

    def set_error(self, error):
        self.error += "ERROR: " + error + "\r\n"

    def get_errors(self):
        return "Errors: \n" + self.error

    def get_completed(self):
        return "Completed Tasks: \n" + self.success

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

    def send_backspace_by_xpath(self, xpath, times):
        for i in range(1, times):
            self.send_keys_exists_by_xpath(xpath, Keys.BACK_SPACE)

    def send_keys_in_browser(self, msg):
        actions = ActionChains(self.browser)
        actions.send_keys(msg)
        actions.perform()

    def send_keys_exists_by_id(self, element_id, keys, error=None, success=None, wait=False):
        try:
            self.browser.find_element_by_id(element_id).send_keys(keys)
            if wait:
                sleep(self.sleep_time)
        except NoSuchElementException:
            if error:
                self.error += "ERROR: " + error + "\r\n"
            return False
        if success:
            self.success += "SUCCESS: " + success + "\r\n"
        return True

    def send_keys_exists_by_xpath(self, xpath, keys, error=None, success=None, wait=False):
        try:
            self.browser.find_element_by_xpath(xpath).send_keys(keys)
            if wait:
                sleep(self.sleep_time)
        except NoSuchElementException:
            if error:
                self.error += "ERROR: " + error + "\r\n"
            return False
        if success:
            self.success += "SUCCESS: " + success + "\r\n"
        return True

    def click_exists_by_xpath(self, xpath, error=None, success=None, wait=False):
        try:
            self.browser.find_element_by_xpath(xpath).click()
            if wait:
                sleep(self.sleep_time)
        except selenium_exception.NoSuchElementException:
            if error:
                self.error += "ERROR: " + error + " [Element Not Found]\r\n"
            return False
        except selenium_exception.ElementNotInteractableException:
            if error:
                self.error += "ERROR: " + error + " [Element Not Interactable]\r\n"
            return False
        except (selenium_exception.WebDriverException, selenium_exception.ElementClickInterceptedException):
            try:
                btn = self.browser.find_element_by_xpath(xpath)
                self.browser.execute_script("arguments[0].click();", btn)
                if wait:
                    sleep(self.sleep_time)
            except selenium_exception:
                if error:
                    self.error += "ERROR: " + error + "\r\n"
                return False
        if success:
            self.success += "SUCCESS: " + success + "\r\n"
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
            self.set_error("Unable to type post title!")

    # After post published
    def post_url(self, url):
        self.post_document_setting_open()
        xpath_u = '//label[text()="URL Slug"]/following-sibling::input[@type="text"]'
        if not self.check_exists_by_xpath(xpath_u):
            # Expand Heading Settings
            err = 'Unable to expand Permalink'
            self.click_exists_by_xpath('//button[@type="button" and text()="Permalink"]', err, wait=True)

        err = "Unable to type post url"
        self.send_keys_exists_by_xpath(xpath_u, url, err, wait=True)

    def post_content_use_default_editor(self, xpath='//button[text()="Use Default Editor"]'):
        err = 'Unable to use default editor'
        self.click_exists_by_xpath(xpath, err)
        sleep(self.sleep_time)

    def post_content_block_setting_open(self):
        xpath = '//button[@type="button" and @aria-label="Block (selected)"]'
        if self.check_exists_by_xpath(xpath):
            return True

        xpath = '//button[@type="button" and @aria-label="Block"]'
        err = "Unable to open Block setting"
        self.click_exists_by_xpath(xpath, err, wait=True)

    def post_content_block_add(self, block_name):
        blocks = ['heading', 'paragraph', 'list', 'image']
        if block_name.lower() not in blocks:
            self.set_error('Enter a valid block name')
            return False

        err = 'Unable to add block :' + block_name
        cmp = block_name + ' Added'
        check_add = '//button[@type="button" and @aria-label="Add block"]'
        self.click_exists_by_xpath(check_add)
        self.send_keys_exists_by_xpath('//input[@type="search" and @placeholder="Search for a block"]', block_name)
        sleep(self.sleep_time)
        self.click_exists_by_xpath('//span[text()="' + block_name.capitalize() + '"]/parent::button', err, cmp)
        sleep(self.sleep_time)

    def post_content_block_setting_heading(self, style):
        head = {
            'h1': 'Heading 1',
            'h2': 'Heading 2',
            'h3': 'Heading 3',
            'h4': 'Heading 4',
            'h5': 'Heading 5',
            'h6': 'Heading 6'
        }
        check_h = '//button[@type="button" and @aria-label="' + head[style] + '"]'
        if not self.check_exists_by_xpath(check_h):
            # Expand Heading Settings
            err = 'Unable to expand Heading Settings'
            self.click_exists_by_xpath('//button[@type="button" and text()="Heading Settings"]', err)
            sleep(self.sleep_time)

        err = 'Invalid Heading style: [' + style + ']'
        self.click_exists_by_xpath(check_h, err)

    def post_content_block_setting_text(self, size=None, custom_size=None, drop_cap=False):
        xpath_text = '//label[text()="Custom"]/following-sibling::input[@type="number"]'
        if not self.check_exists_by_xpath(xpath_text):
            # Expand Text Settings
            self.click_exists_by_xpath('//button[text()="Text Settings" and @type="button"]')
            sleep(self.sleep_time)

        if custom_size:
            self.send_keys_exists_by_xpath(xpath_text, custom_size)

        if size:
            size_list = {
                'default': 14,
                'small': 13,
                'normal': 16,
                'medium': 20,
                'large': 36,
                'huge': 48
            }
            if size.lower() in size_list:
                err = 'Unable to choose text size: ' + size
                self.send_keys_exists_by_xpath(xpath_text, size_list[size], err)
                sleep(self.sleep_time)
            else:
                self.set_error('Invalid text size: ' + size)

        if drop_cap:
            xpath_text = '//p[text()="Toggle to show a large initial letter."]/preceding-sibling::div//input[@type="checkbox"]'
            err = 'Unable to use Drop Cap'
            self.click_exists_by_xpath(xpath_text, err)

    def post_content_block_setting_color(self, text_color, bg_color=None):
        xpath_color = '(//button[text()="Custom color" and @type="button" and @aria-label="Custom color picker"])[1]'
        if not self.check_exists_by_xpath(xpath_color):
            # Expand Color Settings
            err = "Unable to expand Color Settings"
            self.click_exists_by_xpath('//span[text()="Color settings"]/parent::button[@type="button"]', err)
            sleep(self.sleep_time)

        err = "Unable to set text color"
        if self.click_exists_by_xpath(xpath_color, err):
            xpath_color = '//label[text()="Color value in hexadecimal"]/following-sibling::input[@type="text"]'
            sleep(self.sleep_time)
            self.send_backspace_by_xpath(xpath_color, 8)
            err = "Unable to type text color"
            self.send_keys_exists_by_xpath(xpath_color, text_color, err)

        if bg_color:
            xpath_color = '(//button[@type="button" and @aria-label="Custom color picker" and text()="Custom color"])[2]'
            err = "Unable to set background color"
            if self.click_exists_by_xpath(xpath_color, err):
                xpath_color = '//label[text()="Color value in hexadecimal"]/following-sibling::input[@type="text"]'
                sleep(self.sleep_time)
                self.send_backspace_by_xpath(xpath_color, 8)
                err = "Unable to type background color"
                self.send_keys_exists_by_xpath(xpath_color, bg_color, err)

    def post_content_block_heading(self, heading, style='default', text_color=None):
        self.post_content_block_add('heading')
        self.send_keys_in_browser(heading)
        if style != 'default':
            self.post_content_block_setting_heading(style)

        if text_color:
            self.post_content_block_setting_color(text_color)

    def post_content_block_paragraph(self, paragraph, size=None, custom_size=None, drop_cap=False, text_color=None,
                                     bg_color=None):
        self.post_content_block_add('paragraph')
        self.send_keys_in_browser(paragraph)

        if size or custom_size or drop_cap:
            self.post_content_block_setting_text(size, custom_size, drop_cap)

        if text_color or bg_color:
            self.post_content_block_setting_color(text_color, bg_color)

    def post_content(self, data_dictionary):
        element_discus = '//span[text()="Visibility"]'
        if not self.check_exists_by_xpath(element_discus):
            # Expand Excerpt
            self.browser.find_element_by_xpath('//button[text()="Status & Visibility"]').click()
            sleep(self.sleep_time)

            element_discus = '//label[text()="Stick to the top of the blog"]/preceding-sibling::span/input[@type="checkbox"]'
            err = 'Unable to interact with Stick on Top of the blog(Status & Visibility)!'
            self.click_exists_by_xpath(element_discus, err)

            element_discus = '//label[text()="Pending Review"]/preceding-sibling::span/input[@type="checkbox"]'
            err = 'Unable to interact with Pending Review(Status & Visibility)!'
            self.click_exists_by_xpath(element_discus, err)

            check = True
            err = 'Unable to interact with Visibility(Status & Visibility)!'
            if not self.click_exists_by_xpath('//button[text()="Public"]'):
                if not self.click_exists_by_xpath('//button[text()="Private"]'):
                    check = self.click_exists_by_xpath('//button[text()="Password Protected"]', err)

            if check:
                sleep(self.sleep_time)

                self.click_exists_by_xpath('//input[@type="radio" and @value="public"]')

                self.click_exists_by_xpath('//input[@type="radio" and @value="private"]')
                sleep(self.sleep_time)
                alert_obj = self.browser.switch_to.alert
                alert_obj.accept()
                self.browser.switch_to.default_content()

                self.click_exists_by_xpath('//input[@type="radio" and @value="password"]')
                xpath_pass = '//input[@type="text" and @placeholder="Use a secure password"]'
                err = 'Unable to type password(Status & Visibility)!'

    def post_document_setting_open(self):
        xpath = '//button[@type="button" and @aria-label="Document (selected)"]'
        if self.check_exists_by_xpath(xpath):
            return True

        xpath = '//button[@type="button" and @aria-label="Document"]'
        err = "Unable to open Document setting"
        self.click_exists_by_xpath(xpath, err, wait=True)

    def post_status(self, visibility='public', password=None, stick_top=False, pending_review=False):
        element_discus = '//span[text()="Visibility"]'
        if not self.check_exists_by_xpath(element_discus):
            # Expand Excerpt
            self.browser.find_element_by_xpath('//button[text()="Status & Visibility"]').click()
            sleep(self.sleep_time)

        # Check stick on top
        if stick_top:
            element_discus = '//label[text()="Stick to the top of the blog"]/preceding-sibling::span/input[@type="checkbox"]'
            err = 'Unable to interact with Stick on Top of the blog(Status & Visibility)!'
            self.click_exists_by_xpath(element_discus, err)

        # Check pending review
        if pending_review:
            element_discus = '//label[text()="Pending review"]/preceding-sibling::span/input[@type="checkbox"]'
            err = 'Unable to interact with Pending Review(Status & Visibility)!'
            self.click_exists_by_xpath(element_discus, err)

        if visibility:
            check = True
            err = 'Unable to interact with Visibility(Status & Visibility)!'
            if not self.click_exists_by_xpath('//button[text()="Public"]'):
                if not self.click_exists_by_xpath('//button[text()="Private"]'):
                    check = self.click_exists_by_xpath('//button[text()="Password Protected"]', err)

            if check:
                sleep(self.sleep_time)
                if visibility.lower() == 'public':
                    self.click_exists_by_xpath('//input[@type="radio" and @value="public"]')
                elif visibility.lower() == 'private':
                    self.click_exists_by_xpath('//input[@type="radio" and @value="private"]')
                    sleep(self.sleep_time)
                    alert_obj = self.browser.switch_to.alert
                    alert_obj.accept()
                    self.browser.switch_to.default_content()
                    sleep(self.sleep_time)
                elif password and visibility.lower() == 'password':
                    self.click_exists_by_xpath('//input[@type="radio" and @value="password"]')
                    xpath_pass = '//input[@type="text" and @placeholder="Use a secure password"]'
                    err = 'Unable to type password(Status & Visibility)!'
                    self.send_keys_exists_by_xpath(xpath_pass, password, err)
                    sleep(self.sleep_time)

    # After post published
    def post_format(self, formatting='standard'):
        self.post_document_setting_open()
        format_list = ['standard', 'gallery', 'link', 'quote', 'video', 'audio']
        if formatting.lower() in format_list:
            xpath_ = '//label[text()="Post Format"]/following-sibling::div//select/option[@value="' + formatting + '"]'
            err = "Unable to select post format"
            self.click_exists_by_xpath(xpath_, err, wait=True)

    def post_category(self, category):
        err = 'Unable to expand Categories Panel(Categories)!'
        if self.click_exists_by_xpath('//button[text()="Categories"]', err):
            # Expand Categories
            sleep(self.sleep_time)

        check_cat = "//label[text()='" + category + "']"
        if not self.check_exists_by_xpath(check_cat):
            # Add if category does not exist
            err = "Unable to click Add New Category 1"
            self.click_exists_by_xpath('//button[text()="Add New Category"]', err)

            err = "Unable to type Category name"
            self.send_keys_exists_by_xpath("//*[@id='editor-post-taxonomies__hierarchical-terms-input-0']", category,
                                           err)

            err = "Unable to click Add New Category 2"
            self.click_exists_by_xpath('//button[@type="submit" and text()="Add New Category"]', err)
        else:
            # Select category
            err = "Unable to Select category"
            self.click_exists_by_xpath(check_cat, err)

    def post_tag(self, tag):
        check_tag = '//label[text()="Add New Tag"]/following-sibling::div/child::input'
        if not self.check_exists_by_xpath(check_tag):
            # Expand Tags
            self.browser.find_element_by_xpath('//button[text()="Tags"]').click()

        # Add Tag
        tag_input = self.browser.find_element_by_xpath(check_tag)
        tag_input.send_keys(tag + Keys.RETURN)

    def post_image(self, image_name):
        featured_img = '//button[text()="Set featured image"]'
        if not self.check_exists_by_xpath(featured_img):
            # Expand Featured Image
            err = "Unable to Expand Featured Image"
            self.click_exists_by_xpath('//button[text()="Featured image"]', err)

        err = "Unable to click Set featured image"
        self.click_exists_by_xpath('//button[text()="Set featured image"]', err)

        sleep(self.sleep_time)
        err = "Unable to type image name"
        self.send_keys_exists_by_id('media-search-input', image_name, err)

        sleep(self.sleep_time + 3)
        err = "Unable to click searched image name"
        self.click_exists_by_xpath('(//li[@role="checkbox"])[1]', err)

        err = "Unable to finish featured image selection"
        self.click_exists_by_xpath('//button[contains(@class, "media-button-select") and text()="Set featured image"]',
                                   err)

    def post_excerpt(self, excerpt):
        check_excerpt = '//label[text()="Write an excerpt (optional)"]/following-sibling::textarea'
        if not self.check_exists_by_xpath(check_excerpt):
            # Expand Excerpt
            self.browser.find_element_by_xpath('//button[text()="Excerpt"]').click()

        # Add Excerpt
        self.browser.find_element_by_xpath(check_excerpt).send_keys(excerpt)

    def post_discussion(self, comments=True, traceback=True):
        element_discus = '//label[text()="Allow comments"]'
        if not self.check_exists_by_xpath(element_discus):
            # Expand Discussion
            err = "Unable to Expand Discussion"
            self.click_exists_by_xpath('//button[text()="Discussion"]', err)

        # Uncheck comments
        if not comments:
            err = "Unable to Allow pingbacks & trackbacks"
            self.click_exists_by_xpath(element_discus, err)
        # Uncheck traceback
        if not traceback:
            element_discus = '//label[text()="Allow pingbacks & trackbacks"]'
            err = "Unable to Allow pingbacks & trackbacks"
            self.click_exists_by_xpath(element_discus, err)

    def post_save_draft(self):
        xpath_save = '//button[text()="Publish…" and @aria-disabled="true"]'
        if self.check_exists_by_xpath(xpath_save):
            sleep(self.sleep_time)
        xpath_save = '//button[text()="Save Draft"]'
        if not self.check_exists_by_xpath(xpath_save):
            xpath_save = '//button[text()="Save as Pending"]'
            err = "Unable to click Save as Pending Button"
            self.click_exists_by_xpath(xpath_save, err, wait=True)
            sleep(self.sleep_time)
        else:
            err = "Unable to click Save Draft Button"
            if self.click_exists_by_xpath(xpath_save, err, wait=True):
                sleep(self.sleep_time)

    def post_switch_to_draft(self):
        xpath_d = '//button[text()="Switch to draft"]'
        err = "Unable to click Switch to Draft Button"
        if self.click_exists_by_xpath(xpath_d, err, wait=True):
            alert_obj = self.browser.switch_to.alert
            alert_obj.accept()
            self.browser.switch_to.default_content()
            sleep(self.sleep_time)

    def post_publish(self):
        xpath_p = '//button[text()="Publish…" and @aria-disabled="true"]'
        if self.check_exists_by_xpath(xpath_p):
            sleep(self.sleep_time)
        xpath_p = '//button[text()="Publish…"]'
        err = "Unable to click Publish… Button (1)"
        if self.click_exists_by_xpath(xpath_p, err, wait=True):
            xpath_p = '//button[text()="Publish"]'
            err = "Unable to click Publish Button (2)"
            if self.click_exists_by_xpath(xpath_p, err, wait=True):
                err = "Unable to close panel after Publish"
                xpath_p = '//button[@aria-label="Close panel" and @type="button"]'
                self.click_exists_by_xpath(xpath_p, err, wait=True)

    def post_update(self):
        xpath_u = '//button[text()="Update"]'
        err = "Unable to click Update Button"
        if self.click_exists_by_xpath(xpath_u, err, wait=True):
            sleep(self.sleep_time)

    def post_new(self, title, category=None, tag=None, image_name=None, excerpt=None):
        self.browser.get(self.url + "/wp-admin/post-new.php")
        sleep(self.sleep_time_page_load)

        self.post_content_use_default_editor()

        # Add title
        self.post_title(title)

        if category:
            sleep(self.sleep_time)
            self.post_category(category)

        if tag:
            sleep(self.sleep_time)
            self.post_tag(tag)

        if image_name:
            sleep(self.sleep_time)
            self.post_image(image_name)

        if excerpt:
            sleep(self.sleep_time)
            self.post_excerpt(excerpt)
