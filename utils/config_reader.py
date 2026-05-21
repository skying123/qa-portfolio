import os
import configparser
from typing import Dict,Any

def get_config(env : str = 'dev') -> configparser.ConfigParser:
    """
    读取指定环境的ini配置文件
    :param env: 环境标示，对应config/{env}.ini文件
    :return: ConfigParser对象
    """
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(root_dir,'config',f'{env}.ini')

    if not os.path.exists(config_path):
        raise FileNotFoundError(f'配置文件不存在:{config_path}')
    
    config = configparser.ConfigParser()
    config.read(config_path,encoding='utf-8')
    return config

def get_api_config(env:str='dev') -> Dict[str,Any]:
    """
    提取[API]配置信息
    :param env: 环境标示，对应config/{env}.ini文件
    :return: 字典
    """
    config = get_config(env)
    return{
        'base_url':config.get('api','base_url'),
        'timeout':config.getint('api','timeout',fallback=10)
    }

def get_ui_config(env:str='dev') -> Dict[str,Any]:
    """
    提取[UI]配置信息
    :param env: 环境标示，对应config/{env}.ini文件
    :return: 字典
    """
    config = get_config(env)
    return{
        'base_url':config.get('ui','base_url'),
        'browser':config.get('ui','browser'),
        'headless':config.getboolean('ui','headless',fallback=True),
        'driver_path':config.get('ui','driver_path',fallback="").strip()
    }