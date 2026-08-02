# Telemetry Protocol and UART Communication

## Overview

The Satellite Telemetry System uses a custom binary telemetry protocol to transmit real-time sensor data from the ESP32 telemetry node to the Ground Station.

The communication is currently performed over UART through the ESP32's USB interface. The protocol has been designed to be transport-independent, allowing the same packet format to be transmitted over LoRa in future versions without modifying the packet parser or Ground Station software.

---

# Communication Architecture

```
+------------------+
|   Sensor Nodes   |
+------------------+
        │
        ▼
+------------------+
| ESP32 Telemetry  |
|      Node        |
+------------------+
        │
        │ UART (115200 Baud)
        ▼
+------------------+
| USB Interface    |
+------------------+
        │
        ▼
+------------------+
| Ground Station   |
| Python Software  |
+------------------+
```

---

# Why a Binary Protocol?

Instead of sending human-readable text such as:

```
Temperature: 32.4
Pressure: 978
Battery: 82%
```

the telemetry node sends compact binary packets.

Advantages include:

- Lower bandwidth
- Faster transmission
- Fixed packet size
- Easy packet parsing
- Lower CPU overhead
- Suitable for UART, LoRa, BLE and RF communication

---

# Telemetry Packet Structure

Each transmitted packet contains the following fields.

| Field | Data Type | Size (Bytes) | Description |
|--------|-----------|-------------:|------------|
| Header | uint16_t | 2 | Start of packet (0xAA55) |
| Packet ID | uint8_t | 1 | Packet type identifier |
| Packet Counter | uint16_t | 2 | Sequential packet number |
| Timestamp | uint32_t | 4 | System uptime (milliseconds) |
| Temperature | float | 4 | BMP280 temperature |
| Pressure | float | 4 | BMP280 pressure |
| Altitude | float | 4 | Calculated altitude |
| Roll | float | 4 | MPU6050 roll angle |
| Pitch | float | 4 | MPU6050 pitch angle |
| Battery Voltage | float | 4 | Battery voltage |
| Battery Percentage | uint8_t | 1 | Battery charge level |
| Status Flags | uint8_t | 1 | System status |
| Checksum | uint8_t | 1 | Error detection |
| Footer | uint16_t | 2 | End of packet (0x55AA) |

---

# Packet Layout

```
+-------------------------------------------------------+
| Header (0xAA55)                                       |
+-------------------------------------------------------+
| Packet ID                                             |
+-------------------------------------------------------+
| Packet Counter                                        |
+-------------------------------------------------------+
| Timestamp                                             |
+-------------------------------------------------------+
| Temperature                                            |
+-------------------------------------------------------+
| Pressure                                               |
+-------------------------------------------------------+
| Altitude                                               |
+-------------------------------------------------------+
| Roll                                                   |
+-------------------------------------------------------+
| Pitch                                                  |
+-------------------------------------------------------+
| Battery Voltage                                        |
+-------------------------------------------------------+
| Battery Percentage                                     |
+-------------------------------------------------------+
| Status Flags                                           |
+-------------------------------------------------------+
| Checksum                                               |
+-------------------------------------------------------+
| Footer (0x55AA)                                        |
+-------------------------------------------------------+
```

---

# Header

```
0xAA55
```

The header indicates the beginning of a telemetry packet.

The Ground Station continuously scans the incoming serial stream until this value is detected.

Purpose:

- Packet synchronization
- Detect packet start
- Recover from corrupted data

---

# Footer

```
0x55AA
```

The footer indicates the end of the packet.

Purpose:

- Packet termination
- Detection of incomplete packets
- Additional packet validation

---

# Packet ID

Packet IDs allow multiple packet types to share the same communication channel.

| Packet ID | Description |
|-----------|-------------|
| 0x01 | Telemetry Packet |
| 0x02 | Command Packet (Future) |
| 0x03 | Acknowledgement Packet (Future) |
| 0x04 | Configuration Packet (Future) |

Current implementation uses:

```
0x01
```

---

# Packet Counter

Every transmitted packet increments an internal counter.

