#! python3
# -*- encoding: utf-8 -*-

import os


class ConfigGenerator:
    """
    配置文件生成器，基于模板生成database.yml和tables.yml配置文件
    """

    def __init__(self):
        """
        初始化配置生成器
        """
        self.template_dir = os.path.join(os.path.dirname(__file__), 'template')

    def get_template(self, template_name: str, output_path: str = None) -> None:
        """
        获取模板文件并保存到当前目录

        Args:
            template_name: 模板文件名
            output_path: 输出文件路径，如果为None则保存到当前目录
        """
        # 读取模板文件
        template_path = os.path.join(self.template_dir, template_name)
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()

        if output_path is None:
            output_path = os.path.join(os.getcwd(), template_name)

        # 写入输出文件
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(template_content)

    def gen_sql_template(self, output_path: str = None) -> None:
        self.get_template('tables.yml', output_path)

    def gen_env_template(self, output_path: str = None) -> None:
        self.get_template('.env.example', output_path)

