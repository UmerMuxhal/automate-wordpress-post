import codecs
from time import sleep
import mammoth as d2h
import pyperclip
import selenium.common.exceptions as selenium_exception
from bs4 import BeautifulSoup
from random_user_agent.params import SoftwareName, OperatingSystem
from random_user_agent.user_agent import UserAgent
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys


class WordPress:
    """ This class opens a chrome window and use it for automating post on a WordPress site.
    Automate WordPress Block Editor. Blocks that can be used are: Heading, Paragraph, Image, List and Custom HTML.
    Each block can be customized.
    Add post using docx file or html file.

    """

    success = ''
    error = ''
    messages = ''
    sleep_time_page_load = 5

    def __init__(self, site_url, login_url, chrome_driver_path, sleep_time=2, user_agent=False):
        """Creates a new instance of chrome for a WordPress site

        :type site_url: str
        :type login_url: str
        :type chrome_driver_path: str
        :type sleep_time: int
        :type user_agent: bool
        :param site_url: Home address of WordPress site.
        :param login_url: Login address of WordPress site.
        :param chrome_driver_path: Path of chrome webdriver for selenium
        :param sleep_time: Wait time (seconds) between execution of different tasks (default is 2)
        :param user_agent: Use random User-Agent for chrome (default is False)

        Example
        ----
        wp = WordPress('mysite.com', 'mysite.com/wp-admin', 'path-to-chromedriver', 3, True)
        """

        self.site_url = site_url
        self.login_url = login_url
        self.chrome_options = Options()
        self.chrome_driver_path = chrome_driver_path
        if user_agent:
            self.user_agent = self.__user_agent_generator()
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
            self.__user_agent_generator()
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

    def __user_agent_generator(self):
        software_names = [SoftwareName.CHROME.value]
        operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
        user_agent_rotate = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)
        return user_agent_rotate.get_random_user_agent()

    def maximize_window(self):
        """ Maximize Chrome window.

        Example
        ----
        wp.maximize_window()
        """

        self.browser.maximize_window()

    def close(self):
        """ Close Chrome window.

        Example
        ----
        wp.close()
        """

        self.browser.close()

    def __set_error(self, error):
        self.error += "ERROR: " + error + "\r\n"

    @property
    def get_errors(self):
        """ Returns a string with failed tasks.

        :rtype: str

        Example
        ----
        wp.get_errors()

        """

        return "Errors: \n" + self.error

    @property
    def get_completed(self):
        """ Returns a string with completed tasks

        :rtype: str

        Example
        ----
        wp.get_completed()
        """

        return "Completed Tasks: \n" + self.success

    def __check_exists_by_id(self, element_id):
        """ Check if an element exists on page for the given html id

        :type element_id: str
        :rtype: bool
        :param element_id: id attribute of html element
        :returns: True if an element exists on page for the given html id, else False

        Example
        ----
        wp.check_exists_by_id('username')
        """

        try:
            self.browser.find_element_by_id(element_id)
        except NoSuchElementException:
            return False
        return True

    def __check_exists_by_xpath(self, xpath):
        """ Check if an element exists on page for the given html xpath

        :type xpath: str
        :rtype: bool
        :param xpath: xpath of html element
        :returns: True if an element exists on page for the given html xpath, else False

        Example
        ----
        wp.check_exists_by_xpath('//input[@name="user"]')
        """

        try:
            self.browser.find_element_by_xpath(xpath)
        except NoSuchElementException:
            return False
        return True

    def send_keys_select_all(self, xpath=None, element_id=None, wait=False):
        """ Send key combination Ctrl+A to select all text in html element either by xpath or id

        :type xpath: str or None
        :type element_id: str
        :type wait: bool
        :param xpath: xpath of html element
        :param element_id: id attribute of html element
        :param wait: After sending keys, wait for time(if sleep_time set in constructor else 2 seconds)

        Example
        ----
        # Send keys by html xpath
        wp.send_keys_select_all('//input[@name="user"]')

        # Send keys by html id attribute
        wp.send_keys_select_all(None,'username')

        # Wait after sending keys
        wp.send_keys_select_all('//input[@name="user"]', None, True)

        """

        try:
            if xpath:
                self.send_text_exists_by_xpath(xpath, Keys.CONTROL + "a")
            elif element_id:
                self.send_text_exists_by_id(element_id, Keys.CONTROL + "a")
            if wait:
                sleep(self.sleep_time)
        except selenium_exception.NoSuchElementException:
            if xpath:
                self.error += "ERROR: Xpath: " + xpath + " [Element Not Found]\r\n"
            else:
                self.error += "ERROR: Id: " + element_id + " [Element Not Found]\r\n"

    def send_backspace_by_xpath(self, xpath, times, wait=False):
        """ Send backspace key for given number of times in html element by xpath

        :type xpath: str
        :type times: int
        :type wait: bool
        :param xpath: xpath of html element
        :param times: number of times backspace should be sent
        :param wait: After sending key/s, wait for time(if sleep_time set in constructor else 2 seconds)

        Example
        ----
        # Send backspace 10 times in html element by xpath and wait
        wp.send_backspace_by_xpath('//input[@name="user"]', 10, True)

        """

        try:
            for i in range(0, times):
                self.send_text_exists_by_xpath(xpath, Keys.BACK_SPACE)
            if wait:
                sleep(self.sleep_time)
        except selenium_exception.NoSuchElementException:
            self.error += "ERROR: Xpath: " + xpath + " [Element Not Found]\r\n"

    def paste_in_browser(self):
        """ Paste content from clipboard in active html element in browser

        Example
        ----
        wp.paste_in_browser()

        """

        action = ActionChains(self.browser)
        action.key_down(Keys.CONTROL)
        action.send_keys('v')
        action.key_up(Keys.CONTROL)
        action.perform()

    def send_text_in_browser(self, text):
        """ Type given text in active html element in browser

        :type text: str
        :param text: Text to be typed

        Example
        ----
        wp.send_text_in_browser("Hello World!")

        """

        actions = ActionChains(self.browser)
        actions.send_keys(text)
        actions.perform()

    def send_text_exists_by_id(self, element_id, text, error=None, success=None, wait=False, key_wait=None):
        """ Type text in html element by id, if it exists

        :type element_id: str
        :type text: str
        :type error: str
        :type success: str
        :type wait: bool
        :type key_wait: int
        :param element_id: id attribute of html element
        :param text: text to be typed
        :param error: error note in case of failure (Optional)
        :param success: success note in case of completion (Optional)
        :param wait: After typing, wait for time(if sleep_time set in constructor else 2 seconds) (Optional)
        :param key_wait: After each character, wait for time(in seconds) (Optional)

        Example
        ----
        wp.send_text_exists_by_id('username', 'Admin')

        """

        try:
            if not key_wait:
                self.browser.find_element_by_id(element_id).send_keys(text)
            else:
                for i in range(0, len(text)):
                    self.browser.find_element_by_id(element_id).send_keys(text[i])
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

    def send_text_exists_by_xpath(self, xpath, text, error=None, success=None, wait=False):
        """ Type text in html element by xpath, if it exists

        :type xpath: str
        :type text: str or int
        :type error: str
        :type success: str
        :type wait: bool
        :param xpath: xpath of html element
        :param text: text to be typed
        :param error: error note in case of failure (Optional)
        :param success: success note in case of completion (Optional)
        :param wait: After typing, wait for time(if sleep_time set in constructor else 2 seconds) (Optional)

        Example
        ----
        wp.send_text_exists_by_xpath('//input[@name="username"]', 'Admin')

        """

        try:
            self.browser.find_element_by_xpath(xpath).send_keys(text)
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
        """ Click html element by xpath, if it exists

        :type xpath: str
        :type error: str
        :type success: str
        :type wait: bool
        :param xpath: xpath of html element
        :param error: error note in case of failure (Optional)
        :param success: success note in case of completion (Optional)
        :param wait: After click, wait for time(if sleep_time set in constructor else 2 seconds) (Optional)

        Example
        ----
        wp.click_exists_by_xpath('//input[@name="login"]')

        """

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
                self.error += "ERROR: " + error + " [Element Not Intractable]\r\n"
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
        """ Click html elements by xpath, if they exist

        :type xpath: str
        :type wait: bool
        :param xpath: xpath of html elements
        :param wait: After click on all elements, wait for time(if sleep_time set in constructor else 2 seconds)
        (Optional)

        Example
        ----
        wp.click_exists_by_xpath_elements('//input[@type="button"]')

        """

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
        """ Login to WordPress site

        :type email: str
        :type password: str
        :param email: email or username of WordPress User
        :param password: password of WordPress User

        Example
        ----
        wp.wp_login('email', 'password')

        """

        self.browser.get(self.login_url)
        sleep(self.sleep_time)
        self.browser.find_element_by_id('user_login').send_keys(email)
        sleep(self.sleep_time)
        self.browser.find_element_by_id('user_pass').send_keys(password)
        self.browser.find_element_by_id('wp-submit').click()

    def open_page_posts(self):
        """ Open All Posts Page
        """

        self.browser.get(self.site_url + "/wp-admin/edit.php")

    def post_title(self, title):
        """ Set Post Title

        :type title: str
        :param title: title of the post

        Example
        ----
        wp.post_title("Post Title")

        """

        if self.__check_exists_by_id("post-title-0"):
            self.browser.find_element_by_id("post-title-0").send_keys(title)
        else:
            self.__set_error("Unable to type post title!")

    # After post published
    def post_url(self, url):
        """ Set Post Url.
        Applicable after publishing post.

        :type url: str
        :param url: title of the post

        Example
        ----
        wp.post_url("url")

        """

        self.post_document_setting_open()
        xpath_u = '//label[text()="URL Slug"]/following-sibling::input[@type="text"]'
        if not self.__check_exists_by_xpath(xpath_u):
            # Expand Heading Settings
            err = 'Unable to expand Permalink'
            self.click_exists_by_xpath('//button[@type="button" and text()="Permalink"]', err, wait=True)
        err = "Unable to type post url"
        self.send_text_exists_by_xpath(xpath_u, url, err, wait=True)

    def __post_content_use_default_editor(self, xpath='//button[text()="Use Default Editor"]'):
        """ If the WordPress site has an active theme with page builder or a page builder plugin installed,
        use this function to choose Block editor.

        :type xpath: str
        :param xpath: xpath of the use default editor button (optional)

        Example
        ----
        wp.post_content_use_default_editor()

        """

        err = 'Unable to use default editor'
        self.click_exists_by_xpath(xpath, err)
        sleep(self.sleep_time)

    def post_content_block_setting_open(self):
        """ Open or switch to BLOCK SETTING Panel on the right.

        """

        xpath = '//button[@type="button" and @aria-label="Block (selected)"]'
        if self.__check_exists_by_xpath(xpath):
            return True

        xpath = '//button[@type="button" and @aria-label="Block"]'
        err = "Unable to open Block setting"
        self.click_exists_by_xpath(xpath, err, wait=True)

    def post_content_block_add(self, block_name):
        """ Add a block in the editor
        Available blocks are: Heading, Paragraph, List, Image, Custom HTML

        :type block_name: str
        :param block_name: block name to be added (case insensitive) ['heading', 'paragraph', 'list', 'image', 'html']

        Example
        ----
        # For Heading:
        wp.post_content_block_add("heading")

        # For Paragraph:
        wp.post_content_block_add("paragraph")

        # For List:
        wp.post_content_block_add("list")

        # For Image:
        wp.post_content_block_add("image")

        # For Custom HTML:
        wp.post_content_block_add("html")

        """

        blocks = {
            'heading': 'Heading',
            'paragraph': 'Paragraph',
            'list': 'List',
            'image': 'Image',
            'html': 'Custom HTML'
        }
        if block_name.lower() not in blocks:
            self.__set_error('Enter a valid block name')
            return False
        err = 'Unable to add block :' + block_name
        cmp = block_name + ' Added'
        check_add = '//button[@type="button" and @aria-label="Add block"]'
        if self.click_exists_by_xpath(check_add, err):
            check_add = '//input[@type="search" and @placeholder="Search for a block"]'
            if self.send_text_exists_by_xpath(check_add, block_name, wait=True):
                check_add = '//span[text()="' + blocks[block_name] + '"]/parent::button'
                if self.click_exists_by_xpath(check_add, err, cmp, True):
                    return True

    # Block edit as html
    def post_content_block_edit_as_html(self, html=False):
        """ Click on Edit as HTML Button of Editor Block

        :type html: bool
        :param html: True if editor block is to be edited as custom html

        Example
        ----
        wp.post_content_block_edit_as_html(True)

        """

        if html:
            xpath_a = '//button[text()="Edit as HTML" and @type="button"]'
            if not self.__check_exists_by_xpath(xpath_a):
                # Open General Settings Menu
                xpath_e = '//button[@type="button" and @aria-label="More options"]'
                err = "Unable to open General Settings Menu"
                self.click_exists_by_xpath(xpath_e, err, wait=True)
            err = "Unable to click Edit as html"
            self.click_exists_by_xpath(xpath_a, err, wait=True)

    # Heading Block Setting
    def post_content_block_setting_heading(self, style):
        """ Select Heading style.
        Available styles are: h1, h2, h3, h4, h5, h6

        :type style: str
        :param style: Style of heading tag. Allowed: ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']

        Example
        ----
        wp.post_content_block_setting_heading('h1')

        """

        head = {
            'h1': 'Heading 1',
            'h2': 'Heading 2',
            'h3': 'Heading 3',
            'h4': 'Heading 4',
            'h5': 'Heading 5',
            'h6': 'Heading 6'
        }
        if style.lower() in head:
            check_h = '//button[@type="button" and @aria-label="' + head[style] + '"]'
            if not self.__check_exists_by_xpath(check_h):
                # Expand Heading Settings
                err = 'Unable to expand Heading Settings'
                self.click_exists_by_xpath('//button[@type="button" and text()="Heading Settings"]', err)
                sleep(self.sleep_time)

            err = 'Invalid Heading style: [' + style + ']'
            self.click_exists_by_xpath(check_h, err)

    # Text Block Setting
    def post_content_block_setting_text(self, size=None, custom_size=None, drop_cap=False):
        """ Set Paragraph block settings.

        :type size: str
        :type custom_size: int
        :type drop_cap: bool
        :param size: choose font size from sizes available in the editor:
        ['default', 'small', 'normal', 'medium', 'large', 'huge'] (optional)
        :param custom_size: font size (optional)
        :param drop_cap: Set first character of paragraph to capital (optional)

        Example
        ----
        # Using editor's font size
        wp.post_content_block_setting_text("normal")

        # Using custom font size
        wp.post_content_block_setting_text(None, 54)

        # Set First character capital of Text
        wp.post_content_block_setting_text("small", None, True)

        """

        xpath_text = '//label[text()="Custom"]/following-sibling::input[@type="number"]'
        if not self.__check_exists_by_xpath(xpath_text):
            # Expand Text Settings
            self.click_exists_by_xpath('//button[text()="Text Settings" and @type="button"]')
            sleep(self.sleep_time)

        if custom_size:
            self.send_text_exists_by_xpath(xpath_text, custom_size)

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
                self.send_text_exists_by_xpath(xpath_text, size_list[size], err)
                sleep(self.sleep_time)
            else:
                self.__set_error('Invalid text size: ' + size)

        if drop_cap:
            xpath_text = '//p[text()="Toggle to show a large initial letter."]/preceding-sibling::div//input[@type="checkbox"]'
            err = 'Unable to use Drop Cap'
            self.click_exists_by_xpath(xpath_text, err)

    # Text Block Setting
    def post_content_block_setting_text_align(self, align="left"):
        """ Select text alignment.
        Available alignments are: left, center, right

        :type align: str
        :param align: text alignment (default="left"). Allowed: ['left', 'center', 'right']

        Example
        ----
        wp.post_content_block_setting_text_align("center")

        """

        list_align = [
            'left',
            'center',
            'right'
        ]
        if align.lower() in list_align:
            self.click_exists_by_xpath('//span[text()="Color settings"]/parent::button[@type="button"]', wait=True)
            xpath_a = '//button[@type="button" and text()="Align text ' + align.lower() + '"]'
            if not self.__check_exists_by_xpath(xpath_a):
                # Open Align Menu
                xpath_e = '//button[@type="button" and @aria-label="Change text alignment"]'
                err = "Unable to open Text Align Menu"
                self.click_exists_by_xpath(xpath_e, err, wait=True)
            err = "Unable to align text " + align
            self.click_exists_by_xpath(xpath_a, err, wait=True)
        else:
            self.__set_error("Invalid text alignment")

    # Color Block Setting
    def post_content_block_setting_color(self, text_color=None, bg_color=None):
        """ Set color of text and background.

        :type text_color: str
        :type bg_color: str
        :param text_color: hex color code. (optional)
        :param bg_color: hex color code. (optional)

        Example
        ----
        wp.post_content_block_setting_color('#1bbafe', '#ffffff')

        """

        xpath_color = '(//button[text()="Custom color" and @type="button" and @aria-label="Custom color picker"])[1]'
        if not self.__check_exists_by_xpath(xpath_color):
            # Expand Color Settings
            err = "Unable to expand Color Settings"
            self.click_exists_by_xpath('//span[text()="Color settings"]/parent::button[@type="button"]', err, wait=True)

        if text_color:
            err = "Unable to set text color"
            if self.click_exists_by_xpath(xpath_color, err):
                xpath_color = '//label[text()="Color value in hexadecimal"]/following-sibling::input[@type="text"]'
                sleep(self.sleep_time)
                self.send_backspace_by_xpath(xpath_color, 8)
                err = "Unable to type text color"
                self.send_text_exists_by_xpath(xpath_color, text_color, err)

        if bg_color:
            xpath_color = '(//button[@type="button" and @aria-label="Custom color picker" and text()="Custom color"])[2]'
            err = "Unable to set background color"
            if self.click_exists_by_xpath(xpath_color, err):
                xpath_color = '//label[text()="Color value in hexadecimal"]/following-sibling::input[@type="text"]'
                sleep(self.sleep_time)
                self.send_backspace_by_xpath(xpath_color, 8)
                err = "Unable to type background color"
                self.send_text_exists_by_xpath(xpath_color, bg_color, err)

    # Image Block Setting
    def post_content_block_setting_image_border(self, round_shape=False):
        """ Set style for Image Border.

        :type round_shape: bool
        :param round_shape: True, to set round borders. (default=False)

        Example
        ----
        wp.post_content_block_setting_image_border(True)

        """

        xpath_s = '//div[@role="button" and @aria-label="Default"]'
        if not self.__check_exists_by_xpath(xpath_s):
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
        """ Set image block style.

        :type alt_text: str
        :type size: str
        :type width: int
        :type height: int
        :type percentage: int
        :param alt_text: Alt text for image (optional)
        :param size: Select size of Image from editor. Allowed: ['thumbnail', 'medium', 'large', 'full'] (optional)
        :param width: Width of image (optional)
        :param height: Height of image (optional)
        :param percentage: Percentage of image. Allowed: [25, 50, 75, 100] (optional)

        Example
        ----
        wp.post_content_block_setting_image("Image 1", "full", 500, 500, 75%)

        """
        xpath_s = '//label[text()="Alt text (alternative text)"]/following-sibling::textarea'
        if not self.__check_exists_by_xpath(xpath_s):
            # Expand Styles Settings
            err = "Unable to expand Image Settings"
            self.click_exists_by_xpath('//button[text()="Image settings" and @type="button"]', err, wait=True)

        if alt_text:
            err = "Unable to type alt text"
            self.send_text_exists_by_xpath(xpath_s, alt_text, err, wait=True)

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
            self.send_text_exists_by_xpath(xpath_s, width, err, wait=True)

        if height:
            xpath_s = '//label[text()="Height"]/following-sibling::input[@type="number"]'
            err = "Unable to set height"
            self.send_keys_select_all(xpath_s)
            self.send_text_exists_by_xpath(xpath_s, height, err, wait=True)

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
    def post_content_block_setting_image_align(self, align="left"):
        """ Select image alignment
        Available alignments are: left, center, right

        :type align: str
        :param align: image alignment (default="left"). Allowed: ['left', 'center', 'right']

        Example
        ----
        wp.post_content_block_setting_image_align("center")

        """

        list_align = [
            'left',
            'center',
            'right'
        ]
        if align.lower() in list_align:
            xpath_a = '//button[@type="button" and text()="Align ' + align.lower() + '"]'
            if not self.__check_exists_by_xpath(xpath_a):
                # Open Align Menu
                xpath_e = '//button[@type="button" and @aria-label="Change alignment"]'
                err = "Unable to open Align Menu"
                self.click_exists_by_xpath(xpath_e, err, wait=True)
            err = "Unable to align image " + align
            self.click_exists_by_xpath(xpath_a, err, wait=True)
        else:
            self.__set_error("Invalid image alignment")

    # List Block Setting
    def post_content_block_setting_ordered_list(self, start=None, reverse=False):
        """ Customize List block style.

        :type start: int
        :type reverse: bool
        :param start: Number from where to start the list. (optional)
        :param reverse: Reverse the numbering of list. (optional)

        Example
        ----
        wp.post_content_block_setting_ordered_list(10, True)

        """
        xpath_o = '//label[text()="Start value"]/following-sibling::input[@type="number"]'
        if not self.__check_exists_by_xpath(xpath_o):
            # Expand Ordered list Settings
            err = "Unable to expand Styles Settings"
            self.click_exists_by_xpath('//button[text()="Ordered list settings" and @type="button"]', err, wait=True)
        if start:
            err = "Unable to set Start value"
            self.send_text_exists_by_xpath(xpath_o, start, err, wait=True)
        if reverse:
            xpath_o = '//label[text()="Reverse list numbering"]'
            err = 'Unable to reverse list order'
            self.click_exists_by_xpath(xpath_o, err, wait=True)

    def post_content_block_heading(self, heading, style='default', align='left', text_color=None):
        """ Add heading block and customize it.

        :type heading: str
        :type style: str
        :type align: str
        :type text_color: str
        :param heading: Heading text
        :param style: Style of heading tag. Allowed: ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']
        :param align: Heading alignment (default="left"). Allowed: ['left', 'center', 'right'] (optional)
        :param text_color: hex color code for heading's text color. (optional)

        Example
        ----
        # Simple
        wp.post_content_block_heading("Heading 1")

        # Customized
        wp.post_content_block_heading("Heading 1", 'h1', 'center', '#1bbafe')

        """

        if self.post_content_block_add('heading'):
            self.send_text_in_browser(heading)
            if align != "left":
                self.post_content_block_setting_text_align(align)
            if style != 'default':
                self.post_content_block_setting_heading(style)
            if text_color:
                self.post_content_block_setting_color(text_color)

    def post_content_block_paragraph(self, paragraph, align='left', size=None, custom_size=None, drop_cap=False,
                                     text_color=None, bg_color=None):
        """ Add paragraph block and customize it.

        :type paragraph: str
        :type align: str
        :type size: str or None
        :type custom_size: int or None
        :type drop_cap: bool
        :type text_color: str or None
        :type bg_color: str or None
        :param paragraph: Paragraph text
        :param align: Paragraph alignment (default="left"). Allowed: ['left', 'center', 'right'] (optional)
        :param size: choose font size from sizes available in the editor:
        ['default', 'small', 'normal', 'medium', 'large', 'huge'] (optional)
        :param custom_size: font size (optional)
        :param drop_cap: Set first character of paragraph to capital (optional)
        :param text_color: hex color code for paragraph's text color. (optional)
        :param bg_color: hex color code for paragraph's background color. (optional)

        Example
        ----
        # Simple
        wp.post_content_block_paragraph("This is a paragraph.")

        # Customized
        wp.post_content_block_paragraph("This is a paragraph.", "center", "normal", None, True, "#1bbafe", "#ffffff")

        """

        if self.post_content_block_add('paragraph'):
            self.send_text_in_browser(paragraph)
            if align != "left":
                self.post_content_block_setting_text_align(align)

            if size or custom_size or drop_cap:
                self.post_content_block_setting_text(size, custom_size, drop_cap)

            if text_color or bg_color:
                self.post_content_block_setting_color(text_color, bg_color)

    def post_content_block_image(self, image_name=None, caption=None, image_url=None, align='left', round_shape=None,
                                 alt_text=None, size=None, width=None, height=None, percentage=None):
        """ Add image block and customize it.
        For Image block, image can be added either from media library or by using url.

        :type image_name: str
        :type caption: str
        :type image_url: str
        :type align: str
        :type round_shape: bool
        :type alt_text: str
        :type size: str
        :type width: int
        :type height: int
        :type percentage: int
        :param image_name: Image name in media library. (Full image name is not necessary) (optional)
        {Image must be in media of WordPress site, for this to work}
        :param caption: Caption for Image (optional)
        :param image_url: Image url (optional)
        :param align: image alignment (default="left"). Allowed: ['left', 'center', 'right']
        :param round_shape: True, to set round borders. (default=False)
        :param alt_text: Alt text for image (optional)
        :param size: Select size of Image from editor. Allowed: ['thumbnail', 'medium', 'large', 'full'] (optional)
        :param width: Width of image (optional)
        :param height: Height of image (optional)
        :param percentage: Percentage of image. Allowed: [25, 50, 75, 100] (optional)

        Example
        ----
        # Simple

        wp.post_content_block_image("ImageName")
        wp.post_content_block_image(None, None, "https://www.example.com/image")

        # Customized

        wp.post_content_block_image("ImageName", "caption", None, "center", True, "alt-text", "thumbnail", 500, 500, 75)

        """

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
                    self.send_text_in_browser(image_url)
                    err = "Unable to click Apply Button"
                    if self.click_exists_by_xpath('//button[@type="submit" and @aria-label="Apply"]', err, wait=True):
                        size = None
                        check = True

            if check:
                if align != "left":
                    self.post_content_block_setting_image_align(align)

                if caption:
                    xpath = '//figcaption[@role="textbox" and text()=""]'
                    err = "Unable to type caption"
                    if self.send_text_exists_by_xpath(xpath, caption, err, wait=True):
                        if not percentage and not width and not height:
                            percentage = 100

                self.post_content_block_setting_image_border(round_shape)
                self.post_content_block_setting_image(alt_text, size, width, height, percentage)

    def post_content_block_list(self, list_text, ordered=False, start=None, reverse=False, separator='.'):
        """ Add list block and customize it.

        :type list_text: str
        :type ordered: bool
        :type start: int
        :type reverse: bool
        :type separator: str
        :param list_text: List
        :param ordered: True, for numbering. (optional)
        :param start: Number from where to start the list. (optional)
        :param reverse: Reverse the numbering of list. (optional)
        :param separator: Separator before new item in the list. (default=".")
        Example: "Line 1. Line 2" -- Here "." is the separator between list items.

        Example
        ----
        # Un-ordered List
        wp.post_content_block_list("Line 1. Line 2")

        # Ordered List
        wp.post_content_block_list("Line 1. Line 2", True, 50, True)

        # Using separator
        wp.post_content_block_list("Line 1, Line 2", True, 50, True, ",")

        """

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
                self.send_text_in_browser(list_text[i] + separator)
                if i == len(list_text) - 1:
                    break
                self.send_text_in_browser(Keys.RETURN)

            if ordered and (start or reverse):
                self.post_content_block_setting_ordered_list(start, reverse)

    def post_content_block_html(self, html):
        """ Add html block.

        :type html: str
        :param html: html code for html block

        Example
        ----
        wp.post_content_block_html("<div><h5>Heading</h5></div>")

        """

        self.post_content_block_add('html')
        self.send_text_in_browser(html)

    def post_content_from_file(self, file_path='', typing_effect=False):
        """ Add a block using docx or html file.

        :type file_path: str
        :type typing_effect: bool
        :param file_path: path to docx or html file on computer.
        :param typing_effect: True if keyboard typing effect is required. (optional) (default=False)

        Example
        ----
        # Docx file
        wp.post_content_from_file("C\\Path\\To\\File.docx")

        # Html file with typing effect
        wp.post_content_from_file("C\\Path\\To\\File.html", True)

        """

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
            if not typing_effect:
                pyperclip.copy(html)
                sleep(self.sleep_time)
                self.paste_in_browser()
            else:
                self.send_text_in_browser(html)
        else:
            self.__set_error("Invalid File Type")

    def post_document_setting_open(self):
        """ Switch to DOCUMENT SETTING Panel on the right.

        Example
        ----
        wp.post_document_setting_open()

        """

        xpath = '//button[@type="button" and @aria-label="Document (selected)"]'
        if self.__check_exists_by_xpath(xpath):
            return True

        xpath = '//button[@type="button" and @aria-label="Document"]'
        err = "Unable to open Document setting"
        self.click_exists_by_xpath(xpath, err, wait=True)

    def post_status(self, visibility='public', password=None, stick_top=False, pending_review=False):
        """ Configure Post Status Settings

        :type visibility: str
        :type password: str
        :type stick_top: bool
        :type pending_review: bool
        :param visibility: Visibility of Post. Allowed: ['public', 'private, 'password'] (optional)
        :param password: Password for post if visibility set to password protected.
        :param stick_top: True to stick post on top on the blog page. (optional)
        :param pending_review: True to add post in pending

        Example
        ----
        Public post

        wp.post_status('public', password=None, True, True)

        Private post

        wp.post_status('private')

        Password protected post

        wp.post_status('password', "your-password-here")
        """

        element_discus = '//span[text()="Visibility"]'
        if not self.__check_exists_by_xpath(element_discus):
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
                    self.send_text_exists_by_xpath(xpath_pass, password, err)
                    sleep(self.sleep_time)

    # After post published
    def post_format(self, formatting='standard'):
        """ Set Post Format.

        :type formatting: str
        :param formatting: Post display format. Allowed: ['standard', 'gallery', 'link', 'quote', 'video', 'audio']

        ### Example
        ----
        wp.post_format('gallery')

        """

        self.post_document_setting_open()
        format_list = ['standard', 'gallery', 'link', 'quote', 'video', 'audio']
        if formatting.lower() in format_list:
            xpath_ = '//label[text()="Post Format"]/following-sibling::div//select/option[@value="' + formatting + '"]'
            err = "Unable to select post format"
            self.click_exists_by_xpath(xpath_, err, wait=True)

    def post_category(self, category):
        """ Choose category if category name exists otherwise create new category.

        :type category: str
        :param category: Post category name

        Example
        ----
        wp.post_category("category-name")

        """

        err = 'Unable to expand Categories Panel(Categories)!'
        if self.click_exists_by_xpath('//button[text()="Categories"]', err):
            # Expand Categories
            sleep(self.sleep_time)

        check_cat = "//label[text()='" + category + "']"
        if not self.__check_exists_by_xpath(check_cat):
            # Add if category does not exist
            err = "Unable to click Add New Category 1"
            self.click_exists_by_xpath('//button[text()="Add New Category"]', err)

            err = "Unable to type Category name"
            self.send_text_exists_by_xpath("//*[@id='editor-post-taxonomies__hierarchical-terms-input-0']", category,
                                           err)

            err = "Unable to click Add New Category 2"
            self.click_exists_by_xpath('//button[@type="submit" and text()="Add New Category"]', err)
        else:
            # Select category
            err = "Unable to Select category"
            self.click_exists_by_xpath(check_cat, err)

    def post_tag(self, tag):
        """ Choose tag if tag name exists otherwise create new tag.

        :type tag: str
        :param tag: tag name of the post

        Example
        ----
        wp.post_tag("tag-name")
        """

        check_tag = '//label[text()="Add New Tag"]/following-sibling::div/child::input'
        if not self.__check_exists_by_xpath(check_tag):
            # Expand Tags
            err = "Unable to Expand Tags"
            self.click_exists_by_xpath('//button[text()="Tags"]', err, wait=True)

        # Add Tag
        tag_input = self.browser.find_element_by_xpath(check_tag)
        tag_input.send_keys(tag + Keys.RETURN)

    def __media_search_and_select(self, image_name, image_type="Select"):
        """ Search and select image from media library of WordPress site

        :type image_name: str
        :type image_type: str
        :param image_name: Name of the Image in media library
        :param image_type: Select or Set featured image
        """

        err = "Unable to type image name"
        self.send_keys_select_all(None, 'media-search-input')
        self.send_text_exists_by_id('media-search-input', image_name, err, wait=True)

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
        """ Set Featured Image for Post from media library.

        :type image_name: str
        :param image_name: Name of the Image in media library.

        Example
        ----
        wp.post_image("featured-image-name")

        """

        featured_img = '//button[text()="Set featured image"]'
        if not self.__check_exists_by_xpath(featured_img):
            # Expand Featured Image
            err = "Unable to Expand Featured Image"
            self.click_exists_by_xpath('//button[text()="Featured image"]', err)

        err = "Unable to click Set featured image"
        self.click_exists_by_xpath('//button[text()="Set featured image"]', err, wait=True)
        self.__media_search_and_select(image_name, "Set featured image")

    def post_excerpt(self, excerpt):
        """ Set Post excerpt.

        :type excerpt: str
        :param excerpt: excerpt of the post.

        Example
        ----
        wp.post_excerpt("excerpt-text")

        """

        check_excerpt = '//label[text()="Write an excerpt (optional)"]/following-sibling::textarea'
        if not self.__check_exists_by_xpath(check_excerpt):
            # Expand Excerpt
            err = "Unable to Expand Excerpt Setting"
            self.click_exists_by_xpath('//button[text()="Excerpt"]', err, wait=True)

        # Add Excerpt
        self.browser.find_element_by_xpath(check_excerpt).send_keys(excerpt)

    def post_discussion(self, comments=True, traceback=True):
        """ Configure Discussion settings for post.

        :type comments: bool
        :type traceback: bool
        :param comments: False to Disable comments on post.
        :param traceback: False to Disable pingbacks & trackbacks.

        Example
        ----
        wp.post_discussion(False, False)

        """

        element_discus = '//label[text()="Allow comments"]'
        if not self.__check_exists_by_xpath(element_discus):
            # Expand Discussion
            err = "Unable to Expand Discussion"
            self.click_exists_by_xpath('//button[text()="Discussion"]', err)

        # Uncheck comments
        if not comments:
            err = "Unable to Disable comments"
            self.click_exists_by_xpath(element_discus, err)
        # Uncheck traceback
        if not traceback:
            element_discus = '//label[text()="Allow pingbacks & trackbacks"]'
            err = "Unable to Disable pingbacks & trackbacks"
            self.click_exists_by_xpath(element_discus, err)

    def post_save_draft(self):
        """ Save Post as Draft.

        Example
        ----
        wp.post_save_draft()

        """

        xpath_save = '//button[text()="Publish…" and @aria-disabled="true"]'
        if self.__check_exists_by_xpath(xpath_save):
            sleep(self.sleep_time)
        xpath_save = '//button[text()="Save Draft"]'
        if not self.__check_exists_by_xpath(xpath_save):
            xpath_save = '//button[text()="Save as Pending"]'
            err = "Unable to click Save as Pending Button"
            self.click_exists_by_xpath(xpath_save, err, wait=True)
            sleep(self.sleep_time)
        else:
            err = "Unable to click Save Draft Button"
            if self.click_exists_by_xpath(xpath_save, err, wait=True):
                sleep(self.sleep_time)

    def post_switch_to_draft(self):
        """ Switch Post from Published to Draft.

        Example
        ----
        wp.post_switch_to_draft()
        """

        xpath_d = '//button[text()="Switch to draft"]'
        err = "Unable to click Switch to Draft Button"
        sleep(self.sleep_time)
        if self.click_exists_by_xpath(xpath_d, err, wait=True):
            alert_obj = self.browser.switch_to.alert
            alert_obj.accept()
            self.browser.switch_to.default_content()
            sleep(self.sleep_time)

    def post_publish(self):
        """ Publish Post.

        Example
        ----
        wp.post_publish()

        """

        xpath_p = '//button[text()="Publish…" and @aria-disabled="true"]'
        if self.__check_exists_by_xpath(xpath_p):
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
        """ Update Post.

        Example
        ----
        wp.post_update()

        """

        xpath_u = '//button[text()="Update"]'
        err = "Unable to click Update Button"
        if self.click_exists_by_xpath(xpath_u, err, wait=True):
            sleep(self.sleep_time)

    @staticmethod
    def read_html(html_path, full=False):
        """ Read html file and return the code.

        :type html_path: str
        :type full: bool
        :param html_path: html file path.
        :param full: True to get full code, otherwise code in body tag. (optional)
        :rtype: str
        :return: html code of the file.

        Example
        ----
        wp.read_html("C\\Path\\To\\File.html")

        """

        f = codecs.open(html_path, 'r')
        html = f.read()
        soup = BeautifulSoup(html, 'html.parser')
        if not full:
            return soup.body.prettify()
        else:
            return soup.prettify()

    def docx_to_html(self, docx_path):
        """ Convert docx file to html code.

        :type docx_path: str
        :param docx_path: Path of docx file.
        :rtype: str
        :return: html code of the file.

        Example
        ----
        wp.docx_to_html("C\\Path\\To\\File.docx")

        """

        with open(docx_path, "rb") as docx_file:
            result = d2h.convert_to_html(docx_file)
            html = result.value
            self.messages = result.messages
        return html

    def post_new(self, title, category=None, tag=None, featured_image=None, excerpt=None, file_path=None):
        """ Add new post on WordPress site.

        :type title: str
        :type category: str
        :type tag: str
        :type featured_image: str
        :type excerpt: str
        :type file_path: str
        :param title: title of the post.
        :param category:  category name of the post. (optional)
        :param tag: tag of the post. (optional)
        :param featured_image: name of the Image in media library to set as featured image. (optional)
        :param excerpt: excerpt of the post. (optional)
        :param file_path: path of docx or html file for post content. (optional)

        Example
        ----
        Post with just a title:

        wp.post_new("Post Title")

        Post with title, category, tag, featured image and excerpt:

        wp.post_new("Post Title", "Technology", "tech", "featured", "This is excerpt for this post")

        Post with title, category, tag, featured image, excerpt and a file to post from:

        wp.post_new("Post Title", "Technology", "tech", "featured", "This is excerpt for this post",
        "docx/html-file-path")

        """

        self.browser.get(self.site_url + "/wp-admin/post-new.php")
        sleep(self.sleep_time_page_load)

        xpath = '//button[@type="button" and @aria-label="Close dialog"]'
        if self.__check_exists_by_xpath(xpath):
            err = "Unable to close tutorial pop up"
            self.click_exists_by_xpath(xpath, err)

        self.__post_content_use_default_editor()

        # Add title
        self.post_title(title)

        if category:
            sleep(self.sleep_time)
            self.post_category(category)

        if tag:
            sleep(self.sleep_time)
            self.post_tag(tag)

        if featured_image:
            sleep(self.sleep_time)
            self.post_image(featured_image)

        if excerpt:
            sleep(self.sleep_time)
            self.post_excerpt(excerpt)

        if file_path:
            sleep(self.sleep_time)
            html = self.docx_to_html(file_path)
            self.post_content_block_html(html)
