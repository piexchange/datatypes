
import os.path
import setuptools
import sys


HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


author = "Aran-Fey"

with open(HERE+"/README.md") as file:
    long_description = file.read()

packages = setuptools.find_packages()
name = packages[0]
module = __import__(name)

setuptools.setup(
    name=name,
    version=module.__version__,
    author=author,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/{}/{}".format(author, name),
    packages=packages,
    install_requires=['introspection @ https://github.com/Aran-Fey/introspection.git#egg=introspection'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
