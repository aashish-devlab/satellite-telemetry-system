
from collections import deque

import matplotlib.pyplot as plt


class LiveTelemetryPlot:
    """Plot environmental, battery, and IMU telemetry in real time."""

    def __init__(self, max_points=100):
        self.max_points = max_points

        self.times = deque(maxlen=max_points)
        self.temperatures = deque(maxlen=max_points)
        self.pressures = deque(maxlen=max_points)
        self.battery_voltages = deque(maxlen=max_points)

        self.accel_x = deque(maxlen=max_points)
        self.accel_y = deque(maxlen=max_points)
        self.accel_z = deque(maxlen=max_points)
        self.gyro_x = deque(maxlen=max_points)
        self.gyro_y = deque(maxlen=max_points)
        self.gyro_z = deque(maxlen=max_points)

        self.closed = False

        plt.ion()
        self.figure, self.axes = plt.subplots(
            5, 1, figsize=(11, 12), sharex=True
        )
        self.figure.suptitle("Satellite Telemetry — Live Monitor")

        self.temperature_line, = self.axes[0].plot([], [], label="Temperature")
        self.pressure_line, = self.axes[1].plot([], [], label="Pressure")
        self.battery_line, = self.axes[2].plot([], [], label="Battery")

        self.accel_x_line, = self.axes[3].plot([], [], label="Accel X")
        self.accel_y_line, = self.axes[3].plot([], [], label="Accel Y")
        self.accel_z_line, = self.axes[3].plot([], [], label="Accel Z")

        self.gyro_x_line, = self.axes[4].plot([], [], label="Gyro X")
        self.gyro_y_line, = self.axes[4].plot([], [], label="Gyro Y")
        self.gyro_z_line, = self.axes[4].plot([], [], label="Gyro Z")

        self.axes[0].set_ylabel("Temperature (°C)")
        self.axes[1].set_ylabel("Pressure (hPa)")
        self.axes[2].set_ylabel("Battery (V)")
        self.axes[3].set_ylabel("Acceleration")
        self.axes[4].set_ylabel("Gyroscope")
        self.axes[4].set_xlabel("Elapsed time (s)")

        self.axes[3].legend(loc="upper right", ncols=3)
        self.axes[4].legend(loc="upper right", ncols=3)

        for axis in self.axes:
            axis.grid(True)

        self.figure.tight_layout()
        self.figure.show()
        self.figure.canvas.draw()

    def update(self, packet, elapsed_seconds):
        """Add one validated telemetry packet and refresh the plots."""
        if self.closed:
            return

        self.times.append(elapsed_seconds)
        self.temperatures.append(packet.temperature_c)
        self.pressures.append(packet.pressure_hpa)
        self.battery_voltages.append(packet.battery_v)

        self.accel_x.append(packet.accel_x)
        self.accel_y.append(packet.accel_y)
        self.accel_z.append(packet.accel_z)

        self.gyro_x.append(packet.gyro_x)
        self.gyro_y.append(packet.gyro_y)
        self.gyro_z.append(packet.gyro_z)

        self.temperature_line.set_data(self.times, self.temperatures)
        self.pressure_line.set_data(self.times, self.pressures)
        self.battery_line.set_data(self.times, self.battery_voltages)

        self.accel_x_line.set_data(self.times, self.accel_x)
        self.accel_y_line.set_data(self.times, self.accel_y)
        self.accel_z_line.set_data(self.times, self.accel_z)

        self.gyro_x_line.set_data(self.times, self.gyro_x)
        self.gyro_y_line.set_data(self.times, self.gyro_y)
        self.gyro_z_line.set_data(self.times, self.gyro_z)

        for axis in self.axes:
            axis.relim()
            axis.autoscale_view()

        self.figure.canvas.draw_idle()
        self.figure.canvas.flush_events()
        plt.pause(0.001)

    def close(self):
        """Close the graph window safely."""
        if not self.closed:
            self.closed = True
            plt.close(self.figure)
