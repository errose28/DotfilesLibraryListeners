from setuptools import setup

setup(
  name = 'DotfilesLibraryListeners',
  version = '0.0.1',
  author = 'Ethan Rose',
  author_email = 'errose28@gmail.com',
  packages = setuptools.find_packages(),
  url = 'https://github.com/errose28/DotfilesLibraryListeners',
  description = 'Robot Framework listeners for robot framework DotfilesLibrary.',
  long_description = open('README.md').read(),
  license = 'Apache License 2.0',
  platforms = 'any',
  classifiers = [
    "Programming Language :: Python :: 3 :: Only",
    "License :: OSI Approved :: Apache Software License",
    "Operating System :: OS Independent",
    "Framework :: Robot Framework"
    "Framework :: Robot Framework :: Library"
  ],
  python_requires = '>=3.9, <4',
  install_requires = [ "robotframework" ]
)
