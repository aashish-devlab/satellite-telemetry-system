
class TelemetryDashboard:
    def __init__(self, stats=None, fault_detector=None):
        self.packet_count = 0
        self.last_sequence = None
        self.latest_packet = None
        self.stats = stats
        self.fault_detector = fault_detector

    def update(self, packet):
        self.latest_packet = packet
        self.packet_count += 1
        self.last_sequence = packet.sequence

    def render(self):
        if self.latest_packet is None:
            print("Waiting for telemetry...")
            return

        packet = self.latest_packet

        # Clear terminal before rendering the dashboard
        print("\033[2J\033[H", end="")

        print("=" * 52)
        print("       SATELLITE TELEMETRY GROUND STATION")
        print("=" * 52)

        print("PACKET STATISTICS")
        print(f"Valid packets received : {self.packet_count}")
        print(f"Latest sequence number : {self.last_sequence}")

        if self.stats is not None:
            #print(f"Invalid packets received  : {self.stats.invalid_packets}")
            print(f"Missing packets detected  : {self.stats.missing_packets}")
            print(f"Runtime                   : {self.stats.runtime_seconds:.1f} s")
            print(
                f"Average reception rate    : "
                f"{self.stats.reception_rate:.2f} packets/s"
            )

        if self.fault_detector is not None:
            print(
                f"Duplicate packets detected: "
                f"{self.fault_detector.duplicate_packets}"
            )
            print(
                f"Out-of-order packets      : "
                f"{self.fault_detector.out_of_order_packets}"
            )

        print("-" * 52)
        print("ENVIRONMENT")
        print(f"Temperature               : {packet.temperature_c:.2f} °C")
        print(f"Pressure                  : {packet.pressure_hpa:.2f} hPa")

        print("-" * 52)
        print("IMU (RAW SENSOR COUNTS)")
        print(
            f"Accelerometer             : "
            f"{packet.accel_x}, {packet.accel_y}, {packet.accel_z}"
        )
        print(
            f"Gyroscope                 : "
            f"{packet.gyro_x}, {packet.gyro_y}, {packet.gyro_z}"
        )

        print("-" * 52)
        print("POWER")
        print(f"Battery voltage           : {packet.battery_v:.2f} V")

        print("=" * 52)
        print("Press Ctrl+C to stop.")
