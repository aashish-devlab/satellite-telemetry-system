
import csv
from datetime import datetime, timezone
from pathlib import Path


class TelemetryLogger:
    def __init__(self, filename="telemetry_log.csv"):
        self.filename = Path(filename)

        # Create the parent directory if one was specified.
        self.filename.parent.mkdir(parents=True, exist_ok=True)

        # Write the header only when the file is new or empty.
        write_header = (
            not self.filename.exists()
            or self.filename.stat().st_size == 0
        )

        self.file = self.filename.open(
            "a", newline="", encoding="utf-8"
        )
        self.writer = csv.writer(self.file)

        if write_header:
            self.writer.writerow([
                "timestamp_utc",
                "sequence",
                "temperature_c",
                "pressure_hpa",
                "accel_x",
                "accel_y",
                "accel_z",
                "gyro_x",
                "gyro_y",
                "gyro_z",
                "battery_v",
            ])
            self.file.flush()

    def log_packet(self, packet):
        timestamp = datetime.now(timezone.utc).isoformat()

        self.writer.writerow([
            timestamp,
            packet.sequence,
            packet.temperature_c,
            packet.pressure_hpa,
            packet.accel_x,
            packet.accel_y,
            packet.accel_z,
            packet.gyro_x,
            packet.gyro_y,
            packet.gyro_z,
            packet.battery_v,
        ])

        # Make recently received data visible in the file immediately.
        self.file.flush()

    def close(self):
        if not self.file.closed:
            self.file.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
