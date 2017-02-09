# Run from root directory
# python2.7 -m tests.test_screenshot

import unittest
import imghdr
from core import screenshot as sht

class TestScreenshot(unittest.TestCase):
    def test_take_screenshot(self):
        self.__subclasshook__
        filename = 'tests/test.jpg'
        imgFile = sht.take_screenshot(filename)
        self.assertEqual(imghdr.what(filename), 'jpeg') 

if __name__ == '__main__':
    unittest.main()

