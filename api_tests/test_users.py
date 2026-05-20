import pytest
import allure
import yaml
from utils import data_loader

# 获取用户数据
TEST_DATA = data_loader.load_test_data()


@allure.feature('用户模块')
@allure.story('用户curd接口测试')
class TestUsers:
    """用户增删改查接口测试"""
    @allure.title('获取单个用户-ID存在')
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.api
    def test_get_user_success(self,api_client):
        """根据有效ID获取用户详情"""
        user_id = TEST_DATA['users']['existing_id']

        with allure.step(f'请求用户ID：{user_id}'):
            response = api_client.get(f'/users/{user_id}')

        with allure.step('断言状态码为200'):
            assert response.status_code == 200,f'期望200，实际{response.status_code}'
        
        with allure.step('断言响应包含核心用户字段'):
            body = response.json()
            assert 'id' in body,'响应应包含ID字段'
            assert body['id'] == user_id,f'id字段应为{user_id}，实际为：{body.get("id")}'
            assert 'firstName' in body,'响应应包含firstName字段'
            assert 'lastName' in body,'响应应包含lastName字段'

            allure.attach(
                f'用户名：{body.get("firstName")} {body.get("lastName")}',
                name='获取到的用户信息',
                attachment_type=allure.attachment_type.TEXT
            )
    
    @allure.title('获取单个用户-ID不存在')
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.api
    def test_get_user_not_found(self,api_client):
        """查询不存在的用户，应返回404"""
        user_id = TEST_DATA['users']['non_existing_id']

        with allure.step(f'请求用户ID：{user_id}'):
            response = api_client.get(f'/users/{user_id}')

        with allure.step('断言状态码为404'):
            assert response.status_code == 404,f'期望404，实际{response.status_code}'
        
        with allure.step('断言响应应包含错误说明'):
            body = response.json()
            assert 'message' in body or 'error' in body,'404响应应包含错误提示'

    @allure.title('创建新用户')
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.api
    def test_create_user(self,api_client):
        """创建新用户，应返回200/201已经自增ID"""
        payload = TEST_DATA['users']['create']

        with allure.step(f'发送创建请求'):
            response = api_client.post('/users/add',json = payload)

        with allure.step('断言创建成功'):
            assert response.status_code in [200,201],f'期望200/201，实际{response.status_code}'
        
        with allure.step('断言响应应包含新生成的ID'):
            body = response.json()
            assert 'id' in body,'创建成功应返回id'
            assert isinstance(body['id'],int),'id应为整数'
            assert body['id'] > 0,'id应为正整数'

            # 回显校验：后端返回的数据应包含我们提交的内容
            for key in payload:
                assert key in body,f'响应应回显字段：{key}'
                assert body[key] == payload[key],f'字段{key}回显不一致'

            allure.attach(
                f'新用户ID：{body.get("id")}',
                name='新生成的用户ID',
                attachment_type=allure.attachment_type.TEXT
            )
    
    @allure.title('更新用户信息')
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.api
    def test_update_user(self,api_client):
        """put更新用户，验证返回后的数据"""
        user_id = TEST_DATA['users']['existing_id']
        payload = TEST_DATA['users']['update']

        with allure.step(f'更新用户ID={user_id}'):
            response = api_client.put(f'/users/{user_id}',json = payload)

        with allure.step('断言更新成功'):
            assert response.status_code == 200,f'期望200，实际{response.status_code}'
        
        with allure.step('断言字段已更新'):
            body = response.json()
            for key in payload:
                assert body[key] == payload[key],f'字段 {key} 更新失败'

    @allure.title('删除用户')
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.api
    def test_delete_user(self,api_client):
        """delete删除用户，验证返回后的标记"""
        user_id = TEST_DATA['users']['existing_id']

        with allure.step(f'删除用户ID={user_id}'):
            response = api_client.delete(f'/users/{user_id}')

        with allure.step('断言删除成功'):
            assert response.status_code in [200,204],f'期望200/204，实际{response.status_code}'
        
        with allure.step('断言响应包含删除标记'):
            body = response.json()
            # dummyjson.com 返回 isDeleted: true
            assert body.get('isDeleted') is True or 'id' in body,f'应确认删除状态'