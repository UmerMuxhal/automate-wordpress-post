import requests
import time
from bs4 import BeautifulSoup
from lxml.html import fromstring
from itertools import cycle
from selenium.webdriver.chrome.options import Options
import subprocess
from random_user_agent.params import SoftwareName, OperatingSystem
from random_user_agent.user_agent import UserAgent
import os
from datetime import date
import pandas as pd
from time import sleep
import pandas as pd
from random_user_agent.params import SoftwareName, OperatingSystem
from random_user_agent.user_agent import UserAgent
from selenium import webdriver
# import pyautogui
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys


def user_agent_generator():
    software_names = [SoftwareName.CHROME.value]
    operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
    user_agent_rotate = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)
    return user_agent_rotate.get_random_user_agent()


def get_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//tbody/tr')[:10]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            # Grabbing IP and corresponding PORT
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    return proxies


def proxies_generator():
    proxies = {
        'http': 'http://10.10.1.10:3128',
        'https': 'http://10.10.1.10:1080',
        'https': 'http://166.249.185.133:45607',
        'https': 'http://103.119.145.138:8080',
        'https': 'http://176.110.121.90:21776',
    }
    return proxies


def schoobly_scrape():
    url = "https://schoobly.com/"
    # url = "https://www.schoobly.com/search?updated-max=2020-03-31T23:55:00%2B05:30&max-results=60&start=10&by-date=true"
    post_title = []
    post_category = []
    post_req = []
    post_des = []
    post_for = []
    post_desc = []
    post_link = []
    post_img = []
    next_page = True

    today = date.today()
    today = today.strftime("%B %d, %Y")
    today = "March 31, 2020"

    headers = {'User-Agent': user_agent_generator()}
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        raise ConnectionError
    soupO = BeautifulSoup(res.text, 'html.parser')

    while next_page:
        internal_link = []
        page = soupO.find("div", {"class": "blog-posts"})

        post_info = page.find_all("div", {"class": "post-info"})
        for n in post_info:
            post_info_date = n.find("span", {"class": "post-date"}).getText()
            if post_info_date != today:
                next_page = False
                continue
            heading = n.find("h2", {"class": "post-title"})
            internal_link.append(heading.find('a')['href'])

        for n in internal_link:
            res = requests.get(n, headers=headers)
            if res.status_code != 200:
                raise ConnectionError
            soup = BeautifulSoup(res.text, 'html.parser')

            post_title.append(soup.find("h1", {"class": "post-title"}).getText().replace("\n", ""))  # Post Title
            tmp_cat = soup.find("nav", {"id": "breadcrumb"})
            post_category.append(tmp_cat.find("a", {"class": "b-label"}).getText())  # Post Category
            # des = soup.find("div", {"class": "about-course"}).prettify()
            post_desc.append(
                soup.find("div", {"class": "about-course"}).getText().replace("   ", " ").replace("  ", " ").replace(
                    "...", ""))  # Post Description
            tmp_img = soup.find("div", {"class": "post-body"})
            post_img.append(tmp_img.find("img", {"class": "post-thumb"})['src'])  # Post Image Link
            tmp_link = soup.find("div", {"class": "enroll-button"})
            post_link.append(tmp_link.find("a", {"class": "read-more"})['href'])  # Post Link

        if next_page:
            headers = {'User-Agent': user_agent_generator()}
            next_link = soupO.find("a", {"id": "Blog1_blog-pager-older-link"})['href']
            res = requests.get(next_link, headers=headers)
            if res.status_code != 200:
                raise ConnectionError
            soupO = BeautifulSoup(res.text, 'html.parser')

    return post_title, post_category, post_desc, post_link, post_img


