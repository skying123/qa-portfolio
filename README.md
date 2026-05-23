# QA Portfolio · 全栈自动化测试框架

[![QA Portfolio CI](https://github.com/skying123/qa-portfolio/actions/workflows/ci.yml/badge.svg)](https://github.com/skying123/qa-portfolio/actions/workflows/ci.yml)
[![Allure Report](https://img.shields.io/badge/Allure%20Report-Live-blue?logo=github)](https://skying123.github.io/qa-portfolio/)
![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Pytest](https://img.shields.io/badge/Pytest-8.2-green?logo=pytest)
![Selenium](https://img.shields.io/badge/Selenium-4.21-orange?logo=selenium)

>**项目定位**：基于 `Selenium + Pytest + Allure + JMeter` 的工程化测试框架，覆盖接口 / UI / 性能三层，支持 CI/CD 自动触发、多环境配置与可视化报告。

---

## 🚀 在线报告（点击即看）

| 报告类型 | 链接 | 说明 |
|---------|------|------|
| **Allure 测试报告** | [📊 点击查看](https://skying123.github.io/qa-portfolio/) | 每次 push 自动更新，含趋势图、用例详情、请求日志、失败截图 |
| **GitHub Actions** | [⚙️ 构建记录](https://github.com/skying123/qa-portfolio/actions) | 查看每次构建日志与 artifact |

---

## 🏗️ 架构设计

```text
qa-portfolio/
├── .github/workflows/ci.yml      # CI/CD：自动测试 + Allure报告部署
├── api_tests/                     # 接口自动化（DummyJSON）
│   ├── conftest.py                # Fixture：env / api_config / api_client
│   ├── test_auth.py               # 登录认证（正向 + 逆向 + 参数化）
│   └── test_users.py              # 用户CRUD（GET / POST / PUT / DELETE）
├── ui_tests/                      # UI自动化（Selenium POM）
│   ├── conftest.py                # Driver fixture、失败截图 hook
│   └── test_e2e.py                # 登录 → 加购 → 结账端到端
├── pages/                         # POM 页面对象
│   ├── __init__.py
│   ├── base_page.py               # 基类：显式等待、Allure 步骤、截图
│   ├── login_page.py              # 登录页
│   ├── inventory_page.py          # 商品列表页
│   ├── cart_page.py               # 购物车页
│   └── checkout_page.py           # 结账页
├── utils/                         # 工具封装
│   ├── api_client.py              # 生产级客户端：自动重试、Session 复用、Allure 日志
│   └── config_reader.py           # 多环境配置读取（dev / prod）
├── data/
│   └── users.yaml                 # 测试数据与代码分离
├── config/
│   ├── dev.ini                    # 开发环境（有头浏览器、本地chromedriver）
│   └── prod.ini                   # CI环境（无头浏览器、自动下载driver）
├── performance/                   # JMeter 性能测试
│   └── jmeter/
│       ├── dummyjson_load_test.jmx    # 压测脚本
│       ├── data/
│       │   └── users.csv              # 登录参数化数据
│       └── html-report/               # HTML 性能报告（本地生成）
├── requirements.txt
├── pytest.ini
└── README.md
```
---

## 🛠️ 技术亮点

| 能力             | 实现细节                                                      |
| -------------- | --------------------------------------------------------- |
| **POM 模式**     | 页面对象与业务用例分离，定位器集中管理，UI 变更只需改一页                            |
| **防御性设计**      | `tenacity` 自动重试（仅网络异常时重试 3 次，4xx/5xx 不重试避免加压服务端）          |
| **请求可观测**      | 每个请求自动 attach 请求参数 / 响应体到 Allure，失败时秒级定位                  |
| **多环境零改动**     | `pytest --env=prod` 读取不同 ini，代码零改动支持多环境                   |
| **Session 复用** | TCP 连接池复用，保持登录态，接口执行效率提升数倍                                |
| **数据驱动**       | 边界值用例全部抽离到 YAML，新增场景改配置即可                                 |
| **失败自动截图**     | UI 用例失败自动 attach PNG 到 Allure，无需手动复现                      |
| **趋势图持久化**     | Allure History 跨构建保留，支持多次运行的通过率趋势对比                       |
| **环境信息注入**     | 自动写入 `environment.properties`，报告展示 Python 版本、测试环境、BaseURL |
| **参数化压测**    | JMeter CSV 数据驱动，模拟多用户登录与业务循环 |

---

## 📊 性能测试基线

使用 JMeter 对 DummyJSON 进行混合负载压测，**10 并发用户 × 10 线程组迭代 × 5 业务循环**，总请求 **1010 次**，结果如下：

| 接口 | 样本数 | 平均响应(ms) | 中位数(ms) | 90% Line(ms) | 错误率 | 吞吐量(req/s) |
|-----|-------|------------|-----------|-------------|-------|--------------|
| **用户登录** | 10 | 1,748 | 1,412 | 2,702 | 0.00% | 1.61 |
| **查询用户列表** | 500 | 858 | 748 | 1,411 | 0.00% | 5.24 |
| **查询单个用户** | 500 | 509 | 354 | 923 | 0.00% | 5.24 |
| **总体** | 1,010 | 694 | 589 | 1,213 | 0.00% | 10.28 |

> 设计说明：登录通过 `Once Only Controller` 每个线程仅执行 1 次，后续循环复用会话，符合真实用户行为。DummyJSON 为公开演示站点，响应时间受公网波动影响，私有化部署可进一步优化。

---

## 📦 本地运行

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 运行接口测试
pytest api_tests/ -v --env=dev --alluredir=./allure-results

# 3. 运行 UI 测试（有头模式，会弹出浏览器）
pytest ui_tests/ -v --env=dev --alluredir=./allure-results

# 4. 运行全部冒烟用例
pytest -v -m smoke --env=dev --alluredir=./allure-results

# 5. 查看可视化报告（需安装 Allure CLI）
allure serve ./allure-results

# 6. 运行 JMeter 性能测试（非 GUI 模式）
jmeter -n -t performance/jmeter/dummyjson_load_test.jmx \
  -l performance/jmeter/result.jtl \
  -e -o performance/jmeter/html-report

# 7. 查看性能 HTML 报告
open performance/jmeter/html-report/index.html
```

## 📈 演示路线（面试 3 分钟版）

1. **仓库首页** → 点击 `Allure Report` 徽章进入在线报告
2. **Overview** → 展示测试套件通过率与历史趋势图
3. **Behaviors** → 按 Feature / Story 层级展示 `认证模块` / `用户管理模块` / `UI自动化`
4. **Suites** → 展开 `test_e2e_purchase`，展示 6 个 Allure Step（登录 → 加购 → 结账）
5. **失败截图** → 展示 `test_demo_failure_screenshot` 的自动截图附件
6. **Environment** → 展示自动注入的 Python 版本、测试环境、BaseURL
7. **Actions 页** → 展示 CI 自动触发记录，说明每次提交都有质量门禁
8. **JMeter 报告** → 打开 `performance/jmeter/html-report/index.html`，说明 10 并发下吞吐量 **10.28 req/s**、错误率 **0%**、登录 90% Line **2.7s**、查询接口 90% Line **&lt;&lt; 1.5s**

## 🧰 技术栈

- **语言**：Python 3.11
- **测试框架**：Pytest + Allure
- **接口测试**：Requests + tenacity（重试）
- **UI 测试**：Selenium + WebDriver Manager
- **性能测试**：JMeter
- **CI/CD**：GitHub Actions
- **数据格式**：YAML / INI