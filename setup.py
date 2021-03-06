import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="oigusakt-kaarelp2rtel", # Replace with your own username
    version="1.4.0",
    author="Kaarel Pärtel",
    author_email="kaarelp2rtel@gmail.com",
    description="XML Mapper for Riigiteataja legal acts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/KaarelP2rtel/oigusakt",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPLv3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['cached_property'],

)