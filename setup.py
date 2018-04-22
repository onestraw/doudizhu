# -*- coding: utf-8 -*-

from setuptools import setup


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='doudizhu',
    version='0.1.4',
    description='doudizhu engine',
    long_description=readme,
    url='https://github.com/onestraw/doudizhu',
    author='onestraw',
    author_email='hexiaowei91@gmail.com',
    packages=['doudizhu'],
    license=license,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2',
    ],)
