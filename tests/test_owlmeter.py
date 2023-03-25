from domomet import sensor


def test_creating_owlmeter():
    owl = sensor.Measure(serial_tty="/blah/blah/blah")
    assert "OwlMeter" in str(owl)
    assert owl is not None
