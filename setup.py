from setuptools import setup

setup(
    name='repotokens',
    version='1.0.1',
    description="Count number of LLM tokens of source files contained in the repository / folder",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
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