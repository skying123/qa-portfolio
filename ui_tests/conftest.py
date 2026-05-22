import os
import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from utils.config_reader import get_ui_config

def pytest_addoption(parser):
    """添加命令行选项"""
    parser.addoption(
        "--browser",
        action = 'store',
        default = None,
        help = '覆盖浏览器类型，Chrome | Firefox'
    )

@pytest.fixture(scope='session')
def ui_config(request):
    """读取UI环境配置"""
    env = request.config.getoption('--env')
    config = get_ui_config(env)

    # 命令行覆盖浏览器类型
    browser_override = request.config.getoption('--browser')
    if browser_override:
        config['browser'] = browser_override

    allure.attach(
        f'环境：{env}\n'
        f'URL：{config["base_url"]}\n'
        f'浏览器：{config["browser"]}\n'
        f'无头模式：{config["headless"]}\n'
        f'driver路径：{config["driver_path"] or "自动下载"}',
        name= 'UI环境配置',
        attachment_type=allure.attachment_type.TEXT
    )

    return config

@pytest.fixture(scope='function')
def driver(ui_config):
    """每个用例启动一个浏览器实例"""
    browser = ui_config['browser'].lower()
    headless = ui_config['headless']
    driver_path = ui_config['driver_path']

    if browser != 'chrome':
        raise ValueError(f'暂不支持的浏览器：{browser}')
    
    # Chrome选项
    options = ChromeOptions()
    if headless:
        options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')

    # 优先使用本地的浏览器
    if driver_path and os.path.exists(driver_path):
        service = ChromeService(executable_path=driver_path)
        allure.attach(f'使用本地的Chromedriver：{driver_path}',name='Driver来源')
    else:
        service = ChromeService(ChromeDriverManager().install())
        allure.attach('使用自动下载的Chromedriver',name='Driver来源')

    driver = webdriver.Chrome(service=service,options=options)
    driver.implicitly_wait(0) # 禁用隐式等待，全部使用显示等待

    yield driver

    # 关闭浏览器
    driver.quit()
    allure.attach('浏览器已关闭',name='driver清理')

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item,call):
    """测试失败自动截图并附加到allure"""
    outcome = yield
    report = outcome.get_result()

    if report.when == 'call' and report.failed:
        driver = item.funcargs['driver']
        if driver:
            allure.attach(
                driver.get_screenshot_as_png(),
                name='失败截图',
                attachment_type=allure.attachment_type.PNG
            )