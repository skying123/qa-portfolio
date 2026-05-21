import allure
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class LoginPage(BasePage):
    """SauceDemo 登录页面"""

    USERNAME_INPUT = (By.ID,'user-name')
    PASSWORD_INPUT = (By.ID,'password')
    LOGIN_BUTTON = (By.ID,'login-button')
    ERROR_MESSAGE = (By.CSS_SELECTOR,'[data-test="error"]')

    def login(self,username:str,password:str):
        with allure.step(f'登录操作，用户名：{username}'):
            self.input_text(self.USERNAME_INPUT,username)
            self.input_text(self.PASSWORD_INPUT,password)
            self.click(self.LOGIN_BUTTON)

    def get_error_message(self) -> str:
        return self.get_text(self.ERROR_MESSAGE)