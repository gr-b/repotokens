from setuptools import setup

setup(
    name='repotokens',
    version='1.0.0',
    py_modules=['repotokens'],
    install_requires=[
        'tiktoken',
    ],
    entry_points={
        'console_scripts': [
            'repotokens=repotokens:main',
        ],
    },
)