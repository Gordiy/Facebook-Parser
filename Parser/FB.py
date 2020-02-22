import time
import random
from .utils import get_id_from_url, remove_duplicate
from selenium import webdriver


class FacebookParser:
    def __init__(self, path_to_chrome_webdriver):
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications": 2}
        chrome_options.add_experimental_option("prefs", prefs)

        self.__fb_base_url = 'https://www.facebook.com/'
        self.__messenger_base_url = 'https://www.messenger.com/'
        self.__driver = webdriver.Chrome(executable_path=path_to_chrome_webdriver, options=chrome_options)

    def login(self, login, password):
        self.__driver.get(self.__fb_base_url)

        email = self.__driver.find_element_by_id('email')
        pswd = self.__driver.find_element_by_id('pass')
        login_btn = self.__driver.find_element_by_id('loginbutton')

        email.send_keys(login)
        pswd.send_keys(password)
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
                links.append(user_id)

        return links

    def groups_members_id(self, group_url):
        members = []

        if group_url[len(group_url)-1] == '/':
            group_url += 'members'
        else:
            group_url += '/members'

        print(group_url)
        self.__driver.get(group_url)

        # Get scroll height
        last_height = self.__driver.execute_script("return document.body.scrollHeight")
        time.sleep(2)

        while True:
            # Scroll down to bottom
            self.__driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            members += self.__get_ids()
            # Wait to load page
            sleep_scroll = random.randint(1, 3)
            time.sleep(sleep_scroll)
            # Calculate new scroll height and compare with last scroll height
            new_height = self.__driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        remove_duplicate(members)
        return members

    def connect_to_group(self, group_url):
        info = {}

        self.__driver.get(group_url)
        div_connect = self.__driver.find_element_by_class_name('_21kr')
        try:
            div_connect.find_element_by_tag_name('span').click()
            info['status'] = 'connected'
        except Exception as e:
            print(e)
            info['status'] = 'connected before'

        return info

    def messenger_login(self, login, password):
        self.__driver.get(self.__messenger_base_url+'/login')

        email = self.__driver.find_element_by_id('email')
        pswd = self.__driver.find_element_by_id('pass')
        login_btn = self.__driver.find_element_by_id('loginbutton')

        email.send_keys(login)
        pswd.send_keys(password)
        login_btn.click()

        if self.__driver.current_url != 'https://www.messenger.com/login/password/':
            return {'status': 'ok'}
        else:
            print("Can not login!")

    def send_message(self, user_id, text):
        self.__driver.get('{0}{1}{2}'.format(self.__messenger_base_url, 't/', user_id))

        div_input = self.__driver.find_element_by_class_name('_1mf._1mj')
        div_input.find_element_by_tag_name('span').send_keys(text)

        path = self.__driver.find_element_by_class_name('_30yy._38lh._7kpi')
        path.click()

    def parse_chat(self, user_id):
        self.__driver.get(self.__messenger_base_url+'t/'+user_id)

        elem = self.__driver.find_elements_by_class_name('_41ud')
        print(elem)

