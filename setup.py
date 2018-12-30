import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="downer",
    version="0.0.1",
    author="James Craver",
	url='https://github.com/jcraver1021/downer.git',
    description="Bulk HTML downloader",
    packages=setuptools.find_packages(),
	package_data={
		'': ['*.txt'],
	},
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)