import pytest
import allure
from utils.api_client import APIClient
from utils.config_reader import get_api_config

# 注册自定义命令行参数
def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action = "store",
        default = "dev",
        help = "指定测试环境dev | prod"
    )

# 读取当前环境标识
@pytest.fixture(scope='session')
def env(request):
    """
    scope = 'session'：该 fixture 只会在整个测试会话中执行一次，且所有测试用例共享该 fixture 的返回值。
    request.config.getoption("--env")：获取 pytest 命令行参数 --env 的值。
    """
    return request.config.getoption("--env")

# 根据env的值，自动读取对应环境的ini配置文件
@pytest.fixture(scope='session')
def api_config(env:str):
    """
    依赖env,自动读取对应环境的ini配置文件
    """
    config = get_api_config(env)

    # 把配置打印到allure报告中
    allure.attach(
        f'当前环境：{env}\n'
        f'base_url: {config["base_url"]}\n'
        f'timeout: {config["timeout"]}s',
        name = '接口环境配置',
        attachment_type = allure.attachment_type.TEXT
    )

    return config

# 核心：创建 APIClient 实例
@pytest.fixture(scope='session')
def api_client(api_config):
    """
    依赖api_config,创建APIClient实例
    整个测试会话共享同一个 APIClient（单例）
    好处：
      - 复用 TCP 连接，速度快
      - 登录态（Cookie/Token）可以跨用例保持
      - 测试结束自动关闭连接
    """
    client = APIClient(
        base_url = api_config['base_url'],
        timeout = api_config['timeout']
    )

    # 把 client 交给测试用例使用
    yield client

    # yield之后，关闭连接
    client.close()
