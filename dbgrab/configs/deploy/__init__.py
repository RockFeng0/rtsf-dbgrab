from pydantic import Field
from pydantic_settings import BaseSettings


class DeploymentConfig(BaseSettings):
    """ 应用部署配置信息 """

    CURRENT_VERSION: str = Field(
        description="dbgrab版本信息",
        default="1.1.0",
    )

    DEBUG: bool = Field(
        description="是否开启调试模式",
        default=False,
    )


class FetcherConfig(BaseSettings):
    """ 工作路径基本配置 """
    WORK_PATH: str = Field(..., description="工作路径")
    LOG_PATH: str = Field(..., description="日志路径")
    FILE_PATH: str = Field(..., description="文件保存的路径")


class DeployConfig(
    DeploymentConfig,
    FetcherConfig,
):
    pass