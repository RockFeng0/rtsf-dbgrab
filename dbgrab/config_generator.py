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

        # 确定输出路径
        if output_path is None:
            # 保存到当前目录
            output_path = os.path.join(os.getcwd(), template_name)

        # 写入输出文件
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(template_content)

    def get_database_template(self, output_path: str = None) -> None:
        """
        获取database.yaml模板并保存到当前目录

        Args:
            output_path: 输出文件路径，如果为None则保存到当前目录
        """
        self.get_template('database.yml', output_path)

    def get_tables_template(self, output_path: str = None) -> None:
        """
        获取tables.yaml模板并保存到当前目录

        Args:
            output_path: 输出文件路径，如果为None则保存到当前目录
        """
        self.get_template('tables.yml', output_path)

if __name__ == '__main__':
    # 初始化配置生成器
    generator = ConfigGenerator()

    # 获取database.yaml模板到当前目录
    generator.get_database_template("../temp/dev_database.yml")

    # 获取tables.yaml模板到当前目录
    generator.get_tables_template("../temp/dev_tables.yml")
