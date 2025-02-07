from setuptools import setup, find_packages

setup(
    name="bounceinsights",
    version="0.0.0",
    author="Rajesh Goldy",
    author_email="goldirana3210@gmail.com",
    packages=find_packages(include=["backend*", "frontend*"])
)