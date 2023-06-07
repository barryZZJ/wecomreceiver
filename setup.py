from setuptools import setup, find_packages

setup(
    name='wecomreceiver',
    version='0.1',
    author='Barry ZZJ',
    description='wecom app message listener',
    packages=find_packages(),
    install_requires=[
        # list any dependencies your package requires
        'flask',
        'loguru'
    ],
)
