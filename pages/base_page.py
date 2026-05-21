import allure
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import List, Tuple

class BasePage:
    """POM基类：封装显式等待与常用操作，自动附加allure步骤"""

    def __init__(self,driver:WebDriver,base_url:str):
        self.driver = driver
        self.base_url = base_url.rstrip('/')
        self.wait = WebDriverWait(driver,10)

    def open(self,url:str=''):
        """打开页面，自动附加allure步骤"""
        full_url = f'{self.base_url}/{url.lstrip("/")}' if url else self.base_url
        with allure.step(f'打开页面：{full_url}'):
            self.driver.get(full_url)

    def find_element(self,locator:Tuple[str,str]) -> WebElement:
        """显式等待元素可见，返回单个元素"""
        return self.wait.until(EC.visibility_of_element_located(locator))
    
    def find_elements(self,locator:Tuple[str,str]) -> list[WebElement]:
        """显式等待多个元素可见，返回元素列表"""
        return self.wait.until(EC.visibility_of_all_elements_located(locator))
    
    def click(self,locator:Tuple[str,str]):
        """显式等待元素可点击，然后点击"""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        with allure.step(f'点击元素：{locator}'):
            element.click()
    
    def input_text(self,locator:Tuple[str,str],text:str):
        """清空并输入文本"""
        element = self.find_element(locator)
        with allure.step(f'输入文本：{text} 到 {locator}'):
            element.clear()
            element.send_keys(text)

    def get_text(self,locator:Tuple[str,str]) -> str:
        """获取元素文本"""
        return self.find_element(locator).text
    
    def is_displayed(self,locator:Tuple[str,str]) -> bool:
        """判断元素是否显示"""
        try:
            return self.find_element(locator).is_displayed()
        except Exception:
            return False
        
    def take_screenshot(self,name:str='截图'):
        """截图并附加到allure"""
        png = self.driver.get_screenshot_as_png()
        allure.attach(
            png,
            name=name,
            attachment_type=allure.attachment_type.PNG
        )