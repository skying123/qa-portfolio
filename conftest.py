# 注册自定义命令行参数
def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="dev",
        help="指定测试环境: dev | prod"
    )