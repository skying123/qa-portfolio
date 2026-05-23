FROM jenkins/jenkins:lts

USER root

# 系统依赖
RUN apt-get update && apt-get install -y \
    openjdk-21-jre \
    python3 \
    python3-pip \
    chromium \
    chromium-driver \
    npm \
    && npm install -g allure-commandline --registry=https://registry.npmmirror.com \
    && npm cache clean --force \
    && rm -rf /var/lib/apt/lists/*

# 验证
RUN allure --version && python3 --version && chromium --version

USER jenkins
