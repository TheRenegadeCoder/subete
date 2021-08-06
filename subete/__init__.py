from .repo import *

def load(source_dir: str = None) -> Repo:
    """
    Loads the Sample Programs repo as a Repo object. This is
    a convenience function which can be used to quickly generate
    an instance of the Sample Programs repo. 
    
    Assuming subete is imported, here's how you would use this function::

        repo = subete.load()

    Optionally, you can also provide a source directory which
    bypasses the need for git on your system::

        repo = subete.load(source_dir="path/to/sample-programs/archive")

    :return: the Sample Programs repo as a Repo object
    """
    return Repo(source_dir=source_dir)
