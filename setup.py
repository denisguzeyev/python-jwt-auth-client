import os
from glob import glob
try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup

from setuptools import find_packages


install_requires = open("requirements/default.txt").readlines()
doc_requires = open("requirements/documentation.txt").readlines()
dev_requires = install_requires
console_scripts = []

options = {}

setup(name="jwt_auth_client",
      setup_requires=["setuptools_scm"],
      use_scm_version={"version_scheme": "guess-next-dev"},
      description="Nfon JWT auth client",
      author="Denis Guzeyev",
      author_email="denys.guzyeyew@nfon.com",
      url="https://stash.nfon.net/projects/PRESENCE/repos/python-nfon-jwt-auth-client/browse",# noqa
      platforms=["linux"],
      zip_safe=True,
      packages=find_packages(),
      data_files=[
          "jwt_conf.yaml",
      ],
      include_package_data=True,
      install_requires=install_requires,
      extras_require={},
      entry_points={
          "console_scripts": console_scripts,
      },
      **options)
