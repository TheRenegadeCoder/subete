import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="subete",
    version="0.1.0",
    author="The Renegade Coder",
    author_email="jeremy.grifski@therenegadecoder.com",
    description="The Sample Programs API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TheRenegadeCoder/subete",
    packages=setuptools.find_packages(),
    install_requires=[],
    classifiers=(
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ),
)
