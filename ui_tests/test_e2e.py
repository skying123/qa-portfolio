import pytest
import allure
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPAGE
from pages.checkout_page import CheckoutPage
from selenium.webdriver.common.by import By


@allure.feature('UI自动化')
@allure.story('SauceDemo电商流程')
class TestSauceDemo:

    @allure.title('登录成功-进入商品列表')
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.ui
    def test_login_success(self,driver,ui_config):
        login_page = LoginPage(driver,ui_config['base_url'])
        login_page.open()
        login_page.login('standard_user','secret_sauce')

        inventory = InventoryPage(driver,ui_config['base_url'])
        assert inventory.is_displayed(inventory.PRODUCT_ITEMS),'商品列表未显示'

    @allure.title('登录失败-锁定用户提示错误')
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.ui
    def test_login_locked_user(self,driver,ui_config):
        login_page = LoginPage(driver,ui_config['base_url'])
        login_page.open()
        login_page.login('locked_out_user','secret_sauce')

        error_message = login_page.get_error_message()
        assert 'locked out' in error_message.lower(),f'错误提示不符合预期：{error_message}'

    @allure.title('端到端-登录加购物结账完整流程')
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.ui
    def test_e2e_purchase(self,driver,ui_config):
        base_url = ui_config['base_url']

        # 1.登录
        with allure.step('步骤1：登录'):
            login = LoginPage(driver,base_url)
            login.open()
            login.login('standard_user','secret_sauce')

        # 2.加购
        with allure.step('步骤2：添加商品到购物车'):
            inventory = InventoryPage(driver,base_url)
            inventory.add_first_product_to_cart()
            count = inventory.get_cart_count()
            assert count == 1,f'购物车数量应为1，实际为：{count}'

        # 3.进入购物车并结账
        with allure.step('步骤3：进入购物车'):
            inventory.go_to_cart()
            cart = CartPAGE(driver,base_url)
            cart_count = cart.get_items_count()
            assert cart_count == 1,f'购物车商品数量不为1，实际为：{cart_count}'

        with allure.step('步骤4：点击结账'):
            cart.click_checkout()
        
        # 4.填写信息
        with allure.step('步骤5：填写收货信息'):
            checkout = CheckoutPage(driver,base_url)
            checkout.fill_info('test','user','12345')

        # 5.完成订单
        with allure.step('步骤6：完成订单'):
            checkout.finish()
            complete_header = checkout.get_complete_header()
            assert 'Thank you' in complete_header,f'完成页标题不符合预期：{complete_header}'

    @allure.title('演示-失败自动截图')
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.xfail(reason='故意失败，用于演示allure自动截图能力',strict=False)
    @pytest.mark.ui
    def test_demo_failure_screenshot(self,driver,ui_config):
        """此用例故意断言不存在的元素，触发失败截图，用于演示"""
        login = LoginPage(driver,ui_config['base_url'])
        login.open()
        login.login('standard_user','secret_sauce')

        # 留下成功登录截图
        login.take_screenshot('登录成功截图')

        inventory = InventoryPage(driver, ui_config["base_url"])
        inventory.add_first_product_to_cart()

        # 再截图一次，留下购物车加购成功截图
        inventory.take_screenshot('购物车加购成功截图')

        # 故意失败，触发截图
        assert inventory.is_displayed((By.ID,'not-exist-element')),'故意触发失败截图'