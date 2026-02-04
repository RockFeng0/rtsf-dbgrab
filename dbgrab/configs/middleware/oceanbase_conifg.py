#! python3
# -*- encoding: utf-8 -*-

from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings


class OceanbaseConfig(BaseSettings):
    """ 单个oceanbase oracle模式数据库  """
    # jdbc:oceanbase://localhost:2883/OCEANBASE_DB?useUnicode=true&characterEncoding=UTF-8&rewriteBatchedStatements=true
    JDBC: str = Field(..., description="数据库连接jdbc URL")

    # username@tenantname#clustername
    USERNAME: str = Field(..., description="用户名@租户名#集群名")
    PASSWORD: str = Field(..., description="密码")

    # com.oceanbase.jdbc.Driver
    DRIVER: str = Field(..., description="OceanBase驱动程序名称")

    # /soft/oceanbase/oceanbase-client-2.4.9.jar
    CLIENT_JAR: str = Field(..., description="OceanBase客户端jar包")


