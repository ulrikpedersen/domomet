from argparse import ArgumentParser

from . import __version__, receiverfxtrx433e

__all__ = ["main"]


def main(args=None):
    parser = ArgumentParser()
    parser.add_argument("--version", action="version", version=__version__)
    args = parser.parse_args(args)
    return receiverfxtrx433e.main()


# test with: python -m domomet
if __name__ == "__main__":
    main()
