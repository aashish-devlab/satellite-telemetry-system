"""
===========================================================
Satellite Telemetry System
Ground Station Protocol Definition
===========================================================

This module defines the telemetry packet format used by
the ESP32 telemetry node and the Ground Station.

Author : Aashish Kumar
===========================================================
"""

import struct

# =========================================================
# Packet Constants
# =========================================================

PACKET_HEADER = 0xAA55
PACKET_FOOTER = 0x55AA

PACKET_ID_TELEMETRY = 0x01

# =========================================================
# Status Flags
# =========================================================

STATUS_OK = 0x00

STATUS_LOW_BATTERY = 0x01
STATUS_HIGH_TEMP = 0x02
STATUS_BMP_ERROR = 0x04
STATUS_MPU_ERROR = 0x08
STATUS_SENSOR_TIMEOUT = 0x10

# =========================================================
# Packet Structure
#
# <  -> Little Endian
#
# H  -> uint16
# B  -> uint8
# I  -> uint32
# f  -> float
#
# Matches protocol.h exactly
# =========================================================

PACKET_FORMAT = "<H B H I f f f f f f B B B H"

PACKET_SIZE = struct.calcsize(PACKET_FORMAT)

# =========================================================
# Packet Field Index
# =========================================================

HEADER_INDEX = 0
PACKET_ID_INDEX = 1
PACKET_COUNTER_INDEX = 2
TIMESTAMP_INDEX = 3

TEMPERATURE_INDEX = 4
PRESSURE_INDEX = 5
ALTITUDE_INDEX = 6

ROLL_INDEX = 7
PITCH_INDEX = 8

BATTERY_VOLTAGE_INDEX = 9
BATTERY_PERCENT_INDEX = 10

STATUS_INDEX = 11

CHECKSUM_INDEX = 12

FOOTER_INDEX = 13

# =========================================================
# XOR Checksum
# =========================================================

def calculate_checksum(data: bytes) -> int:
    """
    Calculate XOR checksum.

    Parameters
    ----------
    data : bytes

    Returns
    -------
    checksum : int
    """

    checksum = 0

    for byte in data:
        checksum ^= byte

    return checksum

# =========================================================
# Decode Packet
# =========================================================

def decode_packet(packet: bytes):
    """
    Decode a binary telemetry packet.

    Parameters
    ----------
    packet : bytes

    Returns
    -------
    tuple
    """

    return struct.unpack(PACKET_FORMAT, packet)