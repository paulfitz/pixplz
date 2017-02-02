#!/usr/bin/env python

import sys
from setuptools import setup

install_requires = [
    "grequests",
    "Pillow",
    "requests",
    "six",
    "tqdm"
]

setup(name="pixplz",
      version="0.0.1",
      author="Paul Fitzpatrick",
      author_email="paulfitz@alum.mit.edu",
      description="Fetch some images to use as casual training data",
      packages=['pixplz'],
      entry_points={
          "console_scripts": [
              "pixplz=pixplz.fetch:main"
          ]
      },
      install_requires=install_requires,
      url="https://github.com/paulfitz/pixplz"
)
