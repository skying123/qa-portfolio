# QA Portfolio · 全栈自动化测试框架

[![QA Portfolio CI](https://github.com/skying123/qa-portfolio/actions/workflows/ci.yml/badge.svg)](https://github.com/skying123/qa-portfolio/actions/workflows/ci.yml)
[![Allure Report](https://img.shields.io/badge/Allure%20Report-Live-blue?logo=github)](https://skying123.github.io/qa-portfolio/)
![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Pytest](https://img.shields.io/badge/Pytest-8.2-green?logo=pytest)
![Selenium](https://img.shields.io/badge/Selenium-4.21-orange?logo=selenium)

> **项目定位**：基于 `Selenium + Pytest + Allure + JMeter` 的工程化测试框架，覆盖接口/UI/性能三层，支持 CI/CD 自动触发与可视化报告。

---

## 🚀 在线报告（点击即看）

| 报告类型 | 链接 | 说明 |
|---------|------|------|
| **Allure 测试报告** | [📊 点击查看](https://skying123.github.io/qa-portfolio/) | 每次 push 自动更新，含趋势图、用例详情、请求日志 |
| **GitHub Actions** | [⚙️ 构建记录](https://github.com/skying123/qa-portfolio/actions) | 查看每次构建日志与 artifact |

---

## 🏗️ 架构设计
```text
qa-portfolio/
├── .github/workflows/ci.yml   # CI/CD：自动测试 + Allure报告部署
├── api_tests/                  # 接口自动化（DummyJSON）
│   ├── conftest.py             # Fixture：env/api_config/api_client
│   ├── test_auth.py            # 登录认证（正向+逆向+参数化）
│   └── test_users.py           # 用户CRUD（GET/POST/PUT/DELETE）
├── ui_tests/                   # UI自动化（Selenium POM）← Week2
├── utils/
│   ├── api_client.py           # 生产级客户端：自动重试、Session复用、Allure日志
│   └── config_reader.py        # 多环境配置读取（dev/prod）
├── data/users.yaml             # 测试数据与代码分离
├── config/
│   ├── dev.ini                 # 开发环境配置
│   └── prod.ini                # 生产环境配置
└── requirements.txt            # 依赖管理
```
---

## 🛠️ 技术亮点

| 能力 | 实现细节 |
|-----|---------|
| **防御性设计** | `tenacity` 自动重试（仅网络异常时重试3次，4xx/5xx不重试避免加压服务端） |
| **请求可观测** | 每个请求自动 attach 请求参数/响应体到 Allure，失败时秒级定位 |
| **多环境零改动** | `pytest --env=prod` 读取不同 ini，CI 与本地配置隔离 |
| **Session 复用** | TCP 连接池复用，保持登录态，25 个接口用例执行时间从 15s 降至 5s |
| **数据驱动** | 边界值用例全部抽离到 YAML，新增场景改配置即可 |

---

## 📦 本地运行

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 运行接口测试并生成 Allure 结果
pytest api_tests/ -v --env=dev --alluredir=./allure-results

# 3. 查看可视化报告
allure serve ./allure-results
```