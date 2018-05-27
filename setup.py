import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

cur_classifiers = [
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Topic :: Software Development :: Libraries",
    "Topic :: Utilities",
]

setuptools.setup(
    name="ppl",
    version="0.1.0",
    author='Abin Simon',
    author_email='abinsimon10@gmail.com',
    description="A pretty progressbar library",
    url="https://github.com/meain/ppl",
    long_description=long_description,
    packages=setuptools.find_packages(),
    keywords=['progressbar', 'spinner', 'loader'],
    classifiers=cur_classifiers)
