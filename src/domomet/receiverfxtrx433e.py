import atexit
import datetime
import logging
import os
import sys
import time

import RFXtrx
from dotenv import load_dotenv
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.exceptions import InfluxDBError
from influxdb_client.client.write_api import WriteApi, WriteOptions, WriteType

_influxdb_org = "Household"
_influxdb_bucket = "Energy"


def on_exit(db_client: InfluxDBClient, write_api: WriteApi) -> None:
    write_api.close()
    db_client.close()


class CallbackHandler:
    def __init__(self, idb_writer: WriteApi) -> None:
        self.callcounter: int = 0
        self.idb_writer = idb_writer

    def callback_event(self, event: RFXtrx.SensorEvent) -> None:
        print("===== callback_event ======")
        self.callcounter += 1
        data_influxdb_dict = sensor_event_to_influxdb_dict(event)
        logging.debug(data_influxdb_dict)
        datapoint: Point = Point.from_dict(data_influxdb_dict)
        logging.debug(datapoint)

        # use only one of these...
        # self.idb_writer.write(_influxdb_bucket, _influxdb_org, record=datapoint)
        self.idb_writer.write(
            _influxdb_bucket, _influxdb_org, record=data_influxdb_dict
        )


def sensor_event_to_influxdb_dict(event: RFXtrx.SensorEvent) -> dict:
    sensor_data: dict = event.values
    sensor_device: RFXtrx.RFXtrxDevice = event.device
    result = {
        "measurement": "Electricity",
        "tags": {
            "device_make": "OWL",
            "device_type": sensor_device.type_string,
            "device_id": sensor_device.id_string,
        },
        "fields": {
            "power": sensor_data["Energy usage"],  # Watt (int)
            "consumption_total": sensor_data["Total usage"],  # Watt-hours Wh (float)
            "signal_strenght": sensor_data["Rssi numeric"],  # 0-9(?) (int)
            "sensor_battery": sensor_data["Battery numeric"],  # 0-x(?) (int)
        },
        "time": datetime.datetime.now(datetime.timezone.utc),
    }
    return result


def main():
    logging.basicConfig(level=logging.DEBUG)
    load_dotenv()

    if len(sys.argv) >= 2:
        rfxcom_device = sys.argv[1]
    else:
        rfxcom_device = "/dev/cu.usbserial-A1XPT51E"

    modes_list = sys.argv[2].split() if len(sys.argv) > 2 else ["oregon"]
    logging.debug(f"RFXcom serial device: {rfxcom_device} modes: {modes_list}")

    _influxdb_TOKEN = os.getenv("INFLUXDB_TOKEN")
    _influxdb_url = os.getenv("INFLUXDB_URL")
    try:
        with InfluxDBClient(
            url=_influxdb_url, token=_influxdb_TOKEN, org=_influxdb_org
        ) as idb_client:
            with idb_client.write_api(
                write_options=WriteOptions(batch_size=1),
                write_type=WriteType.synchronous,
            ) as idb_writer:
                atexit.register(on_exit, idb_client, idb_writer)
                cb = CallbackHandler(idb_writer)
                core = RFXtrx.Core(rfxcom_device, cb.callback_event, modes=modes_list)
                logging.debug(core)

                while True:
                    # print(core.sensors())
                    print(".", end="")
                    time.sleep(2)
                print("")
    except InfluxDBError as e:
        logging.exception("Influx DB error caught. Re-raising")
        raise e


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
