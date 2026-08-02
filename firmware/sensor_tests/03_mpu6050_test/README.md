# MPU6050 Test

## Purpose
Verify communication with the MPU6050 over I²C and read acceleration, gyroscope, and temperature data.

## Expected Output
- Acceleration (X, Y, Z)
- Gyroscope (X, Y, Z)
- Temperature

## Wiring

| MPU6050 | ESP32 |
|----------|-------|
| VCC | 3.3V |
| GND | GND |
| SDA | GPIO21 |
| SCL | GPIO22 |