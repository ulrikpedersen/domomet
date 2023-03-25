import logging
import os
from argparse import ArgumentParser

from dotenv import load_dotenv

from . import __version__, recorder, wirelesssensor

__all__ = ["main"]


def main(args=None):
    logging.basicConfig(
        level=logging.DEBUG,
        format="'%(asctime)s - %(levelname)s - %(name)s - %(filename)s:%(lineno)d - %(message)s'",  # noqa: E501
        datefmt="%d/%m/%Y %H:%M:%S",
    )
    parser = ArgumentParser()
    parser.add_argument("--version", action="version", version=__version__)
    args = parser.parse_args(args)
    load_dotenv()

    influxdb_TOKEN = os.getenv("INFLUXDB_TOKEN")
    influxdb_url = os.getenv("INFLUXDB_URL")
    logging.debug(f"IDB URL: {influxdb_url}")
    meas = wirelesssensor.Measure()
    meas.start_collecting()
    idbrec = recorder.InfluxDbRecorder(meas)

    return idbrec.run(influxdb_TOKEN, influxdb_url)


# test with: python -m domomet
if __name__ == "__main__":
    main()
