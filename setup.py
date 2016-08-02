from setuptools import setup

setup(
    name='mu',
    version='0.1',
    py_modules=['ma_utils'],
    install_requires=['Click', 'colorama'],
    entry_points='''
        [console_scripts]
        mu=ma_utils:cli
    ''',
)