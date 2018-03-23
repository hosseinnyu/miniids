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

    def test_sensor_listen_notnull_interface(self):
	s  = sensor.Sensor()
	s.instance.interface = None
        self.assertRaises(ValueError, s.start)

    def test_sensor_invalid_interface(self):
	s  = sensor.Sensor()
	s.instance.interface = "nothing"
	self.assertRaises(ValueError, s.start)	

if __name__ == '__main__':
    unittest.main()
