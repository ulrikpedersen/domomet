import datetime
import logging
import os
import queue

import RFXtrx

from .sensor import Publisher


class OwlMeter(Publisher):
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
                self._rfxcomm_serial_tty, self._callback_rfxtrx433, modes=["oregon"]
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
            self._measurements.put(reading, block=False)
        except queue.Full:
            logging.exception(
                "Owl measurement queue is full. Dropping data. Is consumer side stuck?"
            )

    def _sensor_event_to_dict(self, event: RFXtrx.SensorEvent) -> dict:
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
                "consumption_total": sensor_data[
                    "Total usage"
                ],  # Watt-hours Wh (float)
                "signal_strenght": sensor_data["Rssi numeric"],  # 0-9(?) (int)
                "sensor_battery": sensor_data["Battery numeric"],  # 0-x(?) (int)
            },
            "time": datetime.datetime.now(datetime.timezone.utc),
        }
        return result

    def __str__(self) -> str:
        s = (
            f"< OwlMeter: collecting={self._collecting}"
            f"  rfxcomm_tty={self._rfxcomm_serial_tty}"
            f"  queue len={self._measurements.qsize()}>"
        )
        return s
