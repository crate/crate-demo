from setuptools import setup, find_packages

requirements = [
    'crate>=0.11.2',
]

setup(name='github-demo',
  version='0.1.0',
  platforms=['any'],
  py_modules=['s3tocrate'],
  entry_points={
    'console_scripts': ['imp = s3tocrate:main'],
  },
  install_requires=requirements,
)
