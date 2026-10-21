
import io
import unittest
from contextlib import redirect_stdout

from dashboard import TelemetryDashboard
from parser import parse_packet


class TestTelemetryDashboard(unittest.TestCase):
    def setUp(self):
        self.dashboard = TelemetryDashboard()

    def make_packet(self, sequence):
        payload = (
            f"AKTD,{sequence},28.35,991.07,-2200,484,15744,"
            "190,20,-30,3.92"
        )
        checksum = 0

        for char in payload:
            checksum ^= ord(char)

        return parse_packet(f"{payload},{checksum:02X}")

    def test_initial_dashboard(self):
        output = io.StringIO()

        with redirect_stdout(output):
            self.dashboard.render()

        self.assertIn("Waiting for telemetry", output.getvalue())

    def test_update_and_render_packet(self):
        self.dashboard.update(self.make_packet(7))

        output = io.StringIO()
        with redirect_stdout(output):
            self.dashboard.render()

        rendered = output.getvalue()

        self.assertIn("Valid packets received : 1", rendered)
        self.assertIn("Latest sequence number : 7", rendered)
        self.assertIn("28.35", rendered)
        self.assertIn("3.92 V", rendered)

    def test_packet_count_increments(self):
        self.dashboard.update(self.make_packet(7))
        self.dashboard.update(self.make_packet(8))

        self.assertEqual(self.dashboard.packet_count, 2)
        self.assertEqual(self.dashboard.last_sequence, 8)


if __name__ == "__main__":
    unittest.main()
