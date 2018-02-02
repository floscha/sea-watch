from setuptools import setup, find_packages

NAME = 'seawatch'

requirements = list(open('requirements.txt', 'r').readlines())

setup(
    name=NAME,
    version='0.1',
    description="High-level API for Pyplot to easily create beautiful graphs.",
    url='https://github.com/flosch/pewdieplot',
    author='Florian Schäfer',
    author_email='florian.joh.schaefer@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=requirements,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'seawatch = run:main',
        ]
    }
)
