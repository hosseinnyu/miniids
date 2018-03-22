import unittest
import sys
sys.path.append('..')
import sensor

def fun(x):
    return x + 1

class TestSensor(unittest.TestCase):
    def test_seonsor_plugin_notnull_handler(self):
        s  = sensor.Sensor()
	self.assertRaises(ValueError, s.plugin, "HTTP", None)

    def test_sensor_plugin_object_has_notify(self):
	s  = sensor.Sensor()
	self.assertRaises(ValueError, s.plugin, "HTTP", self)
	
    def test_sensor_plugin_traffic_type_not_supported(self):
	s  = sensor.Sensor()
        self.assertRaises(ValueError, s.plugin, "unknown123", self)


if __name__ == '__main__':
    unittest.main()
