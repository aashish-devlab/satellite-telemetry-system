# 05 - BMP280 Sensor Test

## Overview

This test verifies the functionality of the **BMP280 Barometric Pressure Sensor** with the ESP32 using the I²C interface.

The program reads and displays:

- Temperature (°C)
- Atmospheric Pressure (hPa)
- Estimated Altitude (m)

The values are printed to the Serial Monitor every second.

---
## Wiring

| BMP280 | ESP32 |
|--------|-------|
| VCC | 3.3V |
| GND | GND |
| SDA | GPIO21 |
| SCL | GPIO22 |

## I²C Configuration

| Device | Address |
|---------|---------|
| BMP280 | 0x76 |

Example Output

```text
Temperature : 32.43 °C
Pressure    : 977.29 hPa
Altitude    : 303.82 m