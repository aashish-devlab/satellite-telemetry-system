
# Satellite Telemetry System

An ESP32-based telemetry prototype that collects environmental, motion, and battery measurements, displays selected readings on an SSD1306 OLED, and transmits structured telemetry packets to a computer over USB serial. A Python ground station validates incoming packets, tracks reception statistics, logs readings to CSV, and plots live telemetry.

> **Project status:** The core firmware-to-ground-station workflow, telemetry packet handling, and live plotting have been implemented. The latest reported Python test run passed 27 tests. Sensor accuracy, battery-voltage calibration, and sudden measurement changes observed during live testing still require investigation. This project is a prototype and has not been validated for flight-critical use.

## Features

### ESP32 Firmware

- BMP280 temperature and atmospheric pressure readings over I²C.
- IMU accelerometer and gyroscope readings using MPU-6050-compatible register addresses.
- Battery-voltage measurement through the ESP32 ADC and an external voltage divider on GPIO34.
- Local sensor display on an SSD1306 128×64 OLED.
- Structured, newline-terminated telemetry packets transmitted over USB serial at 115200 baud.
- XOR checksum generation using a two-digit uppercase hexadecimal representation.

### Python Ground Station

- USB serial communication with the ESP32.
- Telemetry packet parsing and validation.
- Packet sequence monitoring and reception statistics.
- Duplicate and out-of-order packet detection.
- Terminal dashboard for displaying telemetry and reception information.
- CSV logging of received telemetry.
- Live graphs for temperature, pressure, battery voltage, acceleration axes, and gyroscope axes.
- Serial reconnection and retry handling after connection errors or periods without valid telemetry.

## Hardware Components

| Component | Interface / Configuration | Purpose |
|---|---|---|
| ESP32 DevKit | USB serial, I²C, ADC | Main controller |
| BMP280 | I²C address `0x76` | Temperature and atmospheric pressure |
| IMU | I²C address `0x68` | Acceleration and gyroscope readings |
| SSD1306 OLED | I²C address `0x3C` | Local telemetry display |
| Battery voltage divider | ESP32 GPIO34 / ADC | Battery-voltage measurement |

### I²C Pin Configuration

| Signal | ESP32 GPIO |
|---|---|
| SDA | GPIO21 |
| SCL | GPIO22 |

The IMU identity and calibration must be verified. The firmware uses MPU-6050-compatible register addresses, and the plotted IMU values are raw counts rather than calibrated physical units.

The battery-voltage measurement uses configured divider and correction values. Compare the reading with a reliable multimeter before relying on the result.

## System Architecture

The current data path is:

1. Sensors and the battery-monitor circuit provide measurements to the ESP32.
2. The firmware reads sensor values and updates the OLED.
3. The firmware constructs a telemetry packet and calculates its XOR checksum.
4. The ESP32 transmits newline-terminated packets over USB serial.
5. The Python ground station receives and validates packets.
6. Valid telemetry is displayed, logged to CSV, and plotted.

See [System Architecture](docs/system_architecture.md) for the detailed design and data flow.

## Repository Structure

```text
satellite-telemetry-system/
├── docs/
│   ├── evidence/
│   │   ├── hardware/
│   │   ├── ground-station/
│   │   ├── tests/
│   │   └── diagrams/
│   ├── system_architecture.md
│   └── telemetry_protocol_and_uart_communication.md
├── firmware/
│   └── telemetry_node/
├── ground_station/
│   ├── parser.py
│   ├── faults.py
│   ├── logger.py
│   ├── dashboard.py
│   ├── live_plot.py
│   └── serial_receiver.py
└── README.md
```

The evidence folders are intended for genuine project photographs, actual ground-station screenshots, test output, and diagrams. Add image files only after capturing or creating the corresponding evidence. The `logs/` directory is used for local telemetry data and should not be committed indiscriminately.

## Firmware Setup

1. Install Visual Studio Code and the PlatformIO extension.
2. Open `firmware/telemetry_node/` as the PlatformIO project.
3. Build the project for the configured ESP32 target.
4. Connect the ESP32 and upload the firmware.
5. Confirm that the firmware transmits telemetry packets over USB serial at 115200 baud.

The firmware currently emits a telemetry packet only when the IMU, BMP280, and battery-read functions all report success.

## Ground Station Setup

Run the following commands from the repository root.

### 1. Create or activate the virtual environment

If `.venv` already exists:

```bash
source .venv/bin/activate
```

