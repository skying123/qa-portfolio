import json
import allure
import requests
from typing import Any,Optional
from loguru import logger
from tenacity import (
    retry,
    stop_after_attempt,
    wait_fixed,
    retry_if_exception_type,
    before_sleep_log
)
from requests.exceptions import RequestException,Timeout

class APIClient:
    """
    生产级接口客户端
    - 自动拼接base_url
    - 失败自动重试3次（间隔2秒）
    - 自动记录allure步骤与附件
    - 使用request.session复用tcp连接,提升性能
    """
    def __init__(self,base_url:str,timeout:int=10):
        # 去掉URL末尾可能存在的/
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout

        # 复用session，自动保持TCP连接
        self.session = requests.Session()
        self.session.headers.update({
            'content-type':'application/json',
            'Accept':'application/json'
        })

        logger.info(f'APIClient 初始化 | base_url={self.base_url} | timeout={timeout}s')

    def _prepare_url(self,endpoint:str) -> str:
        """
        拼接完整URL
        """
        endpoint = endpoint.lstrip('/')
        return f'{self.base_url}/{endpoint}'

    @retry(
            stop=stop_after_attempt(3), # 最多重试3次（含首次）
            wait=wait_fixed(2),         # 重试间隔2秒
            retry=retry_if_exception_type((RequestException,Timeout)), # 重试条件，请求异常或超时
            reraise=True,               # 3次重试失败后，直接抛出异常
            before_sleep=before_sleep_log(logger,'retrying...')      # 重试前打印日志
    )
    def request(self,method:str,endpoint:str,**kwargs) -> requests.Response:
        """
        通用请求方法
        :param method: http方法（get,post,put,delete等）
        :param endpoint: 接口路径，如 /api/users
        :param kwargs: 其它参数，透传给requests.request，支持 json=, data=, params=, headers= 等
        :return: requests.Response
        """
        url = self._prepare_url(endpoint)
        # 如果传入参数中没有指定timeout，则使用默认超时
        if 'timeout' not in kwargs:
            kwargs['timeout'] = self.timeout
        
        # allure步骤：在报告里生成一个可折叠的节点
        with allure.step(f'{method.upper()} {endpoint}'):
            # 1.记录请求参数
            request_body = kwargs.get('json') or kwargs.get('data') or kwargs.get('params') or {}
            allure.attach(
                json.dumps(request_body,ensure_ascii=False,indent=2),
                name = '请求参数(Request)',
                attachment_type = allure.attachment_type.JSON
            )
            logger.info(f'请求：{method.upper()}{url} | payload={request_body}')

            # 2. 发起请求
            response = self.session.request(method,url,**kwargs)

            # 3. 记录响应结果到allure
            try:
                resp_body = response.json()
                resp_text = json.dumps(resp_body,ensure_ascii=False,indent=2)
                attach_type = allure.attachment_type.JSON
            except ValueError:
                resp_text = response.text
                attach_type = allure.attachment_type.TEXT
            
            allure.attach(
                resp_text,
                name = f'响应数据（Status：{response.status_code})',
                attach_type = attach_type
            )

            logger.info(f'响应：{response.status_code} | body={resp_text[:500]}')

            # 4. 返回响应对象
            return response
    
    def get(self,endpoint:str,**kwargs) -> requests.Response:
        return self.request('GET',endpoint,**kwargs)
    
    def post(self,endpoint:str,**kwargs) -> requests.Response:
        return self.request('POST',endpoint,**kwargs)
    
    def put(self,endpoint:str,**kwargs) -> requests.Response:
        return self.request('PUT',endpoint,**kwargs)
    
    def delete(self,endpoint:str,**kwargs) -> requests.Response:
        return self.request('DELETE',endpoint,**kwargs)

    def close(self):
        """
        关闭session连接
        """
        self.session.close()
        logger.info('APIClient 连接已关闭')