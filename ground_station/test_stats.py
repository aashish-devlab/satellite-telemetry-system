import unittest

from faults import ReceptionStats


class TestReceptionStats(unittest.TestCase):
    def setUp(self):
        self.stats = ReceptionStats()

    def test_initial_counts_are_zero(self):
        self.assertEqual(self.stats.valid_packets, 0)
        self.assertEqual(self.stats.invalid_packets, 0)
        self.assertEqual(self.stats.missing_packets, 0)

    def test_record_valid_packets(self):
        self.stats.record_valid_packet()
        self.stats.record_valid_packet()

        self.assertEqual(self.stats.valid_packets, 2)

    def test_record_invalid_packets(self):
        self.stats.record_invalid_packet()

        self.assertEqual(self.stats.invalid_packets, 1)

    def test_record_missing_packets(self):
        self.stats.record_missing_packets(3)
        self.stats.record_missing_packets(2)

        self.assertEqual(self.stats.missing_packets, 5)

    def test_non_positive_missing_count_is_ignored(self):
        self.stats.record_missing_packets(0)
        self.stats.record_missing_packets(-1)

        self.assertEqual(self.stats.missing_packets, 0)

    def test_reception_rate_is_non_negative(self):
        self.stats.record_valid_packet()

        self.assertGreaterEqual(self.stats.reception_rate, 0.0)


if __name__ == "__main__":
    unittest.main()