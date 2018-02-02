from setuptools import setup, find_packages

NAME = 'seawatch'

requirements = list(open('requirements.txt', 'r').readlines())

setup(
    name=NAME,
    version='0.1',
    description="Simple observer that rebuilds and updates single Docker services when their code changes.",
    url='https://github.com/flosch/seawatch',
    author='Florian Schäfer',
    author_email='florian.joh.schaefer@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=requirements,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'seawatch = seawatch.__main__:main',
        ]
    }
)
