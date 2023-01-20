import subprocess
import sys

from domomet import __version__


def test_cli_version():
    cmd = [sys.executable, "-m", "domomet", "--version"]
    assert subprocess.check_output(cmd).decode().strip() == __version__
