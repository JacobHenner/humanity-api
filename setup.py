from setuptools import setup

setup(
    name="humanity-api",
    version="0.0.1-dev",
    description="API wrapper for Humanity (ShiftPlanning) APIv2",
    url="https://github.com/JacobHenner/humanity-api",
    author="Jacob Henner",
    author_email="code@ventricle.us",
    long_description=open("README.md").read(),
    license="MIT",
    packages=["humanity"],
    install_requires=["requests", "arrow"],
)
