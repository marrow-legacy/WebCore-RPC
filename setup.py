#!/usr/bin/env python

from setuptools import setup, find_packages
import sys, os

if sys.version_info <= (2, 5):
    raise SystemExit("Python 2.5 or later is required.")

execfile(os.path.join("web", "extras", "xmlrpc", "release.py"))

setup(
        name = name,
        version = version,
        
        description = summary,
        long_description = description,
        author = author,
        author_email = email,
        url = url,
        download_url = download_url,
        license = license,
        keywords = '',
        
        install_requires = [
                'YAPWF'
            ],
        
        test_suite = 'nose.collector',
        
        classifiers = [
                "Development Status :: 1 - Planning",
                "Environment :: Console",
                "Framework :: YAPWF",
                "Intended Audience :: Developers",
                "License :: OSI Approved :: BSD License",
                "Operating System :: OS Independent",
                "Programming Language :: Python",
                "Topic :: Internet :: WWW/HTTP :: WSGI",
                "Topic :: Software Development :: Libraries :: Python Modules"
            ],
        
        packages = find_packages(exclude=['tests']),
        include_package_data = True,
        zip_safe = False,
        
        namespace_packages = [
                'web',
                'web.extras'
            ]
    )
