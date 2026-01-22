from setuptools import setup, find_packages

setup(
    name="dbgrab",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "sqlalchemy",
        "pandas",
        "jaydebeapi",
        "tqdm",
        "rtsf"
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