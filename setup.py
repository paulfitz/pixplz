#!/usr/bin/env python

from setuptools import setup

install_requires = [
    "Pillow",
    "requests",
    "six",
    "tqdm"
]

setup(name="pixplz",
      version="0.0.6",
      author="Paul Fitzpatrick",
      author_email="paulfitz@alum.mit.edu",
      description="Fetch some images to use as casual training data",
      packages=['pixplz'],
      entry_points={
          "console_scripts": [
              "pixplz=pixplz.fetch:main",
              "mp3plz=pixplz.fetch_audio:main"
          ]
      },
      install_requires=install_requires,
      extras_require={
          'parallel': [
              "grequests"
          ]
      },
      url="https://github.com/paulfitz/pixplz"
)
