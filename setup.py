# -*- coding: utf-8 -*-
'''
File Name: setup.py
Author: JackeyGao
mail: gaojunqi@outlook.com
Created Time: 二  8/ 2 15:27:49 2016
'''
from setuptools import setup, find_packages

version = '0.1'
description = "csvSQL 可以让你通过SQL来查看csv文件数据"

def fread(filepath):
    with open(filepath, 'r') as f:
        return f.read()

setup(
    name='csvsql',
    version=version,
    install_requires=[
        'argparse',
        'terminaltables'
    ],
    zip_safe=False,
    py_modules = ['csvsql'],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'csvsql = csvsql:handle_command_line',
        ]
    },
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],
    description=description,
    long_description=fread('README.md'),
    author='JackeyGao',
    author_email='gaojunqi@outlook.com',
    url='https://github.com/jackeygao/csvSQL',
)
