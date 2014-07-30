#!/usr/bin/env python

try:
    from setuptools import setup, find_packages
except ImportError:
    raise ImportError("Could not import \"setuptools\". Please install the setuptools package.")


packages = find_packages(where=".", exclude=('tests', 'bin', 'docs', 'fixtures',))

requires = []

with open('requirements.txt', 'r') as reqfile:
    for line in reqfile:
        requires.append(line.strip())

classifiers = (
    'Development Status :: 1 - Planning',
    'Environment :: Web Environment',
    'Environment :: Console',
    'Enivronment :: No Input/Output (Daemon)',
    'Intended Audience :: Developers',
    'License :: Other/Proprietary License',
    'Natural Language :: English',
    'Operating System :: MacOS :: MacOS X',
    'Operating System :: POSIX :: Linux',
    'Programming Language :: Python :: 2.7',
)

config = {
    "name": "Huduku",
    "version": "0.1",
    "description": "A keyword/faceted search django app for CPS data",
    "author": "Keshav Magge",
    "author_email": "keshav@cobrain.com",
    "url": "https://github.com/cobrain-labs/huduku/",
    "packages": packages,
    "install_requires": requires,
    "classifiers": classifiers,
    "zip_safe": False,
}

setup(**config)