If it does not exist:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install pyserial matplotlib
```

### 2. Identify the ESP32 serial port

On Fedora, run:

```bash
ls -l /dev/serial/by-id/
```

The previously configured device path was:

```text
/dev/serial/by-id/usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0001-if00-port0
```

The path may differ on another computer or after reconnecting the device. Use the path reported by your system.

### 3. Start the ground station

With `.venv` activated and the ESP32 connected:

```bash
python -m ground_station.serial_receiver
```

The receiver opens the configured serial port, receives telemetry, and starts the configured dashboard, CSV logger, and live plots.

Stop the application with `Ctrl+C`.

### Windows serial-port configuration

The receiver contains a commented Windows example:

```python
# PORT = "COM3"
```

On Windows, identify the ESP32 COM port in Device Manager and configure `PORT` in `ground_station/serial_receiver.py` accordingly. The actual port may not be `COM3`.

## Telemetry Protocol

The current packet format is:

```text
AKTD,sequence,temperature_C,pressure_hPa,accel_x,accel_y,accel_z,gyro_x,gyro_y,gyro_z,battery_V,checksum
```

Each packet ends with a newline. The checksum is a two-digit uppercase hexadecimal XOR checksum calculated over the payload bytes before the final comma.

See [Telemetry Protocol and UART Communication](docs/telemetry_protocol_and_uart_communication.md) for the field definitions, serial configuration, and validation behavior.

## Ground Station Modules

| Module | Responsibility |
|---|---|
| `serial_receiver.py` | Opens the serial connection and coordinates telemetry reception |
| `parser.py` | Validates packet identifier, field count, checksum, and numeric fields |
| `faults.py` | Tracks sequence anomalies, including duplicates and out-of-order packets |
| `dashboard.py` | Displays the latest telemetry and reception statistics |
| `logger.py` | Appends parsed telemetry to a CSV file |
| `live_plot.py` | Plots recent telemetry measurements |

The live plotting implementation keeps a bounded recent history of 100 points by default.

## Logs and Testing

### CSV telemetry log

The default output path is:

```text
logs/telemetry_log.csv
```

The logger appends timestamps and parsed telemetry values to the existing CSV file. The path is relative to the current working directory, so start the receiver from the repository root.

Keep generated logs local unless you intentionally select and sanitize a sample for publication.

### Run the test suite

With the virtual environment activated, run:

```bash
python -m unittest discover -s ground_station -p 'test_*.py' -v
```

The latest previously reported run passed **27 tests**. Run the command again after code changes to establish the current result.

The tests cover ground-station software behavior, including packet parsing, fault detection, reception statistics, logging, dashboard behavior, and live plotting. Passing software tests does not establish sensor accuracy or hardware reliability.


## Current Limitations

- **Sensor-reading changes:** A live session showed a sudden battery-voltage drop and changes in temperature and pressure around the same time. The cause has not been established.
- **IMU calibration:** Sensor identity, configuration, scale factors, and gyroscope bias correction require verification.
- **Serial configuration:** The serial port is configured explicitly and may need manual updating.
- **Protocol limitations:** The protocol uses newline-delimited text and an XOR checksum. XOR is for basic accidental-corruption detection, not cryptographic security.
- **Long-duration validation:** Extended logging, repeated disconnect/reconnect behavior, and sensor recovery require additional testing.
- **Hardware reliability:** Software tests cover only the behavior exercised by those tests. They do not prove physical measurement accuracy or flight readiness.

## Future Improvements

1. Investigate simultaneous changes in battery, temperature, and pressure readings.
2. Calibrate battery voltage against known measurements.
3. Verify the IMU identity and convert raw counts to calibrated physical units.
4. Improve sensor-value plausibility checks and error reporting.
5. Add configurable serial-port selection.
6. Test USB disconnect/reconnect recovery and long-duration operation.
7. Make the CSV output path configurable and add session identifiers.
8. Add integration tests using valid, malformed, and corrupted telemetry packets.
9. Measure long-run packet rate and packet loss.
10. Extend the wider telemetry architecture after the existing sensing and communication pipeline is validated.

## Troubleshooting

### `ModuleNotFoundError: No module named 'ground_station'`

Run commands from the repository root, activate `.venv`, and use:

```bash
python -m ground_station.serial_receiver
```

### Serial port not found

- Reconnect the ESP32.
- Run `ls -l /dev/serial/by-id/`.
- Update the configured `PORT` value if necessary.
- Close other applications that may be using the serial device.

### Permission denied on Fedora

Check the serial device permissions and your user's serial-device group membership. A new login session may be needed after changing group membership. Avoid using `sudo` as a routine workaround.

### No valid packets received

- Confirm that the firmware is running.
- Verify the baud rate is 115200.
- Close other serial-monitor applications.
- Confirm that the firmware and parser agree on the packet fields and checksum.
- Check sensor wiring and serial output.

### Implausible graph readings

Compare the CSV data with direct serial output and independent measurements. Investigate wiring, grounding, ADC configuration, calibration, sensor communication, and parsing before assuming the plot is at fault.

---

This is a learning and prototyping system. Validate hardware measurements and failure behavior before using it for safety-critical or flight-critical decisions.
