import time
from .utils import get_id_from_url, remove_duplicate
from selenium import webdriver


class FacebookParser:
    def __init__(self, path_to_chrome_webdriver):
        print(path_to_chrome_webdriver)
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications": 2}
        chrome_options.add_experimental_option("prefs", prefs)

        self.__driver = webdriver.Chrome(executable_path=path_to_chrome_webdriver, options=chrome_options)

    def login(self, fb_base_url):
        self.__driver.get(fb_base_url)

        email = self.__driver.find_element_by_id('email')
        pswd = self.__driver.find_element_by_id('pass')
        login_btn = self.__driver.find_element_by_id('loginbutton')

        email.send_keys('gordiy.yuriy.gord123@gmail.com')
        pswd.send_keys('46256As61F2')
        login_btn.click()

        current_url = self.__driver.current_url.split('?')[0]

        if current_url != 'https://www.facebook.com/login/device-based/regular/login/':
            return {'status': 'ok'}
        else:
            print("Can not login!")

    def __get_ids(self):
        links = []
        div_users = self.__driver.find_elements_by_class_name('_60ri')

        for user_link in div_users:
            link = user_link.find_element_by_tag_name('a').get_attribute('href')
            user_id = get_id_from_url(link)
            if user_id is not None and user_id not in links:
                links.append(link)

        return links

    def groups_members_id(self, group_url):
        members = []

        self.__driver.get(group_url+'/members')

        SCROLL_PAUSE_TIME = 0.6

        # Get scroll height
        last_height = self.__driver.execute_script("return document.body.scrollHeight")
        time.sleep(2)

        while True:
            # Scroll down to bottom
            self.__driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            members += self.__get_ids()
            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)
            # Calculate new scroll height and compare with last scroll height
            new_height = self.__driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        remove_duplicate(members)
        return members
