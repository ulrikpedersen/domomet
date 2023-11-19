import logging
import time
from pprint import pformat

from influxdb_client import InfluxDBClient
from influxdb_client.client.exceptions import InfluxDBError
from influxdb_client.client.write_api import WriteOptions, WriteType

from . import sensor


class InfluxDbRecorder:
    _influxdb_org = "Household"
    # measurement -> bucket
    _influxdb_measurement_buckets = {
        "Electricity": "Energy",
        "Temperature": "Environment",
    }

    def __init__(self, sensor: sensor.Publisher) -> None:
        self._sensor = sensor

    def __str__(self) -> str:
        s = f"< InfluxDbRecorder: sensor:<{self._sensor}> >"
        return s

    def run(self, influxdb_token: str, influxdb_url: str) -> None:
        try:
            with InfluxDBClient(
                url=influxdb_url, token=influxdb_token, org=self._influxdb_org
            ) as idb_client:
                with idb_client.write_api(
                    write_options=WriteOptions(batch_size=1),
                    write_type=WriteType.synchronous,
                ) as idb_writer:
                    while True:
                        try:
                            measurement: dict = self._sensor.get_reading()
                        except TimeoutError:
                            continue
                        logging.info("Got measurement for recording: \n"
                                     f"{pformat(measurement)}")
                        idb_writer.write(
                            self._influxdb_measurement_buckets[
                                measurement["measurement"]
                            ],
                            self._influxdb_org,
                            record=measurement,
                        )
                        time.sleep(2)
        except InfluxDBError as e:
            logging.exception("Influx DB error caught. Re-raising")
            raise e
