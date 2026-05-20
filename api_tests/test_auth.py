import pytest
import allure
from utils import data_loader

# 读取yaml中的测试数据
# def load_test_data():
#     root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#     data_path = os.path.join(root_dir,'data','users.yaml')
#     with open(data_path,'r',encoding='utf-8') as f:
#         return yaml.safe_load(f)
    
TEST_DATA = data_loader.load_test_data()

@allure.feature('认证模块')
@allure.story('登录')
class TestAuth:
    """
    登录相关测试
    """

    @allure.title('登录成功-返回有效token')
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.api
    def test_login_success(sels,api_client):
        """使用有效凭证登录，验证返回的token"""
        data = TEST_DATA['auth']['valid_user']

        with allure.step('发送登录请求'):
            response = api_client.post('/auth/login',json=data)
        
        with allure.step('断言状态码为200'):
            assert response.status_code == 200,f'期望200，实际{response.status_code}'

        with allure.step('断言返回的token有效'):
            body = response.json()
            assert 'accessToken' in body,f'返回数据部应包含token字段，实际响应为{body}'
            assert len(body['accessToken']) > 0,f'token字段不应为空'

            allure.attach(
                body['accessToken'],
                name='获取到的accessToken',
                attachment_type=allure.attachment_type.TEXT
            )

    @allure.title('登录失败-无效密码')
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.api
    def test_login_invalid_password(self,api_client):
        """密码错误时，应返回401且不含token"""
        data = TEST_DATA['auth']['invalid_password']

        with allure.step('使用错误密码登录'):
            response = api_client.post('/auth/login',json=data)

        with allure.step('断言状态码为400或401'):
            assert response.status_code in [400,401],f'期望400或401，实际{response.status_code}'

        with allure.step('断言响应体不含有效token'):
            body = response.json()
            assert 'accessToken' not in body,'错误响应不应包含accessToken'
            assert any(k in body for k in ['error','message']),f'错误响应应包含error或message字段,实际响应为{body}'
    
    @allure.title('登录失败-缺少必填字段：{case_name}')
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.api
    @pytest.mark.parametrize('case_name,payload',[
        # ('缺少密码',{'username':'emilys'}),
        # ('缺少用户名',{'password':'emilyspass'}),
        # ('空对象',{})
        (case["name"], case["payload"])
            for case in TEST_DATA["auth"]["missing_field_cases"]
    ])
    def test_login_missing_field(self,api_client,case_name,payload):
        """必填字段缺少时，应返回400"""
        with allure.step(f'发生不完整请求：{case_name}'):
            response = api_client.post('/auth/login',json=payload)

        with allure.step('断言状态码为400'):
            assert response.status_code == 400,f'期望400，实际{response.status_code}'

        with allure.step('断言响应应包含错误提示'):
            body = response.json()
            assert 'message' in body or 'error' in body,'应提示字段缺失'