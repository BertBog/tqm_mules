from pathlib import Path

from setuptools import setup, find_packages

from tqmmules.version import __version__

with open(Path(__file__).parent / 'README.md', encoding='utf-8') as handle:
    long_description = handle.read()


setup(
    name='tqmmules',
    version=__version__,
    description='TQM mules is a package to parse save files from the mobile version of Titan Quest Legendary Edition.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/BertBog/tqm_mules',
    author='Bert Bogaerts',
    license='MIT',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
    ],
    keywords='titan quest legendary edition',
    packages=find_packages() + ['tqmmules.data'],
    python_requires='>=3',
    install_requires=[],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'parse_saves.py=tqmmules.scripts.parse_saves:run',
        ],
    }
)
