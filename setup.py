import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mpb",
    version="0.0.3",
    author = 'Abin Simon',
    author_email = 'abinsimon10@gmail.com',
    description="A prettier progressbar library",
    url="https://github.com/meain/mpb",
    packages=setuptools.find_packages(),
    keywords = ['progressbar', 'spinner', 'loader'],
)
