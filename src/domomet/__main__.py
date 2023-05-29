import logging
import os
import socket
from argparse import ArgumentParser
from logging.handlers import SysLogHandler

from dotenv import load_dotenv

from . import __version__, recorder, wirelesssensor

__all__ = ["main"]


def main(args=None):
    log_level = os.getenv("DOMOMET_LOGLEVEL", default=logging.DEBUG)
    # only available from Python 3.11:
    # if log_level not in logging.getLevelNamesMapping():
    if log_level not in ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET"]:
        log_level = logging.DEBUG
    logging.basicConfig(
        level=logging.DEBUG,
        format="'%(asctime)s - %(levelname)s - %(name)s - %(filename)s:%(lineno)d - %(message)s'",  # noqa: E501
        datefmt="%d/%m/%Y %H:%M:%S",
    )

    env_syslog_address_port = os.getenv("DOMOMET_SYSLOG_ADDR_PORT", default=None)
    if env_syslog_address_port is not None:

        class ContextFilter(logging.Filter):
            hostname = socket.gethostname()

            def filter(self, record):
                record.hostname = ContextFilter.hostname
                return True

        addr, port = env_syslog_address_port.split(":")
        port = int(port)
        syslog = SysLogHandler(
            address=(
                addr,
                port,
            )
        )
        syslog.addFilter(ContextFilter())
        format = "%(asctime)s %(hostname)s DOMOMET: %(message)s"
        formatter = logging.Formatter(format, datefmt="%b %d %H:%M:%S")
        syslog.setFormatter(formatter)
        logger = logging.getLogger()
        logger.addHandler(syslog)
        logger.setLevel(log_level)

    parser = ArgumentParser()
    parser.add_argument("--version", action="version", version=__version__)
    args = parser.parse_args(args)
    load_dotenv()

    influxdb_TOKEN = os.getenv("INFLUXDB_TOKEN")
    influxdb_url = os.getenv("INFLUXDB_URL")
    logging.debug(f"IDB URL: {influxdb_url}")
    logging.info("Connecting to wireless sensor")
    meas = wirelesssensor.Measure()
    logging.info("Starting listening for measurements")
    meas.start_collecting()
    idbrec = recorder.InfluxDbRecorder(meas)
    logging.info("Starting to record to influxdb")
    return idbrec.run(influxdb_TOKEN, influxdb_url)


# test with: python -m domomet
if __name__ == "__main__":
    main()
