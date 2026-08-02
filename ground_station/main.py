"""
===========================================================
Satellite Telemetry System
Ground Station
===========================================================

Main application for the Ground Station.

Responsibilities:
    - Connect to ESP32
    - Receive telemetry packets
    - Parse packets
    - Log telemetry
    - Detect faults
    - Display telemetry

Author : Aashish Kumar
===========================================================
"""

from serial_manager import SerialManager
from parser import PacketParser
from logger import DataLogger
from faults import FaultDetector

from protocol import PACKET_SIZE


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():

    # ----------------------------------------------
    # Create Modules
    # ----------------------------------------------

    serial = SerialManager()

    parser = PacketParser()

    logger = DataLogger()

    faults = FaultDetector()

    # ----------------------------------------------
    # Connect
    # ----------------------------------------------

    if not serial.connect():

        print("Unable to connect to ESP32")

        return

    print("\nGround Station Started\n")

    # ----------------------------------------------
    # Main Loop
    # ----------------------------------------------

    while True:

        # Wait until a complete packet is available
        if serial.available() >= PACKET_SIZE:

            packet = serial.read(PACKET_SIZE)

            telemetry = parser.parse(packet)

            if telemetry is None:

                continue

            # -----------------------------
            # Console Output
            # -----------------------------

            print("\n==============================")

            print("Packet :", telemetry["packet_counter"])

            print("Time   :", telemetry["timestamp"], "ms")

            print("------------------------------")

            print("Temperature :", telemetry["temperature"], "°C")

            print("Pressure    :", telemetry["pressure"], "hPa")

            print("Altitude    :", telemetry["altitude"], "m")

            print("------------------------------")

            print("Roll        :", telemetry["roll"])

            print("Pitch       :", telemetry["pitch"])

            print("------------------------------")

            print("Battery     :", telemetry["battery_voltage"], "V")

            print("Charge      :", telemetry["battery_percentage"], "%")

            print("==============================")

            # -----------------------------
            # Save CSV
            # -----------------------------

            logger.log(telemetry)

            # -----------------------------
            # Fault Detection
            # -----------------------------

            detected_faults = faults.check(telemetry)

            if detected_faults:

                print("\nFaults:")

                for fault in detected_faults:

                    print(" -", fault)


# --------------------------------------------------
# Entry Point
# --------------------------------------------------

if __name__ == "__main__":

    try:

        main()

    except KeyboardInterrupt:

        print("\nGround Station Closed")