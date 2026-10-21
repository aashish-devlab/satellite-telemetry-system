class FaultDetector:
    def __init__(self):
        # No packet has been received yet.
        self.last_sequence = None

    def check_sequence(self, current_sequence):
        # The first packet establishes our baseline.
        if self.last_sequence is None:
            self.last_sequence = current_sequence
            return None

        # Calculate how many sequence numbers were skipped.
        gap = current_sequence - self.last_sequence - 1

        # Remember the current packet for the next comparison.
        self.last_sequence = current_sequence

        if gap > 0:
            return f"Missing {gap} packet(s)"

        return None
