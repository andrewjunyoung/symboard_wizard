import setuptools
from symboard import __name__, __version__

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name=__name__,
    version=__version__,
    author='Andrew J. Young',
    author_email='andrewjunyoung1@gmail.com',
    description='A text-based keyboard layout creator. Change or add keys ' \
        'to your keyboard with ease.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/andrewjunyoung/symboard',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
