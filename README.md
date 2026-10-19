# Satellite Telemetry System

An ESP32-based telemetry system that collects environmental, motion, and battery measurements, displays selected readings locally, and transmits structured telemetry packets to a computer over USB serial.

## Current Features

- **Environmental sensing:** BMP280 temperature and atmospheric pressure readings.
- **Motion sensing:** IMU acceleration and gyroscope raw readings.
- **Battery monitoring:** Battery voltage measurement using an ESP32 ADC and voltage divider.
- **Local display:** SSD1306 128×64 OLED over I²C.
- **Telemetry packets:** Comma-separated `AKTD` packets containing a sequence number, sensor measurements, battery voltage, and XOR checksum.
- **Serial output:** Telemetry transmission over USB serial at 115200 baud.

## Hardware

| Component | Interface | Status |
|---|---|---|
| ESP32 DevKit | USB serial, I²C, ADC | Main controller |
| BMP280 | I²C, address `0x76` | Tested |
| IMU module | I²C, address `0x68` | Raw register readings tested; exact sensor identity and calibration need verification |
| SSD1306 OLED | I²C, address `0x3C` | Tested |
| Battery voltage divider | ADC, GPIO34 | Tested with multiple batteries |

The I²C bus uses GPIO21 for SDA and GPIO22 for SCL.

## Repository Structure

```text
satellite-telemetry-system/
├── docs/
├── firmware/
│   └── telemetry_node/
│       ├── include/
│       ├── src/
│       ├── platformio.ini
│       └── .gitignore
├── ground_station/
├── tests/
├── .gitignore
└── README.md
```

## Firmware Setup

1. Install Visual Studio Code and the PlatformIO extension.
2. Open `firmware/telemetry_node/` as the PlatformIO project.
3. Build the project for the ESP32 DevKit target.
4. Connect the ESP32 and upload the firmware.
5. Open the serial monitor at **115200 baud**.

## Telemetry Protocol

The current text packet uses this field order:

```text
AKTD,sequence,temperature_C,pressure_hPa,accel_x,accel_y,accel_z,gyro_x,gyro_y,gyro_z,battery_V,checksum
```

- `AKTD`: packet identifier.
- `sequence`: packet sequence number.
- `temperature_C`: temperature in degrees Celsius.
- `pressure_hPa`: pressure in hectopascals.
- `accel_x`, `accel_y`, `accel_z`: raw IMU acceleration readings.
- `gyro_x`, `gyro_y`, `gyro_z`: corrected raw gyroscope counts.
- `battery_V`: measured battery voltage in volts.
- `checksum`: XOR checksum of the payload bytes before the final comma and checksum, represented as two hexadecimal digits.

Each packet ends with a newline. The checksum provides basic error detection and is not a cryptographic integrity mechanism.

## Current Limitations

- The IMU's exact identity and physical-unit calibration are not yet confirmed.
- Sensor failure handling and telemetry packet validation need further testing.
- The Python ground station, packet parser, data logger, and dashboard are not yet implemented.