def collect_from_udemy(links):
    post_req = []
    post_des = []
    post_for = []

    # proxies = get_proxies()
    proxies = proxies_generator()
    proxy_pool = cycle(proxies)

    for link in links:

        proxy = next(proxy_pool)

        headers = {'User-Agent': user_agent_generator()}
        res = requests.get(link, headers=headers, proxies=proxies)
        if res.status_code != 200:
            raise ConnectionError
        bs4 = BeautifulSoup(res.text, 'html.parser')
        req = bs4.find("div", {"class": "requirements__content"}).getText()
        print(req)
        post_req.append(req)
        des = bs4.find("div", {"class": "description__title"}).find_next("div").getText()
        print(des)
        post_des.append(des)
        who = bs4.find("div", {"class": "audience__list"}).getText()
        print(who)
        post_for.append(who)
        break

    return post_req, post_des, post_for


def create_folder(folder=str(date.today())):
    folder = os.getcwd() + "\\" + folder
    if not os.path.exists(folder):
        os.makedirs(folder)


def create_csv(title, cat, desc, link, img, folder=str(date.today()), file=str(date.today())):
    df = pd.DataFrame()
    df['Title'] = title
    df['Category'] = cat
    df['Description'] = desc
    df['Link'] = link
    df['Image'] = img
    df = df[['Title', 'Category', 'Description', 'Link', 'Image']]

    file_name = os.getcwd() + "\\" + folder + "\\" + file + ".csv"
    # file_name = os.getcwd() + "\\" + "2020-03-31" + "\\" + "2020-03-31" + ".csv"
    header = ['Title', 'Category', 'Description', 'Link', 'Image']
    df.to_csv(file_name, encoding='utf-8', index=False, header=header)


def read_link(file=os.getcwd() + "\\" + str(date.today()) + "\\" + str(date.today())):
    df = pd.read_csv(file + ".csv")
    links = []
    for li in df['Link']:
        links.append(li)
    return links


def read_csv(file=os.getcwd() + "\\" + str(date.today()) + "\\" + str(date.today())):
    df = pd.read_csv(file + ".csv")
    titles = []
    links = []
    cats = []
    imgs = []
    for ti in df['Title']:
        titles.append(ti)
    for ca in df['Category']:
        cats.append(ca)
    for li in df['Link']:
        links.append(li)
    for im in df['Image Name']:
        imgs.append(im)

    return titles, links, cats, imgs


def download_image(title, url, folder=str(date.today())):
    for i in range(0, len(title)):
        title[i] = rename_file(title[i])
        title[i] = str(i + 1) + "-" + title[i] + ".jpg"
        title[i] = os.getcwd() + "\\" + folder + "\\" + title[i]
        # title[i] = os.getcwd() + "\\" + "2020-03-31" + "\\" + title[i]
        req = requests.get(url[i], allow_redirects=True)
        with open(title[i], 'wb') as f:
            f.write(req.content)


def rename_file(text):
    text = text.replace("?", "").replace("|", "").replace(":", "").replace(";", "").replace("/", "").replace("\"", "")
    text = text.replace("\\", "").replace(" ", "-").replace("!", "").replace("&", "").replace("'", "")
    text = text.replace("+", "").replace("(", "-").replace(")", "-")
    text = text.replace("---", "-").replace("--", "-")
    text = text.lower()
    return text


def open_firefox_private(link):
    for n in link:
        subprocess.call([r'C:\Program Files\Firefox Developer Edition\firefox.exe', '-private-window', n])
        time.sleep(30)


# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# SELENIUM
# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def get_chrome_options():
    user_agent = user_agent_generator()
    chrome_options = Options()
    chrome_options.add_argument('--window-size=1420,1080')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument(f'user-agent={user_agent}')
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_experimental_option("prefs", {
        "profile.default_content_setting_values.notifications": 2
    })
    return chrome_options


# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# MAIN
# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# title, cat, desc, link, img = schoobly_scrape()
# create_folder()
# create_csv(title, cat, desc, link, img)
# download_image(title, img)
#   # open_firefox_private(link)


# links = read_link()
# open_firefox_private(links)

# file = "F:\C\laragon\www\\ai\scrapping\\2020-03-31\\2020-03-31"
# print(file)
# file = os.getcwd() + "\\" + str(date.today()) + "\\" + str(date.today())
# print(file)
# links = read_link(file)
# collect_from_udemy(links)


