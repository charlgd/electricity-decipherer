from setuptools import find_packages
from setuptools import setup

with open("requirements.txt") as f:
    content = f.readlines()
requirements = [x.strip() for x in content if "git+" not in x]

setup(name='decipherer',
      version="0.0.1",
      description="Electricity Decipherer",
      license="UNLICENSED",
      author="Decipherers",
      author_email="email@decipherer.com",
      url="https://github.com/charlgd/electricity-decipherer.git",
      install_requires=requirements,
      packages=find_packages(),
      #include_package_data: to install data from MANIFEST.in
      include_package_data=True,
      zip_safe=False
)
