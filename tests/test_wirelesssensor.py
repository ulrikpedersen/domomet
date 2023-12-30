from datetime import datetime, timedelta

from domomet.wirelesssensor import ThermometerLocations


def test_get_location_existing():
    sensor = ThermometerLocations()
    location = sensor.get_location("89:01")
    assert location == "bedroom"


def test_get_location_new():
    sensor = ThermometerLocations()
    is_sensor_id_new = sensor.is_sensor_id_new("12:03")
    assert is_sensor_id_new
    location = sensor.get_location("12:03")
    assert location == "UNKNOWN-12:03"


def test_is_sensor_id_new_existing():
    sensor = ThermometerLocations()
    is_new = sensor.is_sensor_id_new("89:01")
    assert not is_new
    location = sensor.get_location("89:01")
    assert location == "bedroom"
    location = sensor.get_location("bb:01")
    assert location == "dining"


def test_is_sensor_id_new_new():
    sensor = ThermometerLocations()
    is_new = sensor.is_sensor_id_new("23:01")
    assert is_new


def test_sensor_new_sensor_id_in_bedroom():
    sensor = ThermometerLocations()
    ten_minutes_ago = datetime.now() - timedelta(minutes=10)
    sensor.last_readings.update({'bedroom': ('89:01', ten_minutes_ago)})
    is_new = sensor.is_sensor_id_new("44:01")
    assert is_new

    location = sensor.get_location("44:01")
    assert location == "bedroom"
