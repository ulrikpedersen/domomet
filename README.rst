homeapp
===========================

|code_ci| |docs_ci| |coverage| |pypi_version| |license|

This is my own Home monitoring app.

============== ==============================================================
pip            ``pip install git+https://github.com/ulrikpedersen/homeapp.git``
Source code    https://github.com/ulrikpedersen/homeapp
Documentation  https://ulrikpedersen.github.io/homeapp
Releases       https://github.com/ulrikpedersen/homeapp/releases
============== ==============================================================

Example use:

.. code-block:: python

    from homeapp import __version__

    print(f"Hello homeapp {__version__}")

Or if it is a commandline tool then you might put some example commands here::

    $ python -m homeapp --version

.. |code_ci| image:: https://github.com/ulrikpedersen/homeapp/actions/workflows/code.yml/badge.svg?branch=main
    :target: https://github.com/ulrikpedersen/homeapp/actions/workflows/code.yml
    :alt: Code CI

.. |docs_ci| image:: https://github.com/ulrikpedersen/homeapp/actions/workflows/docs.yml/badge.svg?branch=main
    :target: https://github.com/ulrikpedersen/homeapp/actions/workflows/docs.yml
    :alt: Docs CI

.. |coverage| image:: https://codecov.io/gh/ulrikpedersen/homeapp/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/ulrikpedersen/homeapp
    :alt: Test Coverage

.. |pypi_version| image:: https://img.shields.io/pypi/v/homeapp.svg
    :target: https://pypi.org/project/homeapp
    :alt: Latest PyPI version

.. |license| image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg
    :target: https://opensource.org/licenses/Apache-2.0
    :alt: Apache License

..
    Anything below this line is used when viewing README.rst and will be replaced
    when included in index.rst

See https://ulrikpedersen.github.io/homeapp for more detailed documentation.
