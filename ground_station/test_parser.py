
import unittest

from parser import parse_packet


def make_packet(payload: str) -> str:
    checksum = 0
    for character in payload:
        checksum ^= ord(character)
    return f"{payload},{checksum:02X}"


class TestTelemetryParser(unittest.TestCase):

    def setUp(self):
        self.payload = (
            "AKTD,69,27.69,990.16,"
            "-672,404,15960,241,40,-16,3.92"
        )
        self.packet = make_packet(self.payload)

    def test_valid_packet(self):
        data = parse_packet(self.packet)

        self.assertEqual(data.sequence, 69)
        self.assertAlmostEqual(data.temperature_c, 27.69)
        self.assertAlmostEqual(data.pressure_hpa, 990.16)
        self.assertEqual(data.accel_z, 15960)
        self.assertAlmostEqual(data.battery_v, 3.92)

    def test_wrong_field_count(self):
        with self.assertRaises(ValueError):
            parse_packet("AKTD,69,27.69")

    def test_invalid_prefix(self):
        packet = make_packet(self.payload.replace("AKTD", "XXXX", 1))
        with self.assertRaises(ValueError):
            parse_packet(packet)

    def test_corrupted_packet(self):
        with self.assertRaises(ValueError):
            parse_packet(self.packet[:-1] + "0")

    def test_invalid_numeric_field(self):
        payload = self.payload.replace("27.69", "invalid")
        with self.assertRaises(ValueError):
            parse_packet(make_packet(payload))


if __name__ == "__main__":
    unittest.main()
