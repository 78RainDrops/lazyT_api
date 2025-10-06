from setuptools import setup, find_packages

setup(
    name="lazyT_api",
    version="1.0",
    description="A task manager REST API built with django and django rest framework",
    author="78RainDrops",
    author_email="smileyrence3@gmailcom",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Django>=5.0",
    ],
    entry_point={
        "console_scripts": [
            "taskapi=manage:main",
        ],
    },
)
