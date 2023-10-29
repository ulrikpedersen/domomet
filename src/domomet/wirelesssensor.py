import datetime
import logging
import os
import queue

import RFXtrx

from .sensor import Publisher

SENSOR_LOCATIONS = {"01": "bedroom", "02": "conservatory", "03": "garden"}


class BresserHygrometerMeasurement:
    CALIBRATION_TABLE = {
        "01": {"temperature_offset": -0.3, "humidity_offset": 0.0},
        "02": {"temperature_offset": 1.0, "humidity_offset": 2.0},
        "03": {"temperature_offset": 1.0, "humidity_offset": 0.0},
    }

    def __init__(
        self,
        event: RFXtrx.SensorEvent,
        timestamp: datetime.datetime = datetime.datetime.now(datetime.timezone.utc),
    ) -> None:
        self._sensor_event: RFXtrx.SensorEvent = event
        self.timestamp: datetime.datetime = timestamp

    def __str__(self) -> str:
        s = (
            f"<BresserHygrometerMeasurement: ID={self._sensor_event.device.id_string} "
            f"temp={self._sensor_event.values['Temperature']}degC>"
        )
        return s

    def to_influxdb_dict(self) -> dict:
        sensor_data: dict = self._sensor_event.values
        sensor_device: RFXtrx.RFXtrxDevice = self._sensor_event.device

        addr = sensor_device.id_string.split(":")[1]
        raw_temperature = sensor_data["Temperature"]
        raw_humidity = sensor_data["Humidity"]
        (
            calibrated_temperature,
            calibrated_humidity,
        ) = BresserHygrometerMeasurement.apply_calibration(
            addr, raw_temperature, raw_humidity
        )
        result = {
            "measurement": "Temperature",
            "tags": {
                "device_make": "Bresser",
                "device_type": sensor_device.type_string,
                "device_id": sensor_device.id_string,
                "location": SENSOR_LOCATIONS[addr],
            },
            "fields": {
                "temperature": calibrated_temperature,  # degree celcius (float)
                "humidity": calibrated_humidity,  # percent (float)
                "humidity_uncalibrated": sensor_data["Humidity"],  # percent (int)
                "humidity_status": sensor_data["Humidity status"],
                "humidity_status_numeric": sensor_data["Humidity status numeric"],
                "temperature_uncalibrated": sensor_data[
                    "Temperature"
                ],  # degree celcius (float)
                "signal_strenght": sensor_data["Rssi numeric"],  # 0-9(?) (int)
                "sensor_battery": sensor_data["Battery numeric"],  # 0-x(?) (int)
            },
            "time": self.timestamp,
        }
        return result

    @staticmethod
    def apply_calibration(address, temperature, humidity) -> tuple:
        calibrated_temperature = (
            temperature
            + BresserHygrometerMeasurement.CALIBRATION_TABLE[address][
                "temperature_offset"
            ]
        )
        calibrated_humidity = (
            humidity
            + BresserHygrometerMeasurement.CALIBRATION_TABLE[address]["humidity_offset"]
        )
        return (calibrated_temperature, calibrated_humidity)


class Measure(Publisher):
    def __init__(self, serial_tty: str = "/dev/ttyUSB0") -> None:
        self._rfxcomm_serial_tty: str = os.getenv(
            "RFXCOMM_SERIAL_TTY", default=serial_tty
        )
        self._measurements: queue.Queue = queue.Queue()
        self._collecting = False
        self._rfxcomm: RFXtrx.Connect = None

    def start_collecting(self) -> None:
        try:
            self._rfxcomm = RFXtrx.Core(
                self._rfxcomm_serial_tty,
                self._callback_rfxtrx433,
                modes=["oregon", "rubicson"],
            )
        except Exception as e:
            logging.exception(
                f"Failed to setup rfxcomm monitoring on TTY: {self._rfxcomm_serial_tty}"
            )
            raise e
        self._collecting = True

    def stop_collecting(self) -> None:
        if self._rfxcomm is not None:
            self._rfxcomm.close_connection()
        self._collecting = False

    def get_reading(self, timeout: float = 5 * 60.0) -> dict:
        try:
            reading: dict = self._measurements.get(block=True, timeout=timeout)
        except queue.Empty:
            msg = f"Timeout {timeout}sec. No readings from Owl. Disconnected."
            logging.exception(msg)
            raise TimeoutError(msg)
        return reading

    def _callback_rfxtrx433(self, event: RFXtrx.SensorEvent) -> None:
        reading = self._sensor_event_to_dict(event)
        try:
            if reading is not None:
                self._measurements.put(reading, block=False)
        except queue.Full:
            logging.exception(
                "Owl measurement queue is full. Dropping data. Is consumer side stuck?"
            )

    def _sensor_event_to_dict(self, event: RFXtrx.SensorEvent) -> dict | None:
        acq_timestamp: datetime.datetime = datetime.datetime.now(datetime.timezone.utc)
        sensor_data: dict = event.values
        sensor_device: RFXtrx.RFXtrxDevice = event.device
        logging.debug(sensor_device)
        logging.debug(sensor_data)

        result = None
        if sensor_device.type_string.startswith("ELEC"):
            # Energy meter measurement captured
            result = {
                "measurement": "Electricity",
                "tags": {
                    "device_make": "OWL",
                    "device_type": sensor_device.type_string,
                    "device_id": sensor_device.id_string,
                },
                "fields": {
                    "power": sensor_data["Energy usage"],  # Watt (int)
                    "consumption_total": sensor_data[
                        "Total usage"
                    ],  # Watt-hours Wh (float)
                    "signal_strenght": sensor_data["Rssi numeric"],  # 0-9(?) (int)
                    "sensor_battery": sensor_data["Battery numeric"],  # 0-x(?) (int)
                },
                "time": datetime.datetime.now(datetime.timezone.utc),
            }
            # logging.debug(result)
        elif sensor_device.type_string.startswith("Rubicson"):
            # Temperature monitor device
            meas = BresserHygrometerMeasurement(event, acq_timestamp)
            # logging.debug(meas)
            result = meas.to_influxdb_dict()
        else:
            logging.warning(f"Unrecognised sensor device: {sensor_device.type_string}")
        logging.debug(result)
        return result

    def __str__(self) -> str:
        s = (
            f"< OwlMeter: collecting={self._collecting}"
            f"  rfxcomm_tty={self._rfxcomm_serial_tty}"
            f"  queue len={self._measurements.qsize()}>"
        )
        return s
