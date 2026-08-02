"""
===========================================================
Satellite Telemetry System
Ground Station - Packet Parser
===========================================================

This module is responsible for:
    - Receiving binary telemetry packets
    - Verifying packet header
    - Verifying packet footer
    - Verifying checksum
    - Decoding packet fields

Author : Aashish Kumar
===========================================================
"""

import struct

from protocol import *


class PacketParser:

    def __init__(self):
        pass

    # --------------------------------------------------
    # Verify Header
    # --------------------------------------------------
    def verify_header(self, packet):

        header = struct.unpack_from("<H", packet, 0)[0]

        return header == PACKET_HEADER

    # --------------------------------------------------
    # Verify Footer
    # --------------------------------------------------
    def verify_footer(self, packet):

        footer = struct.unpack_from("<H", packet, PACKET_SIZE - 2)[0]

        return footer == PACKET_FOOTER

    # --------------------------------------------------
    # Verify Checksum
    # --------------------------------------------------
    def verify_checksum(self, packet):

        received_checksum = packet[CHECKSUM_INDEX]

        calculated_checksum = calculate_checksum(
            packet[:-3]
        )

        return received_checksum == calculated_checksum

    # --------------------------------------------------
    # Decode Packet
    # --------------------------------------------------
    def parse(self, packet):

        if len(packet) != PACKET_SIZE:

            return None

        if not self.verify_header(packet):

            print("[ERROR] Invalid Header")

            return None

        if not self.verify_footer(packet):

            print("[ERROR] Invalid Footer")

            return None

        if not self.verify_checksum(packet):

            print("[ERROR] Checksum Failed")

            return None

        fields = decode_packet(packet)

        telemetry = {

            "packet_id": fields[PACKET_ID_INDEX],

            "packet_counter": fields[PACKET_COUNTER_INDEX],

            "timestamp": fields[TIMESTAMP_INDEX],

            "temperature": fields[TEMPERATURE_INDEX],

            "pressure": fields[PRESSURE_INDEX],

            "altitude": fields[ALTITUDE_INDEX],

            "roll": fields[ROLL_INDEX],

            "pitch": fields[PITCH_INDEX],

            "battery_voltage": fields[BATTERY_VOLTAGE_INDEX],

            "battery_percentage": fields[BATTERY_PERCENT_INDEX],

            "status": fields[STATUS_INDEX]
        }

        return telemetry