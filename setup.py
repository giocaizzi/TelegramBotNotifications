from setuptools import setup, find_packages

# read the contents of your README file
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="TelegramBotNotifications",
    version="0.0.2",
    description="",
    long_description_content_type="text/markdown",
    long_description=long_description,
    url="https://github.com/giocaizzi/TelegramBotNotifications",
    author="giocaizzi",
    author_email="giocaizzi@gmail.com",
    packages=find_packages(include=["TelegramBotNotifications", "TelegramBotNotifications.*"]),
    setup_requires=[],
    tests_require=[],
    install_requires=[
        "python_telegram_bot",
        "pandas",
        "numpy",
    ],
    extras_require={"dev": [],},
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        ],
    project_urls={
        "Documentation": "https://giocaizzi.github.io/TelegramBotNotifications/",
        "Bug Reports": "https://github.com/giocaizzi/TelegramBotNotifications/issues",
        "Source": "https://github.com/giocaizzi/TelegramBotNotifications",
        },
)
