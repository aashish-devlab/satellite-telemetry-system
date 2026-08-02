"""
===========================================================
Satellite Telemetry System
Ground Station - Data Logger
===========================================================

This module logs all valid telemetry packets into a CSV file.

Author : Aashish Kumar
===========================================================
"""

import csv
import os
from datetime import datetime


class DataLogger:

    def __init__(self, log_directory="logs"):

        self.log_directory = log_directory

        os.makedirs(self.log_directory, exist_ok=True)

        filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.csv")

        self.filepath = os.path.join(self.log_directory, filename)

        self.file = open(self.filepath, mode="w", newline="")

        self.writer = csv.writer(self.file)

        # CSV Header
        self.writer.writerow([
            "Packet Counter",
            "Timestamp (ms)",
            "Temperature (°C)",
            "Pressure (hPa)",
            "Altitude (m)",
            "Roll (deg)",
            "Pitch (deg)",
            "Battery Voltage (V)",
            "Battery Percentage (%)",
            "Status Flags"
        ])

        print(f"[LOGGER] Logging to {self.filepath}")

    # --------------------------------------------------
    # Write One Telemetry Packet
    # --------------------------------------------------
    def log(self, telemetry):

        self.writer.writerow([
            telemetry["packet_counter"],
            telemetry["timestamp"],
            telemetry["temperature"],
            telemetry["pressure"],
            telemetry["altitude"],
            telemetry["roll"],
            telemetry["pitch"],
            telemetry["battery_voltage"],
            telemetry["battery_percentage"],
            telemetry["status"]
        ])

        self.file.flush()

    # --------------------------------------------------
    # Close File
    # --------------------------------------------------
    def close(self):

        self.file.close()

        print("[LOGGER] File Saved")