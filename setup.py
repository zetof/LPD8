import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lpd8",
    version="1.0.3",
    author="Christophe Bury",
    author_email="zetof@zetof.net",
    description="A Python library to drive an AKAI LPD8 pad controller",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zetof/LPD8",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'python-rtmidi',
    ],
    python_requires='>=3.6',
)