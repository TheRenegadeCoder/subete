import setuptools

cmdclass = {}

try:
    from sphinx.setup_command import BuildDoc
    cmdclass['build_sphinx'] = BuildDoc
except ImportError:
    print("WARNING: sphinx not available")

with open("README.md", "r") as fh:
    long_description = fh.read()

MAJOR = 0
MINOR = 6
PATCH = 0

name = "subete"
version = f"{MAJOR}.{MINOR}"
release = f"{MAJOR}.{MINOR}.{PATCH}"
setuptools.setup(
    name=name,
    version=release,
    author="The Renegade Coder",
    author_email="jeremy.grifski@therenegadecoder.com",
    description="The Sample Programs API in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TheRenegadeCoder/subete",
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires=[
        "PyYAML>=5",
        "GitPython>=3"
    ],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
        "Topic :: Documentation :: Sphinx",
        "Development Status :: 3 - Alpha"
    ],
    cmdclass=cmdclass,
    command_options={
        'build_sphinx': {
            'project': ('setup.py', name),
            'version': ('setup.py', version),
            'release': ('setup.py', release),
            'source_dir': ('setup.py', 'docs'),
            'build_dir': ('setup.py', 'docs'),
            'builder': ("setup.py", "dirhtml")
        }
    }
)
