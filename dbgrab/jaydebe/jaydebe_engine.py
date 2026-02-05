import jaydebeapi
from jpype import JVMNotFoundException

# 创建连接
class JayDeBeEngine(object):
    def __init__(self, jdbc_driver_name, jdbc_url, jdbc_user, jdbc_password, jdbc_jar):
        """
        Args:
            jdbc_driver_name (str): 驱动名称, 如: com.oceanbase.jdbc.Driver
            jdbc_url (str):  jdbc URL, 如: jdbc:oceanbase://192.168.0.1:2883/TestDB?useUnicode=true&characterEncoding=UTF-8&rewriteBatchedStatements=true
            jdbc_user (str): 数据库用户名, 如: xx@xx#xx
            jdbc_password (str): 数据库密码, 如: 123456
            jdbc_jar (str): JDBC 驱动 JAR 文件路径, 如 /root/oceanbase-client-1.2.3.jar
        """
        self._jdbc_driver_name = jdbc_driver_name
        self._jdbc_url = jdbc_url
        self._jdbc_user = jdbc_user
        self._jdbc_password = jdbc_password
        self._jdbc_jar = jdbc_jar

    def connect(self):
        try:
            conn = jaydebeapi.connect(
                self._jdbc_driver_name, self._jdbc_url, [self._jdbc_user, self._jdbc_password], self._jdbc_jar
                )
        except JVMNotFoundException as e:
            raise JVMNotFoundException(f"{e}\njpype.startJVM启动失败，请检查JAVA_HOME配置. 如:os.environ['JAVA_HOME']='~/anaconda3/envs/dcapp'")
        return conn

    def raw_connection(self):
        return self.connect()

    def __repr__(self):
        return f"<JayDeBeEngine(jdbc_url='{self._jdbc_url}', user='{self._jdbc_user}')>"