
import unittest

from faults import FaultDetector


class TestFaultDetector(unittest.TestCase):

    def setUp(self):
        self.detector = FaultDetector()

    def test_first_packet_sets_baseline(self):
        result = self.detector.check_sequence(10)

        self.assertIsNone(result)
        self.assertEqual(self.detector.last_sequence, 10)

    def test_consecutive_packets(self):
        self.detector.check_sequence(10)

        result = self.detector.check_sequence(11)

        self.assertIsNone(result)

    def test_missing_one_packet(self):
        self.detector.check_sequence(10)

        result = self.detector.check_sequence(12)

        self.assertEqual(result, "Missing 1 packet(s)")

    def test_missing_multiple_packets(self):
        self.detector.check_sequence(10)

        result = self.detector.check_sequence(14)

        self.assertEqual(result, "Missing 3 packet(s)")

    def test_detector_continues_after_gap(self):
        self.detector.check_sequence(10)
        self.detector.check_sequence(12)

        result = self.detector.check_sequence(13)

        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
