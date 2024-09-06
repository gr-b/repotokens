from setuptools import setup

setup(
    name='repotokens',
    version='1.0.0',
    description="Count number of LLM tokens of source files contained in the repository / folder",
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