import unittest
from faults import FaultDetector


class TestFaultDetector(unittest.TestCase):
    def setUp(self):
        self.detector = FaultDetector()

    def test_first_packet_sets_baseline(self):
        result = self.detector.check_sequence(10)
        self.assertEqual(result, 0)
        self.assertEqual(self.detector.last_sequence, 10)

    def test_consecutive_packets(self):
        self.detector.check_sequence(10)
        result = self.detector.check_sequence(11)
        self.assertEqual(result, 0)

    def test_missing_one_packet(self):
        self.detector.check_sequence(10)
        result = self.detector.check_sequence(12)
        self.assertEqual(result, 1)

    def test_missing_multiple_packets(self):
        self.detector.check_sequence(10)
        result = self.detector.check_sequence(14)
        self.assertEqual(result, 3)

    def test_detector_continues_after_gap(self):
        self.detector.check_sequence(10)
        self.detector.check_sequence(12)
        result = self.detector.check_sequence(13)
        self.assertEqual(result, 0)

    def test_duplicate_sequence(self):
        detector = FaultDetector()

        assert detector.check_sequence(10) == 0
        assert detector.check_sequence(10) == 0
        assert detector.duplicate_packets == 1
        assert detector.last_sequence == 10



    def test_out_of_order_sequence(self):
        detector = FaultDetector()

        assert detector.check_sequence(10) == 0
        assert detector.check_sequence(8) == 0
        assert detector.out_of_order_packets == 1
        assert detector.last_sequence == 10



    def test_missing_after_out_of_order_packet(self):
        detector = FaultDetector()

        assert detector.check_sequence(10) == 0
        assert detector.check_sequence(8) == 0
        assert detector.check_sequence(13) == 2



if __name__ == "__main__":
    unittest.main()