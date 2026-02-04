#! python3
# -*- encoding: utf-8 -*-
class DynamicDBError(Exception):
    """动态数据库包基础异常"""
    pass

class ConfigError(DynamicDBError):
    """配置相关异常"""
    pass

class EngineError(DynamicDBError):
    """引擎相关异常"""
    pass

class ConnectionError(DynamicDBError):
    """连接相关异常"""
    pass