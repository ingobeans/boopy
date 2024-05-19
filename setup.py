from setuptools import setup, find_packages

setup(
    name='boopy',
    version='0.3.3',
    packages=find_packages(),
    package_data={
        'boopy': ['monobit.ttf','icon.png'],
    },
    exclude_package_data={'': ['example.py']},
)