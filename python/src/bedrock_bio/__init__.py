from importlib.metadata import version

__version__ = version("bedrock-bio")

from .list_datasets import list_datasets
from .load_dataset import load_dataset

__all__ = ["list_datasets", "load_dataset"]
