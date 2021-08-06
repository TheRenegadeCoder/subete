from .repo import *

def load(source_dir: str = None) -> Repo:
    """
    Loads the Sample Programs repo as a Repo object.

    :return: the Sample Programs repo as a Repo object
    """
    return Repo(source_dir=source_dir)
