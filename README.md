
# Satellite Telemetry System

An ESP32-based telemetry system that collects environmental, motion, and battery measurements, displays selected readings on an SSD1306 OLED, and transmits structured telemetry packets to a computer over USB serial. The Python ground station validates packets, tracks reception statistics, logs readings to CSV, and plots live telemetry.

> **Status:** The core firmware-to-ground-station workflow and live plots have been implemented. The latest reported Python test run passed 27 tests. Sensor accuracy and sudden measurement changes observed during a live session still need investigation before the system can be considered fully validated.

## Features

### ESP32 Firmware
- BMP280 temperature and atmospheric pressure readings.
- Raw accelerometer and gyroscope readings from an IMU at I²C address `0x68`.
- Battery voltage measurement using the ESP32 ADC and a voltage divider on GPIO34.
- Local display on an SSD1306 128×64 OLED.
- Newline-terminated `AKTD` telemetry packets over USB serial at 115200 baud.
- Two-digit uppercase hexadecimal XOR checksum.

### Python Ground Station
- USB serial reception and packet validation.
- Valid/invalid packet and sequence-gap statistics.
- Terminal dashboard displaying telemetry and reception information.
- Append-only CSV telemetry logging.
- Live temperature, pressure, battery, accelerometer X/Y/Z, and gyroscope X/Y/Z graphs.
- Retry loop after serial errors or a period without valid telemetry.

## Hardware and Interfaces

| Component | Interface / Configuration | Notes |
|---|---|---|
| ESP32 DevKit | USB serial, I²C, ADC | Main controller |
| BMP280 | I²C address `0x76` | Temperature and pressure |
| IMU | I²C address `0x68` | Firmware uses MPU-6050 register addresses; identity and calibration need verification |
| SSD1306 OLED | I²C address `0x3C` | 128×64 display |
| Battery voltage divider | GPIO34 / ADC | Divider and correction values are configured in firmware |

I²C uses GPIO21 for SDA and GPIO22 for SCL.

The battery voltage calculation uses a configured divider ratio and correction offset. Calibrate the measurement against a reliable multimeter before relying on the reading.


## Firmware Setup

1. Install Visual Studio Code and the PlatformIO extension.
2. Open `firmware/telemetry_node/` as the PlatformIO project.
3. Build the project for the configured ESP32 DevKit target.
4. Connect the ESP32 and upload the firmware.
5. Confirm that the firmware transmits serial packets at **115200 baud**.

The firmware currently emits a telemetry packet only when the IMU, BMP280, and battery read functions all report success.

## Ground Station Setup

Run all commands from the **repository root** (`satellite-telemetry-system/`). Package-qualified imports expect the repository root to be the working directory.

### 1. Activate the Python Virtual Environment

On Fedora, if `.venv` already exists:

```bash
source .venv/bin/activate
```

