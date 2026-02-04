from setuptools import setup, find_packages

setup(
    name="dbgrab",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "jaydebeapi>=1.2.3",
        "oracledb>=3.4.2",
        "pandas>=3.0.0",
        "psycopg2>=2.9.11",
        "pydantic-settings>=2.12.0",
        "pymysql>=1.1.2",
        "rtsf>=3.0.2",
        "setuptools>=80.10.1",
        "sqlalchemy>=2.0.46",
        "tqdm>=4.67.1",
    ],
    author="",
    author_email="",
    description="SQL Fetcher SDK for risk control AI",
    long_description="",
    long_description_content_type="text/markdown",
    url="",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)