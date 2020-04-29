import os
import sys
import time
import codecs
import requests
import pyautogui
import pyperclip
import subprocess
import pandas as pd
import mammoth as d2h
from time import sleep
from numpy import ufunc
from datetime import date
from bs4 import BeautifulSoup
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
    user_agent = ''
    chrome_options = ''
    pdf = ''
    success = ''
    error = ''
    messages = ''
    sleep_time_page_load = 5

    def __init__(self, url, url_login, chrome_driver_path, sleep_time=2, user_agent=False):
        self.url = url
        self.url_login = url_login
        self.chrome_options = Options()
        self.chrome_driver_path = chrome_driver_path
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

    def send_keys_select_all(self, xpath=None, element_id=None, wait=False):
        if xpath:
            self.send_keys_exists_by_xpath(xpath, Keys.CONTROL + "a")
        elif element_id:
            self.send_keys_exists_by_id(element_id, Keys.CONTROL + "a")
        if wait:
            sleep(self.sleep_time)

    def send_backspace_by_xpath(self, xpath, times, wait=False):
        for i in range(0, times):
            self.send_keys_exists_by_xpath(xpath, Keys.BACK_SPACE)
        if wait:
            sleep(self.sleep_time)

    def paste_in_browser(self):
        action = ActionChains(self.browser)
        action.key_down(Keys.CONTROL)
        action.send_keys('v')
        action.key_up(Keys.CONTROL)
        action.perform()

    def send_keys_in_browser(self, msg):
        actions = ActionChains(self.browser)
        actions.send_keys(msg)
        actions.perform()

    def send_keys_exists_by_id(self, element_id, keys, error=None, success=None, wait=False, key_wait=None):
        try:
            if not key_wait:
                self.browser.find_element_by_id(element_id).send_keys(keys)
            else:
                for i in range(0, len(keys)):
                    self.browser.find_element_by_id(element_id).send_keys(keys[i])
                    sleep(key_wait)

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
        if success:
            self.success += "SUCCESS: " + success + "\r\n"
        return True

    def send_keys_exists_by_xpath(self, xpath, keys, error=None, success=None, wait=False):
        try:
            self.browser.find_element_by_xpath(xpath).send_keys(keys)
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

    def click_exists_by_xpath_elements(self, xpath, wait=False):
        elms = self.browser.find_elements_by_xpath(xpath)
        for elm in elms:
            try:
                elm.click()
            except selenium_exception.NoSuchElementException:
                continue
            except selenium_exception.ElementNotInteractableException:
                continue
            except (selenium_exception.WebDriverException, selenium_exception.ElementClickInterceptedException):
                try:
                    self.browser.execute_script("arguments[0].click();", elm)
                except selenium_exception:
                    continue
        if wait:
            sleep(self.sleep_time)

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
        blocks = {
            'heading': 'Heading',
            'paragraph': 'Paragraph',
            'list': 'List',
            'image': 'Image',
            'html': 'Custom HTML'
        }

        if block_name.lower() not in blocks:
            self.set_error('Enter a valid block name')
            return False

        err = 'Unable to add block :' + block_name
        cmp = block_name + ' Added'
        check_add = '//button[@type="button" and @aria-label="Add block"]'
        if self.click_exists_by_xpath(check_add, err):
            check_add = '//input[@type="search" and @placeholder="Search for a block"]'
            if self.send_keys_exists_by_xpath(check_add, block_name, wait=True):
                check_add = '//span[text()="' + blocks[block_name] + '"]/parent::button'
                if self.click_exists_by_xpath(check_add, err, cmp, True):
                    return True

    # General Block Setting
    def post_content_block_setting_general(self, html=False):
        if html:
            xpath_a = '//button[text()="Edit as HTML" and @type="button"]'
            if not self.check_exists_by_xpath(xpath_a):
                # Open General Settings Menu
                xpath_e = '//button[@type="button" and @aria-label="More options"]'
                err = "Unable to open General Settings Menu"
                self.click_exists_by_xpath(xpath_e, err, wait=True)
            err = "Unable to click Edit as html"
            self.click_exists_by_xpath(xpath_a, err, wait=True)

    # Heading Block Setting
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

    # Text Block Setting
    def post_content_block_setting_text_align(self, align='left'):
        list_align = [
            'left',
            'center',
            'right'
        ]
        if align.lower() in list_align:
            self.click_exists_by_xpath('//span[text()="Color settings"]/parent::button[@type="button"]', wait=True)
            xpath_a = '//button[@type="button" and text()="Align text ' + align.lower() + '"]'
            if not self.check_exists_by_xpath(xpath_a):
                # Open Align Menu
                xpath_e = '//button[@type="button" and @aria-label="Change text alignment"]'
                err = "Unable to open Text Align Menu"
                self.click_exists_by_xpath(xpath_e, err, wait=True)
            err = "Unable to align text " + align
            self.click_exists_by_xpath(xpath_a, err, wait=True)
        else:
            self.set_error("Invalid text alignment")

    def post_content_block_setting_color(self, text_color, bg_color=None):
        xpath_color = '(//button[text()="Custom color" and @type="button" and @aria-label="Custom color picker"])[1]'
        if not self.check_exists_by_xpath(xpath_color):
            # Expand Color Settings
            err = "Unable to expand Color Settings"
            self.click_exists_by_xpath('//span[text()="Color settings"]/parent::button[@type="button"]', err, wait=True)

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

    # Image Block Setting
    def post_content_block_setting_image_style(self, round_shape=False):
        xpath_s = '//div[@role="button" and @aria-label="Default"]'
        if not self.check_exists_by_xpath(xpath_s):
            # Expand Styles Settings
            err = "Unable to expand Styles Settings"
            self.click_exists_by_xpath('//button[text()="Styles" and @type="button"]', err, wait=True)
        if not round_shape:
            err = "Unable to set Default Style"
            self.click_exists_by_xpath(xpath_s, err, wait=True)
        else:
            xpath_s = '//div[@role="button" and @aria-label="Rounded"]'
            err = "Unable to set Round Style"
            self.click_exists_by_xpath(xpath_s, err, wait=True)

    # Image Block Setting
    def post_content_block_setting_image(self, alt_text=None, size=None, width=None, height=None, percentage=None):
        xpath_s = '//label[text()="Alt text (alternative text)"]/following-sibling::textarea'
        if not self.check_exists_by_xpath(xpath_s):
            # Expand Styles Settings
            err = "Unable to expand Image Settings"
            self.click_exists_by_xpath('//button[text()="Image settings" and @type="button"]', err, wait=True)

        if alt_text:
            err = "Unable to type alt text"
            self.send_keys_exists_by_xpath(xpath_s, alt_text, err, wait=True)

        if size:
            s_list = [
                "thumbnail",
                "medium",
                "large",
                "full",
            ]
            if size.lower() in s_list:
                xpath_s = '//label[text()="Image size"]/following-sibling::select/option[@value="' + size.lower() + '"]'
                err = "Unable to set size (option not available)"
                self.click_exists_by_xpath(xpath_s, err, wait=True)

        if width:
            xpath_s = '//label[text()="Width"]/following-sibling::input[@type="number"]'
            err = "Unable to set width"
            self.send_keys_select_all(xpath_s)
            self.send_keys_exists_by_xpath(xpath_s, width, err, wait=True)

        if height:
            xpath_s = '//label[text()="Height"]/following-sibling::input[@type="number"]'
            err = "Unable to set height"
            self.send_keys_select_all(xpath_s)
            self.send_keys_exists_by_xpath(xpath_s, height, err, wait=True)

        if percentage:
            p_list = {
                25: '25%',
                50: '50%',
                75: '75%',
                100: '100%',
            }
            if percentage in p_list:
                xpath_s = '//button[contains(text(), "' + str(percentage) + '")]'
                err = "Unable to set Percentage [xpath]: " + xpath_s
                self.click_exists_by_xpath(xpath_s, err, wait=True)

    # Image Block Setting
    def post_content_block_setting_image_align(self, align='left'):
        list_align = [
            'left',
            'center',
            'right'
        ]
        if align.lower() in list_align:
            xpath_a = '//button[@type="button" and text()="Align ' + align.lower() + '"]'
            if not self.check_exists_by_xpath(xpath_a):
                # Open Align Menu
                xpath_e = '//button[@type="button" and @aria-label="Change alignment"]'
                err = "Unable to open Align Menu"
                self.click_exists_by_xpath(xpath_e, err, wait=True)
            err = "Unable to align image " + align
            self.click_exists_by_xpath(xpath_a, err, wait=True)
        else:
            self.set_error("Invalid image alignment")

    # List Block Setting
    def post_content_block_setting_ordered_list(self, start=None, reverse=False):
        xpath_o = '//label[text()="Start value"]/following-sibling::input[@type="number"]'
        if not self.check_exists_by_xpath(xpath_o):
            # Expand Ordered list Settings
            err = "Unable to expand Styles Settings"
            self.click_exists_by_xpath('//button[text()="Ordered list settings" and @type="button"]', err, wait=True)
        if start:
            err = "Unable to set Start value"
            self.send_keys_exists_by_xpath(xpath_o, start, err, wait=True)
        if reverse:
            xpath_o = '//label[text()="Reverse list numbering"]'
            err = 'Unable to reverse list order'
            self.click_exists_by_xpath(xpath_o, err, wait=True)

    def post_content_block_heading(self, heading, style='default', align='left', text_color=None, html=False):
        if self.post_content_block_add('heading'):
            self.send_keys_in_browser(heading)
            if align != "left":
                self.post_content_block_setting_text_align(align)
            if html:
                self.post_content_block_setting_general(html)
            if style != 'default':
                self.post_content_block_setting_heading(style)

            if text_color:
                self.post_content_block_setting_color(text_color)

    def post_content_block_paragraph(self, paragraph, align='left', size=None, custom_size=None, drop_cap=False,
                                     text_color=None, bg_color=None, html=False):
        if self.post_content_block_add('paragraph'):
            self.send_keys_in_browser(paragraph)
            if align != "left":
                self.post_content_block_setting_text_align(align)

            if html:
                self.post_content_block_setting_general(html)

            if size or custom_size or drop_cap:
                self.post_content_block_setting_text(size, custom_size, drop_cap)

            if text_color or bg_color:
                self.post_content_block_setting_color(text_color, bg_color)

    def post_content_block_image(self, image_name=None, caption=None, image_url=None, align='left', round_shape=None,
                                 alt_text=None, size=None, width=None, height=None, percentage=None, html=False):
        check = False
        if self.post_content_block_add('image'):
            if image_name:
                err = "Unable to click Media Library Button"
                if self.click_exists_by_xpath('//button[text()="Media Library"]', err, wait=True):
                    if self.__media_search_and_select(image_name) is True:
                        check = True

            if image_url:
                err = "Unable to click Insert from URL Button"
                if self.click_exists_by_xpath('//button[text()="Insert from URL"]', err, wait=True):
                    self.send_keys_in_browser(image_url)
                    err = "Unable to click Apply Button"
                    if self.click_exists_by_xpath('//button[@type="submit" and @aria-label="Apply"]', err, wait=True):
                        size = None
                        check = True

            if check:
                if align != "left":
                    self.post_content_block_setting_image_align(align)

                if html:
                    self.post_content_block_setting_general(html)

                if caption:
                    xpath = '//figcaption[@role="textbox" and text()=""]'
                    err = "Unable to type caption"
                    if self.send_keys_exists_by_xpath(xpath, caption, err, wait=True):
                        if not percentage and not width and not height:
                            percentage = 100

                self.post_content_block_setting_image_style(round_shape)
                self.post_content_block_setting_image(alt_text, size, width, height, percentage)

    def post_content_block_list(self, list_text, ordered=False, start=None, reverse=False, separator='.'):
        if self.post_content_block_add('list'):
            if ordered:
                err = "Unable to Order list"
                xpath = '//button[@type="button" and @aria-label="Convert to ordered list"]'
                self.click_exists_by_xpath(xpath, err, wait=True)

            list_text = list_text.split(separator)
            del list_text[len(list_text) - 1]
            for i in range(0, len(list_text)):
                if list_text[i]:
                    if list_text[i][0] == " ":
                        list_text[i] = list_text[i].replace(" ", "", 1)
                self.send_keys_in_browser(list_text[i] + separator)
                if i == len(list_text) - 1:
                    break
                self.send_keys_in_browser(Keys.RETURN)

            if ordered and (start or reverse):
                self.post_content_block_setting_ordered_list(start, reverse)

    def post_content_block_html(self, html=None):
        self.post_content_block_add('html')
        if html:
            self.send_keys_in_browser(html)

    def post_content_from_file(self, file_path='', animation=False):
        list_ext = [
            'docx',
            'html'
        ]
        ext = file_path.split('.')
        if ext[-1].lower() in list_ext:
            self.post_content_block_add('html')
            if ext[-1].lower() == 'docx':
                html = self.docx_to_html(file_path)
            else:
                html = self.read_html(file_path)
            if not animation:
                pyperclip.copy(html)
                sleep(self.sleep_time)
                self.paste_in_browser()
            else:
                self.send_keys_in_browser(html)
        else:
            self.set_error("Invalid File Type")

    # TODO:
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
            err = "Unable to Expand Tags"
            self.click_exists_by_xpath('//button[text()="Tags"]', err, wait=True)

        # Add Tag
        tag_input = self.browser.find_element_by_xpath(check_tag)
        tag_input.send_keys(tag + Keys.RETURN)

    def __media_search_and_select(self, image_name, image_type="Select"):
        err = "Unable to type image name"
        self.send_keys_select_all(None, 'media-search-input')
        self.send_keys_exists_by_id('media-search-input', image_name, err, wait=True)

        sleep(self.sleep_time)
        err = "No image found"
        if not self.click_exists_by_xpath('(//li[@role="checkbox"])[1]', err):
            # xpath = '(//span[contains(@class, "media-modal-icon")]/parent::button[contains(@class, "media-modal-close")])[3]'
            xpath = '//span[contains(@class, "media-modal-icon")]/parent::button[contains(@class, "media-modal-close")]'
            err = "Unable to close Media Library"
            self.click_exists_by_xpath_elements(xpath, True)
            err = "Unable to click Media Library Button Again"
            if self.click_exists_by_xpath('//button[text()="Media Library"]', err, wait=True):
                if not self.click_exists_by_xpath('(//li[@role="checkbox"])[1]', err):
                    xpath = '(//span[contains(@class, "media-modal-icon")]/parent::button[contains(@class, "media-modal-close")])[3]'
                    xpath = '//span[contains(@class, "media-modal-icon")]/parent::button[contains(@class, "media-modal-close")]'
                    err = "Unable to close Media Library"
                    self.click_exists_by_xpath_elements(xpath, True)
                else:
                    err = "Unable to finish image selection"
                    if self.click_exists_by_xpath(
                            '//button[contains(@class, "media-button-select") and text()="' + image_type + '"]', err):
                        return True

        else:
            err = "Unable to finish image selection"
            if self.click_exists_by_xpath(
                    '//button[contains(@class, "media-button-select") and text()="' + image_type + '"]', err):
                return True

    def post_image(self, image_name):
        featured_img = '//button[text()="Set featured image"]'
        if not self.check_exists_by_xpath(featured_img):
            # Expand Featured Image
            err = "Unable to Expand Featured Image"
            self.click_exists_by_xpath('//button[text()="Featured image"]', err)

        err = "Unable to click Set featured image"
        self.click_exists_by_xpath('//button[text()="Set featured image"]', err, wait=True)

        self.__media_search_and_select(image_name, "Set featured image")

        # err = "Unable to type image name"
        # self.send_keys_exists_by_id('media-search-input', image_name, err)
        #
        # sleep(self.sleep_time + 3)
        # err = "Unable to click searched image name"
        # self.click_exists_by_xpath('(//li[@role="checkbox"])[1]', err)
        #
        # err = "Unable to finish featured image selection"
        # self.click_exists_by_xpath('//button[contains(@class, "media-button-select") and text()="Set featured image"]',
        #                            err)

    def post_excerpt(self, excerpt):
        check_excerpt = '//label[text()="Write an excerpt (optional)"]/following-sibling::textarea'
        if not self.check_exists_by_xpath(check_excerpt):
            # Expand Excerpt
            err = "Unable to Expand Excerpt Setting"
            self.click_exists_by_xpath('//button[text()="Excerpt"]', err, wait=True)

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
        sleep(self.sleep_time)
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

    def read_html(self, html_path, full=False):
        f = codecs.open(html_path, 'r')
        html = f.read()
        soup = BeautifulSoup(html, 'html.parser')
        if not full:
            return soup.body.prettify()
        else:
            return soup.prettify()

    def docx_to_html(self, docx_path):
        with open(docx_path, "rb") as docx_file:
            result = d2h.convert_to_html(docx_file)
            html = result.value
            self.messages = result.messages
        return html

    # Junk
    def post_from_pdf(self, pdf_path):
        # self.send_keys_in_browser(Keys.CONTROL + 't')
        # ActionChains(self.browser).send_keys(Keys.COMMAND, "t").perform()
        # self.pdf = self.browser = webdriver.Chrome(executable_path=self.chrome_driver_path,
        #                                            chrome_options=self.chrome_options)
        browser = self.browser.window_handles[0]
        pyautogui.hotkey('ctrl', 't')
        sleep(self.sleep_time)
        pdf = self.browser.window_handles[1]
        self.browser.switch_to.window(pdf)
        self.browser.get(pdf_path)
        # self.browser.get('file:///' + pdf_path)
        # self.send_keys_in_browser(Keys.CONTROL + 'a')
        # ActionChains(self.pdf.find_element_by_tag_name('body')).send_keys(Keys.CONTROL, "a").perform()
        pyautogui.click(clicks=3)
        sleep(self.sleep_time)
        pyautogui.hotkey('ctrl', 'a')
        # self.send_keys_in_browser(Keys.CONTROL + 'c')
        sleep(self.sleep_time)
        # ActionChains(self.pdf).send_keys(Keys.CONTROL, "c").perform()
        pyautogui.hotkey('ctrl', 'c')
        sleep(self.sleep_time)
        # self.send_keys_in_browser(Keys.CONTROL + 'w')
        # self.pdf.close()
        # ActionChains(self.pdf).send_keys(Keys.CONTROL, "w").perform()
        pyautogui.hotkey('ctrl', 'w')
        self.browser.switch_to.window(browser)
        sleep(self.sleep_time)
        self.post_content_block_paragraph('')
        pyautogui.hotkey('ctrl', 'v')

    def post_new(self, title, category=None, tag=None, image_name=None, excerpt=None, docx_path=None):
        self.browser.get(self.url + "/wp-admin/post-new.php")
        sleep(self.sleep_time_page_load)

        xpath = '//button[@type="button" and @aria-label="Close dialog"]'
        if self.check_exists_by_xpath(xpath):
            err = "Unable to close tutorial pop up"
            self.click_exists_by_xpath(xpath, err)

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

        if docx_path:
            sleep(self.sleep_time)
            self.post_content_block_html(None, docx_path)
