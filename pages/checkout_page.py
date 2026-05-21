import allure
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CheckoutPage(BasePage):
    """SauceDemo 结账页面"""

    FIRST_NAME = (By.ID,'first-name')
    LAST_NAME = (By.ID,'last-name')
    ZIP_CODE = (By.ID,'postal-code')
    CONTINUE_BUTTON = (By.ID,'continue')
    FINISH_BUTTON = (By.ID,'finish')
    COMPLETE_HEADER = (By.CLASS_NAME,'complete-header')

    def fill_info(self,first:str,last:str,zip_code:str):
        with allure.step(f'填写结账信息：{first} {last},{zip_code}'):
            self.input_text(self.FIRST_NAME,first)
            self.input_text(self.LAST_NAME,last)
            self.input_text(self.ZIP_CODE,zip_code)
            self.click(self.CONTINUE_BUTTON)

    def finish(self):
        with allure.step('点击完成订单'):
            self.click(self.FINISH_BUTTON)

    def get_complete_header(self) -> str:
        return self.get_text(self.COMPLETE_HEADER)