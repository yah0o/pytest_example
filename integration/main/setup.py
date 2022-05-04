import os

import setuptools

version = os.getenv('FREYA_VERSION', '0.0.0')
if 'latest' in version:
    version = '0.0.0'

setuptools.setup(
    name='freya-tests',
    version=version,
    description='Network Platform Environment Tests',
    author='Freya Network Platform Team',
    author_email='network_platform_team@wargaming.net',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Frameworks',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    packages=setuptools.find_packages()
)
