"""
===========================================================
Satellite Telemetry System
Ground Station - Fault Detection
===========================================================

This module analyzes received telemetry packets and
detects abnormal operating conditions.

Author : Aashish Kumar
===========================================================
"""


class FaultDetector:

    def __init__(self):

        self.last_packet_counter = None

    # --------------------------------------------------
    # Check Faults
    # --------------------------------------------------
    def check(self, telemetry):

        faults = []

        # -------------------------------
        # Battery
        # -------------------------------
        if telemetry["battery_percentage"] < 20:
            faults.append("LOW BATTERY")

        # -------------------------------
        # Temperature
        # -------------------------------
        if telemetry["temperature"] > 70:
            faults.append("HIGH TEMPERATURE")

        # -------------------------------
        # Roll
        # -------------------------------
        if abs(telemetry["roll"]) > 45:
            faults.append("HIGH ROLL ANGLE")

        # -------------------------------
        # Pitch
        # -------------------------------
        if abs(telemetry["pitch"]) > 45:
            faults.append("HIGH PITCH ANGLE")

        # -------------------------------
        # Packet Loss Detection
        # -------------------------------
        if self.last_packet_counter is not None:

            expected = self.last_packet_counter + 1

            if telemetry["packet_counter"] != expected:

                faults.append(
                    f"PACKET LOSS (Expected {expected}, Received {telemetry['packet_counter']})"
                )

        self.last_packet_counter = telemetry["packet_counter"]

        # -------------------------------
        # Status Flags
        # -------------------------------
        status = telemetry["status"]

        if status & 0x01:
            faults.append("STATUS FLAG: LOW BATTERY")

        if status & 0x02:
            faults.append("STATUS FLAG: HIGH TEMPERATURE")

        if status & 0x04:
            faults.append("STATUS FLAG: BMP280 ERROR")

        if status & 0x08:
            faults.append("STATUS FLAG: MPU6050 ERROR")

        if status & 0x10:
            faults.append("STATUS FLAG: SENSOR TIMEOUT")

        return faults