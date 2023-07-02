# SPDX-License-Identifier: MIT

from unittest import TestCase
from yeet_api.device import Device


class DeviceTest(TestCase):
    def setUp(self):
        self.device = Device("testbrand_1", "testmodel_1_1")

    def test_attr(self):
        self.assertEqual(self.device.brand, "testbrand_1")
        self.assertEqual(self.device.model, "testmodel_1_1")

    def test_device_metadata(self):
        self.assertEqual(self.device.fullname, "Test Device")
        self.assertEqual(self.device.codename, "TESTDEV123")

    def test_verify_resources(self):
        self.assertEqual(
            self.device.get_available_resources(),
            ("recovery", "kernel", "extraresource1", "extraresource2"),
        )

    def test_resources(self):
        self.assertEqual(
            self.device.get_resource("recovery"),
            {
                "PBRP": "https://google.com",
                "TWRP": "https://google.com",
                "OFOX": "https://google.com",
            },
        )
        self.assertEqual(
            self.device.get_resource("kernel"),
            {
                "BBKERNEL": "https://google.com",
                "PERFKERNEL": "https://google.com",
                "BALANCEDKERNEL": "https://google.com",
            },
        )

    def test_extra_resources(self):
        self.assertEqual(
            self.device.get_resource("extraresource1"),
            {"UNLOCKSCRIPT": "https://google.com"},
        )
        self.assertEqual(
            self.device.get_resource("extraresource2"),
            {"BOOTLOADERUNLOCKGUIDE": "https://google.com"},
        )
