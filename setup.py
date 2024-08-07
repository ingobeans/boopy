from setuptools import setup, find_packages

setup(
    name='boopy',
    version='0.3.4',
    packages=find_packages(),
    package_data={
        'boopy': ['monobit.ttf','icon.png'],
    },
    exclude_package_data={'': ['example.py']},
    install_requires=[
        "pygame-ce>=2.5.0",
        "setuptools>=72.1.0",
    ],
)