def check_exists_by_xpath(browser, xpath):
    try:
        browser.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True


def sell():
    chrome_options = get_chrome_options()
    browser = webdriver.Chrome(executable_path='chromedriver')
    browser = webdriver.Chrome(chrome_options=chrome_options)

    url = "http://www.technologyinfos.com/courses/wp-admin/"
    # url = "http://www.technologyinfos.com"
    browser.get(url)

    sleep(3)

    browser.maximize_window()
    usr = input('Enter Email Id:')
    pwd = input('Enter Password:')

    username_box = browser.find_element_by_id('user_login')
    username_box.send_keys(usr)
    sleep(3)

    password_box = browser.find_element_by_id('user_pass')
    password_box.send_keys(pwd)

    login_box = browser.find_element_by_id('wp-submit')
    login_box.click()

    url_posts = "http://www.technologyinfos.com/courses/wp-admin/edit.php"
    url_new_post = "http://www.technologyinfos.com/courses/wp-admin/post-new.php"

    small_wait = 2
    normal_wait = 5
    long_wait = 8
    implicit_wait = 10
    divi_wait = 15

    file = "F:\C\laragon\www\\ai\scrapping\\2020-04-07\\2020-04-07"
    titles, links, cats, imgs = read_csv(file)
    if len(titles) == len(links):
        for i in range(16, len(titles)):
            if i == 0 or i == 1:
                continue
            browser.get(url_new_post)
            title_box = browser.find_element_by_id("post-title-0")
            title_box.send_keys(titles[i])

            # browser.find_element_by_xpath('//button[text()="Outliers"]')

            check_cat = '//button[text()="Add New Category"]'
            if not check_exists_by_xpath(browser, check_cat):
                sleep(small_wait)
                category = browser.find_element_by_xpath('//button[text()="Categories"]')
                category.click()

            try:
                sleep(normal_wait)
                category_select = browser.find_element_by_xpath("//label[text()='" + cats[i] + "']")
                category_select.click()

            except NoSuchElementException as e:
                btn_add_category = browser.find_element_by_xpath('//button[text()="Add New Category"]')
                btn_add_category.click()

                new_category = browser.find_element_by_xpath(
                    "//*[@id='editor-post-taxonomies__hierarchical-terms-input-0']")
                new_category.send_keys(cats[i])
                btn_add_new_category = browser.find_element_by_xpath(
                    '//button[@type="submit" and text()="Add New Category"]')
                btn_add_new_category.click()

            featured_img = '//button[text()="Set featured image"]'
            if not check_exists_by_xpath(browser, featured_img):
                sleep(small_wait)
                featured_img = browser.find_element_by_xpath('//button[text()="Featured Image"]')
                featured_img.click()

            sleep(small_wait)
            set_featured_img = browser.find_element_by_xpath('//button[text()="Set featured image"]')
            set_featured_img.click()

            sleep(normal_wait)
            img_search = browser.find_element_by_id('media-search-input')
            img_search.send_keys(imgs[i])

            sleep(normal_wait)
            img_select = browser.find_element_by_xpath('//li[@role="checkbox"]')
            img_select.click()

            sleep(small_wait)
            btn_set_featured_img = browser.find_element_by_xpath(
                '//button[contains(@class, "media-button-select") and text()="Set featured image"]')
            btn_set_featured_img.click()

            sleep(small_wait)
            hide_title = browser.find_element_by_xpath("//select[@name='et_single_title']/option[text()='Hide']")
            hide_title.click()
            # print("hideTitle: " + hide_title)

            sleep(small_wait)
            save_draft = browser.find_element_by_xpath('//button[text()="Save Draft"]')
            save_draft.click()
            # print("saveDraft: " + save_draft)

            sleep(long_wait)
            btn_use_divi = browser.find_element_by_xpath('//button[text()="Use Divi Builder"]')
            btn_use_divi.click()
            # print("use divi builder: " + btn_use_divi)

            browser.implicitly_wait(implicit_wait)
            sleep(divi_wait)
            btn_browse_layout = browser.find_element_by_xpath("//button[text()='Browse Layouts']")
            # btn_browse_layout = browser.find_element_by_xpath("//button[contains(text(),'Browse Layouts' ]")
            # btn_browse_layout = browser.find_element_by_xpath('//*[@id="et-fb-settings-column"]/div/div/div/div/ul/li[2]/a')
            # btn_browse_layout = browser.find_element_by_xpath(
            #     '/html/body/div[1]/div/div/div/div/div/article/div/div/div/div[1]/div/div[2]/div/div[2]/div/button')
            btn_browse_layout.click()
            # print("btn browse layout: " + btn_browse_layout)

            sleep(implicit_wait)
            btn_saved_layout = browser.find_element_by_link_text("Your Saved Layouts")
            # btn_saved_layout = browser.find_element_by_xpath('//*[@id="et-fb-settings-column"]/div/div/div/div/ul/li[2]/a')
            # btn_saved_layout = browser.find_element_by_xpath(
            #     '/html/body/div[1]/div/div/div/div/div/article/div/div/div/div[1]/div/div[3]/div/div/div/div/ul/li[2]/a')
            btn_saved_layout.click()
            # print("saved layout: " + btn_saved_layout)

            sleep(normal_wait)
            browser.switch_to.frame(1)
            btn_template = browser.find_element_by_xpath("//*[@id='dlib-app']/div[1]/div[2]/div[2]/div[2]/a[6]")
            btn_template.click()

            sleep(long_wait)
            # browser.switch_to.frame(0)

            # btn_enroll = browser.find_element_by_xpath("//*[@id='et_pb_root']/div/div[1]/div[6]/div[2]/div[2]/a")
            # browser.switch_to.active_element
            # btn_enroll.click()
            #
            # sleep(long_wait)
            # enroll_setting = browser.find_element_by_xpath(
            #     "//*[@id='et_pb_root']/div/div[1]/div[6]/div[2]/div[2]/div[2]/div/div/button[1]")
            # enroll_setting.click()
            #
            # sleep(long_wait)
            # enroll_link = browser.find_element_by_xpath("//*[@id='et-fb-app']/div[3]/div[3]/div/div[1]/form/div[2]/div")
            # enroll_link.click()
            #
            # sleep(long_wait)
            # enroll_url = browser.find_element_by_xpath("//*[@id='et-fb-button_url']")
            # enroll_url.send_keys(links[i])
            #
            # sleep(long_wait)
            # enroll_save = browser.find_element_by_xpath("//*[@id='et-fb-app']/div[3]/div[4]/div/button[4]")
            # enroll_save.click()
            #
            # sleep(long_wait)
            # browser.switch_to.default_content() #imp ******************
            btn_publish = browser.find_element_by_xpath("//*[@id='et_pb_root']/div/div[3]/div/button[5]")
            btn_publish.click()

            sleep(implicit_wait)
            btn_edit_post = browser.find_element_by_link_text("Edit Post")
            btn_edit_post.click()

            browser.implicitly_wait(implicit_wait)
            sleep(normal_wait)
            page_layout = browser.find_element_by_xpath(
                "//select[@name='et_pb_page_layout']/option[text()='Fullwidth']")
            page_layout.click()

            sleep(small_wait)
            btn_update_post = browser.find_element_by_xpath("//button[text()='Update']")
            btn_update_post.click()
            sleep(implicit_wait)

            # open_firefox_private([links[i]])
            print(i)

            # if i == 0:
            #     break

        input("p: ")


sell()

# file = "F:\C\laragon\www\\ai\scrapping\\2020-04-01\\2020-04-01"
# titles, links = read_csv(file)
# print("titles: ", titles)
# print("links: ", links)
# print("titles Length: ", len(titles))
# print("links Length: ", len(links))
