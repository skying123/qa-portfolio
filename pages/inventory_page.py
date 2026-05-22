import allure
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class InventoryPage(BasePage):
    """SauceDemo 商品列表页"""

    PRODUCT_ITEMS = (By.CLASS_NAME,'inventory_item')
    ADD_TO_CART_BUTTONS = (By.CSS_SELECTOR,'.inventory_item .btn_primary')
    CART_BADGE = (By.CLASS_NAME,'shopping_cart_badge')
    MENU_BUTTON = (By.ID,'react-burger-menu-btn')
    LOGOUT_LINK = (By.ID,'logout_sidebar_link')
    CART_LINK = (By.CLASS_NAME,'shopping_cart_link')

    def add_first_product_to_cart(self):
        with allure.step('添加第一个商品到购物车'):
            buttons = self.find_elements(self.ADD_TO_CART_BUTTONS)
            if buttons:
                buttons[0].click()

    def get_cart_count(self) -> int:
        try:
            badge_text = self.get_text(self.CART_BADGE)
            return int(badge_text)
        except Exception:
            return 0
        
    def go_to_cart(self):
        with allure.step('点击购物车图标'):
            self.click(self.CART_LINK)

    def logout(self):
        with allure.step('登出账号'):
            self.click(self.MENU_BUTTON)
            self.click(self.LOGOUT_LINK)