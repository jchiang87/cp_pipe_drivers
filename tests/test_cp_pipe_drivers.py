"""
Example unit tests for cp_pipe_drivers package
"""
import unittest
import desc.cp_pipe_drivers

class cp_pipe_driversTestCase(unittest.TestCase):
    def setUp(self):
        self.message = 'Hello, world'

    def tearDown(self):
        pass

    def test_run(self):
        foo = desc.cp_pipe_drivers.cp_pipe_drivers(self.message)
        self.assertEqual(foo.run(), self.message)

    def test_failure(self):
        self.assertRaises(TypeError, desc.cp_pipe_drivers.cp_pipe_drivers)
        foo = desc.cp_pipe_drivers.cp_pipe_drivers(self.message)
        self.assertRaises(RuntimeError, foo.run, True)

if __name__ == '__main__':
    unittest.main()
