
import unittest
from unittest.mock import Mock, patch

import matplotlib
matplotlib.use("Agg")

from ground_station.live_plot import LiveTelemetryPlot


def make_mock_packet(index=0):
    """Create a mock telemetry packet with all plotted fields."""
    packet = Mock()

    packet.temperature_c = 28.5 + index
    packet.pressure_hpa = 990.7 + index
    packet.battery_v = 3.92 + index * 0.01

    packet.accel_x = 100 + index
    packet.accel_y = -200 - index
    packet.accel_z = 16000 + index

    packet.gyro_x = 10 + index
    packet.gyro_y = -20 - index
    packet.gyro_z = 30 + index

    return packet


class TestLiveTelemetryPlot(unittest.TestCase):

    @patch("ground_station.live_plot.plt.pause")
    def test_update_adds_telemetry_data(self, mock_pause):
        plot = LiveTelemetryPlot(max_points=3)

        try:
            packet = make_mock_packet()
            plot.update(packet, elapsed_seconds=1.0)

            self.assertEqual(list(plot.times), [1.0])

            # Existing environmental and battery signals
            self.assertEqual(list(plot.temperatures), [28.5])
            self.assertEqual(list(plot.pressures), [990.7])
            self.assertEqual(list(plot.battery_voltages), [3.92])

            # Accelerometer signals
            self.assertEqual(list(plot.accel_x), [100])
            self.assertEqual(list(plot.accel_y), [-200])
            self.assertEqual(list(plot.accel_z), [16000])

            # Gyroscope signals
            self.assertEqual(list(plot.gyro_x), [10])
            self.assertEqual(list(plot.gyro_y), [-20])
            self.assertEqual(list(plot.gyro_z), [30])

            # All nine lines should receive the same time coordinate
            lines = [
                plot.temperature_line,
                plot.pressure_line,
                plot.battery_line,
                plot.accel_x_line,
                plot.accel_y_line,
                plot.accel_z_line,
                plot.gyro_x_line,
                plot.gyro_y_line,
                plot.gyro_z_line,
            ]

            for line in lines:
                self.assertEqual(list(line.get_xdata()), [1.0])

            mock_pause.assert_called_once()
        finally:
            plot.close()

    @patch("ground_station.live_plot.plt.pause")
    def test_data_is_limited_to_max_points(self, mock_pause):
        plot = LiveTelemetryPlot(max_points=2)

        try:
            for index in range(3):
                plot.update(
                    make_mock_packet(index),
                    elapsed_seconds=float(index),
                )

            # Time history remains bounded
            self.assertEqual(list(plot.times), [1.0, 2.0])

            # Every signal must retain only the latest two values
            signals = [
                plot.temperatures,
                plot.pressures,
                plot.battery_voltages,
                plot.accel_x,
                plot.accel_y,
                plot.accel_z,
                plot.gyro_x,
                plot.gyro_y,
                plot.gyro_z,
            ]

            for signal in signals:
                self.assertEqual(len(signal), 2)

            self.assertEqual(list(plot.accel_x), [101, 102])
            self.assertEqual(list(plot.gyro_z), [31, 32])
            mock_pause.assert_called()
        finally:
            plot.close()

    def test_close_marks_plot_closed(self):
        plot = LiveTelemetryPlot()

        try:
            plot.close()
            self.assertTrue(plot.closed)
        finally:
            plot.close()


if __name__ == "__main__":
    unittest.main()
