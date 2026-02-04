#! python3
# -*- encoding: utf-8 -*-

from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings


class DatabaseConfig(BaseSettings):
    """单个数据库配置模型"""
    NAME: str = Field(..., description="数据库别名/标识名称")
    URL: str = Field(..., description="数据库连接URL")
    DRIVER: Optional[str] = Field(default=None, description="数据库驱动")
    POOL_SIZE: int = Field(default=5, description="连接池大小")
    MAX_OVERFLOW: int = Field(default=10, description="最大溢出连接数")
    POOL_RECYCLE: int = Field(default=3600, description="连接回收时间(秒)")
    ECHO: bool = Field(default=False, description="是否输出SQL日志")

