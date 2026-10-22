
# Telemetry Protocol and UART Communication

## 1. Overview

The Satellite Telemetry System uses a structured, comma-separated text packet to transfer sensor and battery measurements from an ESP32 to a Python ground station.

The current communication path is USB serial at 115200 baud. The ESP32 transmits newline-terminated packets, and the Python receiver reads and parses the incoming stream.

Each packet contains a packet identifier, sequence number, sensor measurements, battery voltage, and an XOR checksum.

## 2. Serial Communication Configuration

| Parameter | Value |
|---|---|
| Controller | ESP32 DevKit |
| Computer connection | USB serial |
| Baud rate | 115200 |
| Packet format | Comma-separated text |
| Packet identifier | `AKTD` |
| Packet delimiter | Comma (`,`) |
| Packet termination | Newline |
| Checksum format | Two-digit uppercase hexadecimal XOR |

The serial receiver uses a configured device path. On Fedora, available serial devices can be inspected with:

```bash
ls -l /dev/serial/by-id/
```

On Windows, configure the receiver with the COM port assigned to the ESP32 in Device Manager.

Only one application should normally own the serial port at a time. Close other serial-monitor applications before starting the Python receiver.

## 3. Packet Structure

The packet has 12 comma-separated fields:

```text
AKTD,sequence,temperature_C,pressure_hPa,accel_x,accel_y,accel_z,gyro_x,gyro_y,gyro_z,battery_V,checksum
```

The packet ends with a newline character.

### Field Definitions

| Index | Field | Description |
|---:|---|---|
| 1 | `AKTD` | Packet identifier |
| 2 | `sequence` | Packet sequence number |
| 3 | `temperature_C` | Temperature in degrees Celsius |
| 4 | `pressure_hPa` | Atmospheric pressure in hectopascals |
| 5 | `accel_x` | Raw accelerometer X-axis count |
| 6 | `accel_y` | Raw accelerometer Y-axis count |
| 7 | `accel_z` | Raw accelerometer Z-axis count |
| 8 | `gyro_x` | Gyroscope X-axis count after configured bias correction |
| 9 | `gyro_y` | Gyroscope Y-axis count after configured bias correction |
| 10 | `gyro_z` | Gyroscope Z-axis count after configured bias correction |
| 11 | `battery_V` | Calculated battery voltage in volts |
| 12 | `checksum` | XOR checksum represented as two uppercase hexadecimal digits |

The parser expects the `AKTD` identifier and the documented field count. The checksum and numeric fields are also validated.

`AKTD` is the project's packet identifier. It is not a claim that the current prototype communicates with a satellite.

## 4. Sequence Number

The sequence field identifies the packet's position in the transmitted sequence.

The ground station uses sequence information to track reception behavior, including sequence gaps, duplicate observations, and out-of-order packets.

Sequence anomalies can help identify possible transmission or reception problems, but they do not by themselves establish the underlying cause.

## 5. XOR Checksum

The packet includes a two-digit uppercase hexadecimal XOR checksum.

The documented checksum rule is:

1. Start with the packet payload before the final comma that introduces the checksum.
2. Treat the payload as bytes.
3. XOR the payload bytes together.
4. Represent the result as two uppercase hexadecimal digits.
5. Append the checksum as the final comma-separated field.

The checksum field itself is excluded from the checksum calculation.

### Conceptual Example

For a payload represented by bytes \(b_1, b_2, \ldots, b_n\), the checksum is:

\[
C = b_1 \oplus b_2 \oplus \cdots \oplus b_n
\]

where \(\oplus\) denotes the bitwise XOR operation.

The actual implementation in the firmware and parser is the authoritative reference for the precise byte handling and checksum calculation.

An XOR checksum provides basic accidental-corruption detection. It is not a cryptographic integrity check and does not protect against deliberate packet modification.

## 6. Packet Framing

Each packet is terminated by a newline. The receiver uses this delimiter to identify packet boundaries in the serial stream.

The receiver must not assume that one serial read always corresponds to exactly one complete packet. Serial reads may return partial data or multiple packets, depending on buffering and timing.

Malformed packets, packets with an invalid identifier, incorrect field counts, invalid checksums, or non-numeric measurement fields should not be treated as valid telemetry.

Refer to the implementation in:

- `firmware/telemetry_node/`
- `ground_station/parser.py`
- `ground_station/serial_receiver.py`

## 7. Ground-Station Validation

The Python ground station performs the following documented checks:

1. Packet identifier validation.
2. Expected field-count validation.
3. XOR checksum validation.
4. Numeric-field validation.
5. Packet sequence monitoring.
6. Reception and fault statistics.

Valid telemetry can be displayed in the terminal dashboard, appended to the CSV log, and shown in live plots.

The receiver also has retry handling for serial exceptions and periods without valid telemetry. Serial-port discovery is not fully automatic; the configured device path may need updating.

## 8. Telemetry Logging

The default CSV output path is:

```text
logs/telemetry_log.csv
```

The log contains a timestamp, sequence number, temperature, pressure, acceleration axes, gyroscope axes, and battery voltage.

The logger appends to an existing file. Back up or rename the log before starting a new dataset if previous measurements need to be preserved separately.

The log path is relative to the working directory, so start the receiver from the repository root.

## 9. Running the Ground Station

Activate the project's Python virtual environment:

```bash
source .venv/bin/activate
```

Start the receiver from the repository root:

```bash
python -m ground_station.serial_receiver
```

Stop the receiver with `Ctrl+C`.

If the connection fails:

1. Confirm that the ESP32 is connected and running.
2. Check the available serial-device paths.
3. Verify that the configured port matches the device.
4. Confirm the baud rate is 115200.
5. Close other applications using the serial port.
6. Confirm that the firmware and parser use the same packet structure and checksum rule.

## 10. Protocol Limitations

- The packet format is plain comma-separated text.
- The protocol uses a simple XOR checksum.
- Sensor values are not all calibrated physical measurements; IMU axes are raw counts.
- Battery voltage requires calibration against an independent measurement.
- Sequence anomalies help identify reception irregularities but do not diagnose their cause.
- Long-duration communication and reconnect behavior require further testing.
- The protocol has not been validated for safety-critical or flight-critical operation.

## 11. Potential Improvements

Possible future enhancements include:

1. Explicit protocol versioning.
2. Configurable packet-rate and sequence-number handling.
3. Additional malformed-packet and checksum-failure tests.
4. Integration tests using recorded serial packets.
5. Clearer receiver connection-state reporting.
6. Long-duration packet-loss and reconnect measurements.
7. More robust framing and error recovery if the protocol requirements expand.

These are proposed improvements, not claims of existing functionality.
