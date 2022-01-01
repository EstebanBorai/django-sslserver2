import sslserver2

from pathlib import Path
from setuptools import setup, find_packages

CWD = Path(__file__).parent

README = (CWD / "README.md").read_text()

setup(
    author="Esteban Borai",
    author_email="estebanborai@gmail.com",
    description="Django package to support both HTTP and HTTPS as runserver command",
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.10",
    ],
    include_package_data=True,
    install_requires=["django >= 3"],
    license="MIT",
    long_description=README,
    long_description_content_type="text/markdown",
    name="django-sslserver2",
    packages=["sslserver2"],
    url="https://github.com/EstebanBorai/django-sslserver2",
    version=sslserver2.__version__,
)
