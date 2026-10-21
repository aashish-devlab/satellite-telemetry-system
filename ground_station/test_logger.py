
import csv
import tempfile
import unittest
from pathlib import Path

from logger import TelemetryLogger
from parser import parse_packet


class TestTelemetryLogger(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.log_path = Path(self.temp_dir.name) / "telemetry.csv"

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_writes_header_and_packet(self):
        payload = (
            "AKTD,10,28.35,991.07,-2200,484,15744,"
            "190,20,-30,3.92"
        )

        # Calculate the XOR checksum over the payload.
        checksum = 0
        for char in payload:
            checksum ^= ord(char)

        # Parse only after creating a valid checksum.
        packet = parse_packet(f"{payload},{checksum:02X}")

        with TelemetryLogger(self.log_path) as logger:
            logger.log_packet(packet)

        with self.log_path.open(
            newline="", encoding="utf-8"
        ) as file:
            rows = list(csv.reader(file))

        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0][0], "timestamp_utc")
        self.assertEqual(rows[1][1], "10")
        self.assertEqual(rows[1][-1], "3.92")
        self.assertTrue(rows[1][0].endswith("+00:00"))


    def test_appends_without_duplicate_header(self):
        payload = (
            "AKTD,11,28.35,991.07,-2200,484,15744,"
            "190,20,-30,3.92"
        )
        checksum = 0
        for char in payload:
            checksum ^= ord(char)

        packet = parse_packet(f"{payload},{checksum:02X}")

        with TelemetryLogger(self.log_path) as logger:
            logger.log_packet(packet)

        with TelemetryLogger(self.log_path) as logger:
            logger.log_packet(packet)

        with self.log_path.open(newline="", encoding="utf-8") as file:
            rows = list(csv.reader(file))

        self.assertEqual(len(rows), 3)
        self.assertEqual(sum(row[0] == "timestamp_utc" for row in rows), 1)


if __name__ == "__main__":
    unittest.main()
