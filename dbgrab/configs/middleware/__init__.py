#! python3
# -*- encoding: utf-8 -*-

import os
from typing import Dict, Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from dbgrab.configs.middleware.database_conifg import DatabaseConfig
from dbgrab.configs.middleware.oceanbase_conifg import OceanbaseConfig


class DynamicDBConfig(BaseSettings):
    """动态数据库配置主类"""

    # 数据库配置字典, 传统数据库
    # noinspection PyDataclass
    DATABASES: Dict[str, DatabaseConfig] = Field(default_factory=dict)

    # 数据库配置字典, oceanbase oracle
    # noinspection PyDataclass
    OCEANBASES: Dict[str, OceanbaseConfig] = Field(default_factory=dict)

    model_config = SettingsConfigDict(
        env_file=None,  # 动态设置
        env_file_encoding='utf-8',
        extra='ignore',
        env_prefix='DB_ENGINE_',
        env_nested_delimiter='__',  # 嵌套模型分隔符
    )

    # 动态环境文件路径
    _custom_env_file: Optional[str] = None

    @classmethod
    def set_env_file(cls, env_file: str):
        """设置自定义环境文件"""
        if not os.path.exists(env_file):
            raise FileNotFoundError(f"环境文件不存在: {env_file}")
        cls._custom_env_file = env_file

    @classmethod
    def get_env_file(cls) -> Optional[str]:
        """获取当前环境文件路径"""
        return cls._custom_env_file