If the virtual environment does not exist yet:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install pyserial matplotlib
```

The receiver uses `pyserial` (imported as `serial`) and Matplotlib for live plots.

### 2. Find the ESP32 Serial Device

Run:

```bash
ls -l /dev/serial/by-id/
```

The current Fedora configuration uses this device path:

```text
/dev/serial/by-id/usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0001-if00-port0
```

The device name can differ depending on the USB-to-UART bridge and system. Use the path shown by your machine if it changes.

### 3. Start the Ground Station

From the repository root, with `.venv` activated:

```bash
python -m ground_station.serial_receiver
```

The receiver opens the configured port at 115200 baud and starts the terminal dashboard, CSV logger, and live plots.

Keep the terminal open while the receiver runs.

Stop it with **Ctrl+C**.

## Reconnecting the ESP32

If you unplug and reconnect the ESP32:

1. Stop the receiver with **Ctrl+C** if it is still running.
2. Reconnect the ESP32 by USB and wait for Fedora to detect it.
3. Check the available serial paths:

   ```bash
   ls -l /dev/serial/by-id/
   ```

4. Activate the environment and restart the receiver:

   ```bash
   source .venv/bin/activate
   python -m ground_station.serial_receiver
   ```

5. If the serial path has changed, edit the `PORT` value near the top of `ground_station/serial_receiver.py` to match the path listed on your system, then rerun the command.

The receiver has a retry loop for serial exceptions and returns to its connection loop after the valid-packet timeout. It does not dynamically discover every possible serial device, so manually checking `/dev/serial/by-id/` is the recovery step if the configured path changes.

## Windows Serial-Port Note

The receiver contains a commented Windows example:

```python
# PORT = "COM3"
```

On Windows, comment out the Fedora path and set `PORT` to the COM port assigned to the ESP32 in Device Manager. The port may not be `COM3`.

Run the receiver from the repository root in a Python environment where the dependencies are installed.

## Telemetry Packet Format

The firmware emits this field order:

```text
AKTD,sequence,temperature_C,pressure_hPa,accel_x,accel_y,accel_z,gyro_x,gyro_y,gyro_z,battery_V,checksum
```

| Field | Meaning |
|---|---|
| `AKTD` | Packet identifier |
| `sequence` | Increasing packet sequence number |
| `temperature_C` | Temperature in degrees Celsius |
| `pressure_hPa` | Pressure in hectopascals |
| `accel_x`, `accel_y`, `accel_z` | Raw IMU acceleration counts |
| `gyro_x`, `gyro_y`, `gyro_z` | Raw gyroscope counts after configured bias correction |
| `battery_V` | Calculated battery voltage in volts |
| `checksum` | XOR checksum over payload bytes before the final comma, represented as uppercase hexadecimal |

Each packet ends with a newline.

The XOR checksum provides basic accidental-corruption detection; it is not a cryptographic integrity mechanism. IMU readings are raw counts, not calibrated physical units.

## Ground Station Components

- **Parser:** Validates the packet identifier, field count, checksum, and numeric values.
- **Reception statistics:** Tracks valid and invalid packets, runtime, reception rate, and sequence gaps.
- **Fault detection:** Checks packet sequence numbers and tracks duplicate and out-of-order observations.
- **Terminal dashboard:** Displays the latest parsed readings and reception statistics.
- **CSV logger:** Appends timestamps and parsed sensor values to `logs/telemetry_log.csv`.
- **Live graphs:** Displays temperature, pressure, battery voltage, all three accelerometer axes, and all three gyroscope axes.

The live plot keeps a bounded recent history of 100 points by default.

## Logs and Tests

### CSV Telemetry Log

Default output path:

```text
logs/telemetry_log.csv
```

The log contains a timestamp, sequence number, temperature, pressure, accelerometer axes, gyroscope axes, and battery voltage.

The path is relative to the current working directory, so launch the receiver from the repository root to keep logs in the expected location.

The logger appends to the existing CSV. Back up or rename the file before starting a fresh dataset if you want to preserve earlier measurements separately.

### Run the Complete Test Suite

From the repository root, with the virtual environment activated:

```bash
python -m unittest discover -s ground_station -p 'test_*.py' -v
```

The latest reported run passed **27 tests**.

The suite covers ground-station components, including packet parsing, fault detection, reception statistics, logging, dashboard behavior, and live plotting. Run the command again after code changes; the current test output is the definitive result.

## Current Limitations and Known Issues

- **Sudden live-reading changes:** A live graph showed a sharp battery-voltage drop and changes in temperature and pressure at approximately the same time. The cause has not been established. Possible causes include ADC or sensor behavior, power or wiring issues, or a data-path problem. Investigate before relying on these readings.
- **Battery calibration:** The divider ratio and correction offset are firmware constants. Compare the reading against a multimeter across the intended voltage range before relying on it.
- **IMU identity and calibration:** Raw counts are plotted, and gyroscope bias correction is hard-coded. Verify the sensor identity, register configuration, scale factors, and calibration before converting readings to physical units.
- **Sensor failure handling:** The firmware reports a general sensor-reading error, but recovery behavior has not been comprehensively validated.
- **Serial device selection:** The Fedora port is configured explicitly. If the path changes, `PORT` must be updated manually.
- **Protocol limitations:** Packets use newline-delimited text and a simple XOR checksum.
- **Hardware validation:** Passing Python tests verifies only the software behavior covered by those tests. It does not prove sensor accuracy, battery calibration, or long-duration hardware reliability.
- **Long-duration testing:** Repeated USB disconnect/reconnect recovery and prolonged logging still need testing on the actual hardware.

## Future Improvements

These are potential next steps, not claims of completed functionality:

1. Investigate simultaneous battery, temperature, and pressure changes using CSV timestamps, serial output, and independent measurements.
2. Add sensor-value plausibility checks and explicit warnings in the terminal dashboard.
3. Calibrate battery voltage against known voltages.
4. Verify IMU identity and configuration, then convert raw counts into calibrated physical units.
5. Add configurable serial-port selection or command-line options.
6. Add connection-state messages and tests for unplug/replug recovery.
7. Make the CSV output path configurable and add session identifiers.
8. Improve plotting with clearer units, optional axis limits, pause/resume, and plot export.
9. Add integration tests using recorded valid, malformed, and corrupted telemetry packets.
10. Measure long-run packet rate, packet loss, and resource usage.
11. Extend the wider telemetry system after sensing, packet handling, and ground-station behavior are reliable.

## Troubleshooting

### `ModuleNotFoundError: No module named 'ground_station'`

- Change to the repository root.
- Activate `.venv`.
- Run the module command instead of launching the Python file directly:

  ```bash
  python -m ground_station.serial_receiver
  ```

### Serial Port Not Found or Connection Error

- Reconnect the ESP32.
- Run `ls -l /dev/serial/by-id/`.
- Confirm that `PORT` in `ground_station/serial_receiver.py` matches the current path.
- Close other serial-monitor applications that may be using the port.

### Permission Denied When Opening the Serial Device

Check the device permissions and your Fedora user's serial-device group membership. A new login session may be required after changing group membership.

Avoid running the ground station with `sudo` as a routine workaround.

### No Valid Telemetry Packets

- Confirm that the firmware is uploaded and running.
- Check that the baud rate is 115200.
- Close other serial-monitor applications.
- Confirm that the firmware and parser agree on packet fields and checksum.
- Check ESP32 wiring and serial output.

### Implausible Graph Readings

Compare the CSV log with direct serial output and independent measurements. Investigate power, grounding, ADC divider wiring and calibration, sensor communication, and parsing before assuming the graph is at fault.

---

This is a learning and prototyping system. Validate hardware measurements and failure behavior before using it for safety-critical or flight-critical decisions.