Example:

```
1
2
3
4
5
6
```

Purpose:

- Detect packet loss
- Monitor communication reliability
- Measure packet transmission rate

Example:

```
101
102
104
```

Packet **103** has been lost.

---

# Timestamp

Timestamp is generated using:

```cpp
millis()
```

Purpose:

- Determine packet generation time
- Calculate transmission frequency
- Detect communication delays
- Measure system uptime

---

# Sensor Payload

The payload contains all real-time telemetry values.

```
Temperature
Pressure
Altitude
Roll
Pitch
Battery Voltage
Battery Percentage
```

Each value is stored using binary floating-point or integer representation to reduce packet size.

---

# Status Flags

Status flags occupy one byte.

Each bit represents one system condition.

| Bit | Meaning |
|-----|---------|
| Bit 0 | Low Battery |
| Bit 1 | High Temperature |
| Bit 2 | BMP280 Error |
| Bit 3 | MPU6050 Error |
| Bit 4 | Sensor Timeout |
| Bit 5 | Reserved |
| Bit 6 | Reserved |
| Bit 7 | Reserved |

Example:

```
00000001
```

Indicates:

```
Low Battery
```

Example:

```
00001001
```

Indicates:

```
Low Battery
MPU6050 Error
```

---

# Checksum

The checksum provides simple packet error detection.

The current implementation uses an XOR checksum.

Algorithm:

```cpp
checksum = 0;

for(each byte)
{
    checksum ^= byte;
}
```

Receiver performs the same calculation.

If

```
Received Checksum == Calculated Checksum
```

the packet is accepted.

Otherwise,

```
Packet Discarded
```

---

# UART Communication

## Communication Parameters

| Parameter | Value |
|-----------|-------|
| Baud Rate | 115200 bps |
| Data Bits | 8 |
| Parity | None |
| Stop Bits | 1 |
| Flow Control | None |

Communication format:

```
115200 8N1
```

---

# Why UART?

UART was selected during development because it provides:

- Reliable wired communication
- Easy debugging
- High transfer speed
- Simple Python integration
- Direct USB interface

It allows verification of the telemetry protocol before introducing wireless communication.

---

# Serial Transmission

The telemetry packet is transmitted using

```cpp
Serial.write()
```

instead of

```cpp
Serial.println()
```

### Serial.println()

```
Temperature:31.42
Pressure:977.20
Battery:82%
```

Human readable

Large packet size

Debugging only

---

### Serial.write()

```
AA 55 01 ...
```

Binary packet

Small packet size

Fast transmission

Easy parsing

Production communication

---

# Communication Workflow

```
Read Sensors
      │
      ▼
Update TelemetryData
      │
      ▼
Create Telemetry Packet
      │
      ▼
Generate Status Flags
      │
      ▼
Calculate Checksum
      │
      ▼
Serial.write(Packet)
      │
      ▼
USB UART
      │
      ▼
Ground Station
```

---

# Ground Station Responsibilities

The Ground Station performs the following operations:

1. Open UART port
2. Receive binary packets
3. Synchronize using the packet header
4. Verify packet checksum
5. Decode telemetry values
6. Display real-time telemetry
7. Log data to CSV
8. Detect communication faults

---

# Future LoRa Migration

The protocol has been intentionally designed to be independent of the communication medium.

Current communication:

```
ESP32
   │
UART
   │
USB
   │
Ground Station
```

Future communication:

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

No changes to the packet format or Ground Station parser are required.

---

# Design Goals

The telemetry protocol has been designed with the following objectives:

- Modular architecture
- Fixed packet size
- Low communication overhead
- Error detection
- Easy synchronization
- Expandability
- Hardware independence
- Compatibility with UART and LoRa

---

# Conclusion

The custom telemetry protocol provides a reliable and scalable method for transmitting real-time sensor data from the telemetry node to the Ground Station. By combining structured binary packets, packet synchronization, checksum verification, and a transport-independent design, the system is prepared for future expansion from wired UART communication to long-range LoRa communication while maintaining a consistent software architecture.