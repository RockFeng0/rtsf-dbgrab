#! python3
# -*- encoding: utf-8 -*-

import os
from functools import lru_cache
from typing import Dict, Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from dbgrab.configs.deploy import DeployConfig
from dbgrab.configs.middleware import DynamicDBConfig


@lru_cache()
def get_db_config(env_file: Optional[str] = None) -> DynamicDBConfig:
    """获取数据库配置（带缓存）"""
    if env_file:
        DynamicDBConfig.set_env_file(env_file)

    current_env_file = DynamicDBConfig.get_env_file()

    # 动态创建配置类
    class EnvironmentAwareConfig(
        DeployConfig,
        DynamicDBConfig,
    ):
        model_config = SettingsConfigDict(
            env_file=current_env_file,
            env_file_encoding='utf-8',
            case_sensitive=True,
            extra='ignore',
            env_prefix='DB_ENGINE_',
            env_nested_delimiter='__',
        )
    return EnvironmentAwareConfig()


def clear_config_cache():
    """清除配置缓存"""
    get_db_config.cache_clear()
