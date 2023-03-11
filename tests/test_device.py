# SPDX-License-Identifier: MIT

from unittest import TestCase
from yeet_api.devices import Device, _DeviceJSON


class DeviceTest(TestCase):
    def setUp(self):
        self.device = Device("testbrand", "testmodel")

    def test_device(self):
        self.assertEqual(self.device.fullname, "Test Device")
        self.assertEqual(self.device.codename, "TESTDEV123")

    def test_resources(self):
        self.assertEqual(
            self.device.get_available_resources(),
            ("recovery", "kernel", "extraresource1", "extraresource2"),
        )
        self.assertEqual(
            self.device.get_resource("recovery"),
            {
                "PBRP": "https://google.com",
                "TWRP": "https://google.com",
                "OFOX": "https://google.com",
            },
        )
