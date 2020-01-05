import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name = 'symboard',
    version = '0.2.0',
    author = 'Andrew J. Young',
    author_email = 'andrewjunyoung1@gmail.com',
    description = 'A text-based keyboard layout creator. Change or add keys ' \
        'to your keyboard with ease.',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/andrewjunyoung/symboard',
    packages = setuptools.find_packages(),
    classifiers = [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires = '>=3.6',
)
