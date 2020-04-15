from setuptools import find_packages
from setuptools import setup

setup(
    name='utils',
    version='0.0.37',
    description='Common helper functions for Alana bots',
    author='Ondrej Dusek, Ioannis Papaioannou, Alessandro Suglia, Igor Shalyminov',
    author_email='ipapaioannou83@gmail.com',
    url='https://github.com/WattSocialBot/utils',
    download_url='https://github.com/WattSocialBot/utils.git',
    license='MIT',
    packages=find_packages(),
    package_data={'utils': ['profanities/*.txt']},
    install_requires=["flask_restful",
                      "requests",
                      "unidecode",
                      "watchtower",
                      "pytest"]
    )
