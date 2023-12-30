import logging
import os
import queue
import re
from datetime import datetime, timedelta, timezone

import RFXtrx

from .sensor import Publisher

# If you get a new sensor, set its address to 1, 2, or 3 and add it
# to this dictionary with the location it is expected to be placed in.
SENSOR_LOCATIONS = {
    "01": ["bedroom", "dining"],
    "02": ["conservatory"],
    "03": ["garden"],
}


class ThermometerLocations:
    """
    A class that manages the locations of thermometers based on their sensor IDs.

    This class is implemented as a singleton, meaning that only one instance of it can
    exist.

    Attributes:
        _instance (ThermometerLocations): The singleton instance of the class.
        last_readings (dict[str, tuple[str, datetime]]): A dictionary that stores the
            last readings for each location. The keys are the location names, and the
            values are tuples containing the sensor ID and the timestamp of the last
            reading.
        _sensor_id_regexp (re.Pattern): A compiled regular expression pattern used to
            validate sensor IDs.

    Methods:
        get_location(sensor_id: str) -> str:
            Retrieves the location associated with the given sensor ID.
            If the sensor ID is new, it assigns a location to it based on predefined
            rules.
        is_sensor_id_new(addr: str) -> bool:
            Checks if the given sensor ID is new (i.e., not found in the last readings).

    Usage:
        # Create an instance of ThermometerLocations
        locations = ThermometerLocations()

        # Get the location for a sensor ID
        location = locations.get_location("89:01")

        # Check if a sensor ID is new
        is_new = locations.is_sensor_id_new("89:01")
    """

    _instance = None  # THIS IS A SINGLETON CLASS

    def __new__(cls):
        if cls._instance is None:
            logging.debug(
                "Creating and initialising the original instance "
                "of ThermometerLocations"
            )
            cls._instance = super(ThermometerLocations, cls).__new__(cls)
            # One-time initialisation here:
            cls._instance.last_readings: dict[str, tuple[str, datetime]] = {
                "bedroom": ("89:01", datetime.now()),
                "conservatory": ("18:02", datetime.now()),
                "garden": ("bb:03", datetime.now()),
            }
            cls._instance._sensor_id_regexp = re.compile(r"^[0-9a-f]{2}:0[0-3]{1}$")
        return cls._instance

    def get_location(self, sensor_id: str) -> str:
        """
        Retrieves the location associated with the given sensor ID.
        If the sensor ID is new, it assigns a location to it based on predefined rules.

        Args:
            sensor_id (str): The sensor ID to retrieve the location for.

        Returns:
            str: The location associated with the sensor ID.

        Raises:
            RuntimeError: If the sensor ID is invalid.

        Example:
            # Create an instance of ThermometerLocations
            locations = ThermometerLocations()

            # Get the location for a sensor ID
            location = locations.get_location("89:01")
        """
        # First check for a valid address
        if not re.match(self._sensor_id_regexp, sensor_id):
            raise RuntimeError(f"Invalid sensor ID: '{sensor_id}'")

        # Check if address is already known
        if not self.is_sensor_id_new(sensor_id):
            # Find the location for the address, update the timestamp and return
            for location, (location_addr, _) in self.last_readings.items():
                if sensor_id == location_addr:
                    self.last_readings.update({location: (sensor_id, datetime.now())})
                    return location

        # Address is new. Find a location for it
        locations = SENSOR_LOCATIONS[sensor_id.split(":")[-1]]
        logging.debug(
            "New sensor ID detected: '%s' Sensor expected in locations: %s",
            sensor_id,
            locations,
        )
        for location in locations:
            if location in self.last_readings:
                # Check if the last reading for this location is older than 5 minutes
                # If so, update the address and timestamp
                last_timestamp = self.last_readings[location][1]
                if datetime.now() - last_timestamp > timedelta(minutes=5):
                    logging.info(
                        "Temperature sensor in location: %s has reading older"
                        " than 5 minutes. Updating with new sensor ID: '%s'",
                        location,
                        sensor_id,
                    )
                    self.last_readings.update({location: (sensor_id, datetime.now())})
                    return location
            else:
                # Location is new. Register it and return
                logging.info(
                    "Registering new location: '%s' for sensor ID: '%s'",
                    location,
                    sensor_id,
                )
                self.last_readings.update({location: (sensor_id, datetime.now())})
                return location

        # No location found. Register the address as unknown and return
        unknown_location = f"UNKNOWN-{sensor_id}"
        logging.warning(
            "Can't determine location for new sensor ID." "Registering location: '%s'",
            unknown_location,
        )
        self.last_readings.update({unknown_location: (sensor_id, datetime.now())})
        return unknown_location

    def is_sensor_id_new(self, addr: str) -> bool:
        """
        Checks if the given sensor ID is new (i.e., not found in the last readings).

        Args:
            addr (str): The sensor ID to check.

        Returns:
            bool: True if the sensor ID is new, False otherwise.

        Example:
            # Create an instance of ThermometerLocations
            locations = ThermometerLocations()

            # Check if a sensor ID is new
            is_new = locations.is_sensor_id_new("89:01")
        """
        return addr not in list(zip(*self.last_readings.values()))[0]


