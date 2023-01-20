from importlib.metadata import version

__version__ = version("homeapp")
del version

__all__ = ["__version__"]
