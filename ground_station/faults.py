
import time


class FaultDetector:
    def __init__(self):
        self.last_sequence = None
        self.duplicate_packets = 0
        self.out_of_order_packets = 0

    def check_sequence(self, current_sequence):
        if self.last_sequence is None:
            self.last_sequence = current_sequence
            return 0

        # Same sequence number: duplicate packet
        if current_sequence == self.last_sequence:
            self.duplicate_packets += 1
            return 0

        # Lower sequence number: out-of-order packet
        if current_sequence < self.last_sequence:
            self.out_of_order_packets += 1
            return 0

        # Higher sequence number: check for missing packets
        missing = current_sequence - self.last_sequence - 1
        self.last_sequence = current_sequence
        return missing



class ReceptionStats:
    def __init__(self):
        self.start_time = time.monotonic()
        self.valid_packets = 0
        self.invalid_packets = 0
        self.missing_packets = 0

    def record_valid_packet(self):
        self.valid_packets += 1

    def record_invalid_packet(self):
        self.invalid_packets += 1

    def record_missing_packets(self, count):
        if count > 0:
            self.missing_packets += count

    @property
    def runtime_seconds(self):
        return time.monotonic() - self.start_time

    @property
    def reception_rate(self):
        elapsed = self.runtime_seconds

        if elapsed <= 0:
            return 0.0

        return self.valid_packets / elapsed
