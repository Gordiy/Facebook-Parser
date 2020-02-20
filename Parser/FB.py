import os
from selenium import webdriver

class FB:
    def __init__(self):
        path = os.getcwd() + '/chromedriver'
        self.driver = webdriver.Chrome(path)

    def login(self, login_url, login, password):
        self.driver.get(login_url)

        fb_email_field = self.driver.find_element_by_id('email')
        fb_pass_field = self.driver.find_element_by_id('pass')
        login_btn = self.driver.find_element_by_id('loginbutton')

        fb_email_field.send_keys(login)
        fb_pass_field.send_keys(password)
        login_btn.click()

        current_url = self.driver.current_url.split("?")[0]

        if current_url == 'https://www.facebook.com/login/device-based/regular/login/':
            return True

    def parse_group(self, link_to_group):
        pass
