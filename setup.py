from setuptools import setup, find_packages

import ast
import sys


def readme():
    with open('README.rst', 'r', encoding='utf-8') as f:
        return f.read()


def get_version():
    filename = 'iso20275/__init__.py'
    with open(filename, 'r') as f:
        tree = ast.parse(f.read(), filename)
        for node in tree.body:
            if (isinstance(node, ast.Assign) and
                    node.targets[0].id == '__version__'):
                version = ast.literal_eval(node.value)
        if isinstance(version, tuple):
            version = '.'.join([str(x) for x in version])
        return version


def get_install_requirements():
    return ['setuptools']


setup(
    name='iso-20275',
    version=get_version(),
    description='ISO 20275 Entity Legal Type package for Python',
    long_description=readme(),
    license='MIT',
    author='Youri Hubaut',
    packages=find_packages(),
    package_data={'iso20275': ['ISO-20275 - 2019-11-06.csv', 'Cleaned - ISO-20275 - 2019-11-06.csv']},
    url='https://github.com/Gawaboumga/iso-20275-python',
    keywords='internationalization i18n elf iso20275 entity legal types',
    install_requires=get_install_requirements(),
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: Stackless',
        'Topic :: Software Development :: Internationalization',
    ]
)
