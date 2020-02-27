import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Spiky",
    version="0.0.1",
    author="Andre Theron",
    author_email="andretheronsa@gmail.com",
    description="Removes spikes from GeoPackage shapes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/andretheronsa/spiky",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        'geopandas>=0.7.0',
        'pygc>=1.1.0',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPL-2.0 License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)