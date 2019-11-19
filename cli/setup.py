import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setuptools.setup(
    name="teleserver",
    py_modules=['teleserver'],
    version="0.0.5",
    author="Szymon Piotr Krasuski",
    description="CLI tool to teleserver project.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Dysproz/teleserver",
    packages=setuptools.find_packages(exclude=("tests",)),
    install_requires=required,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.6',
    entry_points='''
    [console_scripts]
    teleserver=teleserver:teleserver.cli
    '''
)
