# System Architecture

## Overview

The Satellite Telemetry System is a modular embedded system designed to acquire environmental and inertial sensor data, package it into a standardized telemetry packet, and transmit it to a Ground Station for real-time monitoring, logging, and analysis.

The system follows a layered architecture to ensure modularity, scalability, and ease of maintenance. Each subsystem is responsible for a single task, allowing future expansion such as LoRa communication, GPS integration, SD card logging, and cloud connectivity without major modifications to the existing firmware.

---

# System Architecture

```
                           +----------------------+
                           |     Ground Station   |
                           |----------------------|
                           | Python Application   |
                           | Dashboard            |
                           | Data Logger          |
                           | Fault Detection      |
                           +----------▲-----------+
                                      │
                         UART (Current) / LoRa (Future)
                                      │
                           +----------▼-----------+
                           |      ESP32           |
                           |----------------------|
                           | Telemetry Protocol   |
                           | Packet Builder       |
                           | Checksum Generator   |
                           +----------▲-----------+
                                      │
               ┌──────────────────────┼──────────────────────┐
               │                      │                      │
               ▼                      ▼                      ▼
         +-----------+         +-------------+       +--------------+
         | MPU6050   |         |  BMP280     |       | Battery       |
         | IMU       |         | Pressure    |       | Monitoring    |
         +-----------+         +-------------+       +--------------+
               │                      │                      │
               └──────────────┬───────┴──────────────┬──────┘
                              ▼                      ▼
                        Sensor Acquisition     Power Monitoring
                                      │
                                      ▼
                             TelemetryData Structure
                                      │
                                      ▼
                             Telemetry Packet Builder
                                      │
                                      ▼
                             UART / LoRa Transmission
```

---

# Hardware Architecture

The telemetry node is built around the ESP32 microcontroller, which acts as the central processing unit.

## Hardware Components

| Component | Purpose |
|----------|---------|
| ESP32 DevKit V1 | Main Controller |
| MPU6050 | Inertial Measurement Unit (Acceleration & Angular Velocity) |
| BMP280 | Temperature, Pressure and Altitude Sensor |
| SSD1306 OLED | Local Telemetry Display |
| TP4056 | Battery Charging & Protection |
| XL6009 | Boost Converter |
| 18650 Battery | Portable Power Source |

---

# Software Architecture

The firmware is divided into independent modules.

```
main.cpp
    │
    ├──────── bmp280.cpp
    │
    ├──────── mpu6050.cpp
    │
    ├──────── battery.cpp
    │
    ├──────── telemetry.cpp
    │
    ├──────── protocol.cpp
    │
    └──────── oled.cpp
```

Each module performs a single responsibility.

---

## Module Description

### main.cpp

Responsible for:

- Initializing peripherals
- Calling sensor update functions
- Creating telemetry packets
- Updating the OLED
- Sending telemetry data

---

### bmp280.cpp

Responsible for:

- Initializing the BMP280
- Reading temperature
- Reading pressure
- Calculating altitude

---

### mpu6050.cpp

Responsible for:

- Initializing MPU6050
- Sensor calibration
- Reading accelerometer
- Reading gyroscope
- Roll calculation
- Pitch calculation

---

### battery.cpp

Responsible for:

- ADC configuration
- Battery voltage measurement
- Voltage filtering
- Battery percentage calculation

---

### telemetry.cpp

Responsible for:

- Maintaining the shared telemetry data structure
- Formatting telemetry information
- Printing diagnostic information

---

### protocol.cpp

Responsible for:

- Creating telemetry packets
- Packet numbering
- Timestamp generation
- Status flag generation
- Checksum calculation
- UART transmission

---

### oled.cpp

Responsible for:

- OLED initialization
- Displaying real-time telemetry
- Display refresh

---

# Data Flow

The firmware follows the following sequence during each execution cycle.

```
Read Sensors
      │
      ▼
Update TelemetryData
      │
      ▼
Build Telemetry Packet
      │
      ▼
Generate Checksum
      │
      ▼
UART Transmission
      │
      ▼
Ground Station
```

---

# Telemetry Workflow

```
MPU6050
        │
BMP280  │
Battery │
        ▼
Sensor Drivers
        ▼
TelemetryData
        ▼
Telemetry Packet
        ▼
Checksum
        ▼
Serial.write()
        ▼
Ground Station
```

---

# Ground Station Architecture

The Ground Station is implemented in Python.

```
UART Receiver
        │
        ▼
Packet Synchronization
        ▼
Checksum Verification
        ▼
Packet Parser
        ▼
Real-Time Dashboard
        ▼
CSV Logger
        ▼
Fault Detection
```

---

# Power Architecture

```
USB
 │
 ▼
TP4056 Charger
 │
 ├──────────► 18650 Battery
 │
 └──────────► XL6009 Boost Converter
                    │
                    ▼
                 ESP32 VIN

Battery Voltage
        │
Voltage Divider
        │
GPIO34 ADC
```

---

# Communication Architecture

Current communication method:

```
ESP32
   │
UART
   │
USB
   │
Laptop
```

Future communication architecture:

```
ESP32
   │
SX1262 LoRa
   │
Wireless Link
   │
SX1262 LoRa
   │
USB UART
   │
Ground Station
```

The telemetry packet format remains identical for both UART and LoRa communication.

---

# Design Principles

The firmware has been designed according to the following principles:

- Modular architecture
- Separation of responsibilities
- Hardware abstraction
- Scalable communication protocol
- Reusable sensor drivers
- Transport-independent telemetry protocol

---

# Future Enhancements

The current architecture allows seamless integration of additional features such as:

- LoRa Communication
- GPS Receiver
- SD Card Data Logging
- Real-Time Clock (RTC)
- Error Correction (CRC16)
- Command and Control Packets
- Bidirectional Communication
- Cloud Connectivity
- Web Dashboard
- OTA Firmware Updates

---

# Summary

The Satellite Telemetry System is built using a layered and modular architecture that separates hardware abstraction, sensor acquisition, telemetry generation, communication, and visualization into independent modules. This design simplifies maintenance, improves code reusability, and enables future expansion without requiring significant changes to the existing firmware.