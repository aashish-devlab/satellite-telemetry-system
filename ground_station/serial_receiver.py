
import time
from matplotlib.pylab import plot
import serial

from ground_station.parser import parse_packet
from ground_station.faults import FaultDetector, ReceptionStats
from ground_station.logger import TelemetryLogger
from ground_station.dashboard import TelemetryDashboard
from ground_station.live_plot import LiveTelemetryPlot

fault_detector = FaultDetector()


# Fedora: stable USB serial device path.
PORT = (
    "/dev/serial/by-id/"
    "usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0001-if00-port0"
)

# Windows: comment out the Fedora path and use this instead.
# PORT = "COM3"

BAUD_RATE = 115200
PACKET_TIMEOUT = 8
RETRY_DELAY = 1


def receive_packets():
    # Start the timer when this connection attempt begins.
    last_packet_time = time.monotonic()
    fault_detector = FaultDetector()
    stats = ReceptionStats()
    dashboard = TelemetryDashboard(stats, fault_detector)
    logger = TelemetryLogger("logs/telemetry_log.csv")
    plot = LiveTelemetryPlot(max_points=100)
    plot_start_time = time.monotonic()

    with serial.Serial(
        PORT,
        BAUD_RATE,
        timeout=1,
        write_timeout=1,
        rtscts=False, # Disables RTS/CTS hardware flow control
        dsrdtr=False, # Disables DSR/DTR flow control.
    ) as connection:

        connection.dtr = False
        connection.rts = False

        print(f"Connected to {PORT}. Waiting for telemetry...")

        while True:
            raw_line = connection.readline()

            if raw_line:
                line = raw_line.decode(
                    "ascii", errors="ignore"
                ).strip()

                try:
                    packet = parse_packet(line)

                except ValueError as error:
                    stats.record_invalid_packet()

                    if stats.invalid_packets <= 10:
                        print(f"Invalid packet #{stats.invalid_packets}: {error}")

                else:
                    # Only a successfully parsed packet resets the timer.
                    last_packet_time = time.monotonic()
                    stats.record_valid_packet()
                    logger.log_packet(packet)

                    missing = fault_detector.check_sequence(packet.sequence)

                    if missing > 0:
                        stats.record_missing_packets(missing)
                        print(f"SEQUENCE FAULT: Missing {missing} packet(s)")

                    dashboard.update(packet)
                    dashboard.render()
                    elapsed_seconds = time.monotonic() - plot_start_time
                    plot.update(packet, elapsed_seconds)
                    # print(
                    #     f"Seq: {packet.sequence} | "
                    #     f"Temp: {packet.temperature_c:.2f} C | "
                    #     f"Pressure: {packet.pressure_hpa:.2f} hPa | "
                    #     f"Accel: ({packet.accel_x}, "
                    #     f"{packet.accel_y}, {packet.accel_z}) | "
                    #     f"Gyro: ({packet.gyro_x}, "
                    #     f"{packet.gyro_y}, {packet.gyro_z}) | "
                    #     f"Battery: {packet.battery_v:.2f} V",
                    #     flush=True,
                    # )

            # Check the timeout even if incoming data is invalid.
            elapsed = time.monotonic() - last_packet_time

            if elapsed > PACKET_TIMEOUT:
                print(
                    f"No valid telemetry for {PACKET_TIMEOUT} seconds. "
                    "Reopening serial connection..."
                )
                return


def main():
    while True:
        try:
            print(f"Opening {PORT}...")
            receive_packets()

        except KeyboardInterrupt:
            print("\nReceiver stopped.")
            break

        except (serial.SerialException, OSError) as error:
            print(f"Serial connection error: {error}")

        time.sleep(RETRY_DELAY)


if __name__ == "__main__":
    main()
