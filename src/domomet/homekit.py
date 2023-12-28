import logging
import signal
import threading
import time
from pprint import pformat

from pyhap.accessory import Accessory
from pyhap.accessory_driver import AccessoryDriver
from pyhap.const import CATEGORY_SENSOR

from . import sensor


class ElectricityMeterSensor(Accessory):
    """A HomeKit electiricty meter sensor"""

    category = CATEGORY_SENSOR

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        serv_current_power = self.add_preload_service("ElectricityMeter")
        self.characteristic_current_power = serv_current_power.configure_char(
            "CurrentPowerUsage"
        )

    def connect_sensor_pub(self, sensor: sensor.Publisher) -> None:
        self.sensor = sensor
        self._poll_thread = threading.Thread(target=self.update_readings)

    def update_readings(self) -> None:
        while True:
            try:
                measurement: dict = self.sensor.get_reading()
            except TimeoutError:
                continue
            logging.debug(f"Got measurement: \n{pformat(measurement)}")
            self.characteristic_current_power.set_value(measurement["fields"]["power"])
            time.sleep(2)


def run_server(sensor: sensor.Publisher):
    # Start the accessory on port 51826
    driver = AccessoryDriver(port=51826)

    hkit_owl = ElectricityMeterSensor(driver, "OWL eMeter")
    hkit_owl.connect_sensor_pub(sensor=sensor)

    # Change `get_accessory` to `get_bridge` if you want to run a Bridge.
    driver.add_accessory(accessory=hkit_owl)

    # We want SIGTERM (terminate) to be handled by the driver itself,
    # so that it can gracefully stop the accessory, server and advertising.
    signal.signal(signal.SIGTERM, driver.signal_handler)

    # Start it!
    driver.start()
