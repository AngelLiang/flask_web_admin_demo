
from setuptools import setup, find_packages

setup(
    name="flask_app",
    version="0.0.1",
    packages=find_packages(),
    install_requires=["Flask"],
    include_package_data=True,
    zip_safe=False,
)
