from setuptools import setup, find_packages

setup(
    name='env_manager',
    version='0.1',
    py_modules=['env_manager'],
    entry_points={
        'console_scripts': [
            'env_manager=env_manager:main',
        ],
    },
    install_requires=[
        # List your dependencies here if any
    ],
)
