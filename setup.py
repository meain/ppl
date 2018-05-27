import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ppl",
    version="0.0.3",
    author = 'Abin Simon',
    author_email = 'abinsimon10@gmail.com',
    description="A pretty progressbar library",
    url="https://github.com/meain/ppl",
    packages=setuptools.find_packages(),
    keywords = ['progressbar', 'spinner', 'loader'],
)
