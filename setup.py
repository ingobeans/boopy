from setuptools import setup, find_packages

setup(
    name='boopy',
    version='0.1',
    packages=find_packages(),
    package_data={
        'boopy': ['monobit.ttf'],
    },
    exclude_package_data={'': ['example.py']},
)