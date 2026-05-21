import allure
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CartPAGE(BasePage):
    """SauceDemo 购物车页面"""

    CART_ITEMS = (By.CLASS_NAME,'cart-item')
    CHECKOUT_BUTTON = (By.ID,'checkout')
    CONTINUE_SHOPPING = (By.ID,'continue-shopping')

    def get_items_count(self) -> int:
        return len(self.find_elements(self.CART_ITEMS))
    
    def click_checkout(self):
        with allure.step('点击结账按钮'):
            self.click(self.CHECKOUT_BUTTON)