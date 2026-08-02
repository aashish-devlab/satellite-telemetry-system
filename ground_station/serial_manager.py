"""
===========================================================
Satellite Telemetry System
Ground Station - Serial Manager
===========================================================

This module handles UART communication with the ESP32
Telemetry Node.

Responsibilities:
    - Open serial port
    - Read raw bytes
    - Write raw bytes
    - Close connection

Author : Aashish Kumar
===========================================================
"""

import serial
import serial.tools.list_ports


class SerialManager:

    def __init__(self,
                 port="/dev/ttyUSB0",
                 baudrate=115200,
                 timeout=1):

        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout

        self.serial_port = None

    # --------------------------------------------------
    # Open UART
    # --------------------------------------------------
    def connect(self):

        try:

            self.serial_port = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=self.timeout
            )

            print(f"[INFO] Connected to {self.port}")

            return True

        except Exception as e:

            print(f"[ERROR] {e}")

            return False

    # --------------------------------------------------
    # Close UART
    # --------------------------------------------------
    def disconnect(self):

        if self.serial_port:

            self.serial_port.close()

            print("[INFO] Serial Port Closed")

    # --------------------------------------------------
    # Read Bytes
    # --------------------------------------------------
    def read(self, size):

        if self.serial_port:

            return self.serial_port.read(size)

        return None

    # --------------------------------------------------
    # Write Bytes (Future Commands)
    # --------------------------------------------------
    def write(self, data):

        if self.serial_port:

            self.serial_port.write(data)

    # --------------------------------------------------
    # Bytes Waiting
    # --------------------------------------------------
    def available(self):

        if self.serial_port:

            return self.serial_port.in_waiting

        return 0

    # --------------------------------------------------
    # Connection Status
    # --------------------------------------------------
    def is_connected(self):

        if self.serial_port:

            return self.serial_port.is_open

        return False


# ------------------------------------------------------
# List Available Serial Ports
# ------------------------------------------------------

def list_ports():

    ports = serial.tools.list_ports.comports()

    print("\nAvailable Serial Ports:\n")

    for port in ports:

        print(f"{port.device}  -  {port.description}")