class BresserHygrometerMeasurement:
    CALIBRATION_TABLE = {
        "bedroom": {"temperature_offset": -0.3, "humidity_offset": 0.0},
        "conservatory": {"temperature_offset": 1.0, "humidity_offset": 2.0},
        "garden": {"temperature_offset": 1.0, "humidity_offset": 0.0},
    }

    def __init__(
        self,
        event: RFXtrx.SensorEvent,
        timestamp: datetime = datetime.now(timezone.utc),
    ) -> None:
        self._sensor_event: RFXtrx.SensorEvent = event
        self.timestamp: datetime = timestamp
        self.thermometer_locations = ThermometerLocations()

    def __str__(self) -> str:
        s = (
            f"<BresserHygrometerMeasurement: ID={self._sensor_event.device.id_string} "
            f"temp={self._sensor_event.values['Temperature']}degC>"
        )
        return s

    def to_influxdb_dict(self) -> dict:
        sensor_data: dict = self._sensor_event.values
        sensor_device: RFXtrx.RFXtrxDevice = self._sensor_event.device

        location = self.thermometer_locations.get_location(sensor_device.id_string)
        raw_temperature = sensor_data["Temperature"]
        raw_humidity = sensor_data["Humidity"]
        (
            calibrated_temperature,
            calibrated_humidity,
        ) = BresserHygrometerMeasurement.apply_calibration(
            location, raw_temperature, raw_humidity
        )
        result = {
            "measurement": "Temperature",
            "tags": {
                "device_make": "Bresser",
                "device_type": sensor_device.type_string,
                "device_id": sensor_device.id_string,
                "location": location,
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
    def apply_calibration(
        location: str, temperature: float, humidity: float
    ) -> tuple[float, float]:
        """
        Apply calibration offsets to the temperature and humidity measurements based on
        the given location. If the location is not found in the calibration table, the
        measurements are returned unmodified.

        Args:
            location (str): The location for which the calibration offsets should be
                            applied.
            temperature (float): The temperature measurement.
            humidity (float): The humidity measurement.

        Returns:
            tuple: A tuple containing the calibrated temperature and humidity
            measurements.
        """
        if location not in BresserHygrometerMeasurement.CALIBRATION_TABLE:
            logging.debug(
                f"Location {location} not found in calibration table. "
                f"Using uncalibrated values."
            )
            return (temperature, humidity)

        calibrated_temperature = (
            temperature
            + BresserHygrometerMeasurement.CALIBRATION_TABLE[location][
                "temperature_offset"
            ]
        )
        calibrated_humidity = (
            humidity
            + BresserHygrometerMeasurement.CALIBRATION_TABLE[location][
                "humidity_offset"
            ]
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
            msg = f"Timeout {timeout}sec. No readings from any sensors. Disconnected?"
            logging.warning(msg)
            raise TimeoutError(msg)
        return reading

    def _callback_rfxtrx433(self, event: RFXtrx.SensorEvent) -> None:
        """Callback method from RXFtrx with event update.

        This is called from the RFXtrx polling thread when an event has
        been received and decoded by the sensor.
        Parse the event object into a dictionary that influxdb can use and
        put the result dictionary on to a queue to be consumed by the recording
        thread.

        Importantly this function must handle all exceptions to avoid crashing the
        RFXtrx polling thread
        """
        try:
            reading = self._sensor_event_to_dict(event)
        except Exception:
            logging.exception(
                "Caught and handling exception in callback "
                f"when parsing sensor event: {event}"
            )
            reading = None
        if reading is None:
            return
        try:
            self._measurements.put(reading, block=False)
        except queue.Full:
            logging.exception(
                "Owl measurement queue is full. Dropping data. Is consumer side stuck?"
            )

    def _sensor_event_to_dict(self, event: RFXtrx.SensorEvent) -> dict | None:
        acq_timestamp: datetime = datetime.now(timezone.utc)
        if not isinstance(event, RFXtrx.SensorEvent):
            logging.warning(
                f"Received unexpected event type from RFXtrx: "
                f"{type(event)} Event IGNORED: {event}"
            )
            return
        sensor_data: dict = event.values
        sensor_device: RFXtrx.RFXtrxDevice = event.device
        logging.info(f"Received Event. Device: {sensor_device} Data: {sensor_data}")

        result = None
        if sensor_device.type_string.lower().startswith("elec"):
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
                    # "consumption_total": # See below. Watt-hours Wh (float)
                    "signal_strenght": sensor_data["Rssi numeric"],  # 0-9(?) (int)
                    "sensor_battery": sensor_data["Battery numeric"],  # 0-x(?) (int)
                },
                "time": datetime.now(timezone.utc),
            }
            if sensor_data["Count"] == 0:
                result["fields"].update(
                    {
                        "consumption_total": sensor_data[  # Watt-hours Wh (float)
                            "Total usage"
                        ]
                    }
                )
            else:
                logging.warning(
                    "Disregarding Total usage reading as Count!=0 from "
                    f"Device: {sensor_device} Reading: {sensor_data}"
                )
            logging.debug("Parsed Event: %s", result)
            # SANITY DATA CHECK: sometimes the OWL report power at or above 1MW which
            # is unlikely to be real but really mess with the stats in the DB.
            # Discard the data point if higher than 20KW
            if result["fields"]["power"] > 20000:
                logging.warning(
                    f"Discarding unrealistic high power reading from OWL. "
                    f"Reading: {result}"
                )
                result = None
        elif sensor_device.type_string.lower().startswith("rubicson"):
            # Temperature monitor device
            meas = BresserHygrometerMeasurement(event, acq_timestamp)
            # logging.debug(meas)
            result = meas.to_influxdb_dict()
        else:
            logging.warning(
                f"Unrecognised sensor device: {sensor_device.type_string}"
                f" Event: {event}"
            )
        logging.debug(result)
        return result

    def __str__(self) -> str:
        s = (
            f"< OwlMeter: collecting={self._collecting}"
            f"  rfxcomm_tty={self._rfxcomm_serial_tty}"
            f"  queue len={self._measurements.qsize()}>"
        )
        return s
