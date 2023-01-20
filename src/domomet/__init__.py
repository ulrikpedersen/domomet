from importlib.metadata import version

__version__ = version("domomet")
del version

__all__ = ["__version__"]
