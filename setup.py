#!/usr/bin/env python

from setuptools import setup, find_packages
import sys, os

if sys.version_info <= (2, 5):
    raise SystemExit("Python 2.5 or later is required.")

execfile(os.path.join("web", "extras", "rpc", "xml", "release.py"))

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
                "Development Status :: 4 - Beta",
                "Environment :: Web Environment",
                "Framework :: YAPWF",
                "Intended Audience :: Developers",
                "License :: OSI Approved :: MIT License",
                "Operating System :: OS Independent",
                "Programming Language :: Python",
                "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
                "Topic :: Software Development :: Libraries :: Python Modules",
                "Topic :: Text Processing :: Markup :: XML"
            ],
        
        packages = find_packages(exclude=['tests']),
        include_package_data = True,
        zip_safe = True,
        
        namespace_packages = [
                'web',
                'web.extras',
                'web.extras.rpc'
            ]
    )
