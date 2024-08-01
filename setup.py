from setuptools import setup, find_packages

setup(
    name='envlink',
    version='0.1',
    py_modules=['envlink'],
    entry_points={
        'console_scripts': [
            'envlink=envlink:main',
        ],
    },
    install_requires=[
        # List your dependencies here if any
    ],
)
