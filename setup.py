import os

from setuptools import find_packages, setup

# Try to load the version from a datafile in the package
package_version = "1.0"

# read the contents of your README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="anomark",
    version=package_version,
    description="ANSSI - AnoMark",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/ANSSI-FR/AnoMark/",
    author="https://github.com/ajunius-ANSSI",
    author_email="<TODO>",
    license="MIT",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords="<TODO>",
    packages=find_packages(
        exclude=[
            'tests/*',
        ]
    ),
    install_requires=[
        "certifi==2021.10.8",
        "numpy==1.26.3",
        "pandas==1.4.2",
        "python-dateutil==2.8.2",
        "pytz==2022.1",
        "six==1.16.0",
        "tqdm==4.64.0",
    ],
    extra_requires={
    },
    package_data={
        '': [
            "*.xml",
        ]
    }
)
