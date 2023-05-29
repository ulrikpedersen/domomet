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
    # if log_level not in logging.getLevelNamesMapping():  # only available from Python 3.11
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

        syslog = SysLogHandler(address=env_syslog_address_port.split(":"))
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
    meas = wirelesssensor.Measure()
    meas.start_collecting()
    idbrec = recorder.InfluxDbRecorder(meas)

    return idbrec.run(influxdb_TOKEN, influxdb_url)


# test with: python -m domomet
if __name__ == "__main__":
    main()
