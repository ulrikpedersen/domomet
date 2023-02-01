from domomet import electricitymeter


def test_creating_owlmeter():
    owl = electricitymeter.OwlMeter(serial_tty="/blah/blah/blah")
    assert "OwlMeter" in str(owl)
    assert owl is not None
