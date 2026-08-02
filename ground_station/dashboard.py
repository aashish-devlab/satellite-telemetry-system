"""
===========================================================
Satellite Telemetry System
Ground Station Dashboard
===========================================================

Displays real-time telemetry received from the telemetry
node.

Author : Aashish Kumar
===========================================================
"""

import customtkinter as ctk


class Dashboard:

    def __init__(self):

        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()

        self.root.title("Satellite Telemetry Ground Station")

        self.root.geometry("900x700")

        # -------------------------------------------------
        # Header
        # -------------------------------------------------

        self.title = ctk.CTkLabel(
            self.root,
            text="SATELLITE TELEMETRY GROUND STATION",
            font=("Arial", 24, "bold")
        )

        self.title.pack(pady=15)

        # -------------------------------------------------
        # Connection
        # -------------------------------------------------

        self.connection = ctk.CTkLabel(
            self.root,
            text="Connection : DISCONNECTED",
            font=("Arial", 18)
        )

        self.connection.pack()

        # -------------------------------------------------
        # Packet
        # -------------------------------------------------

        self.packet = ctk.CTkLabel(
            self.root,
            text="Packet : 0",
            font=("Arial",18)
        )

        self.packet.pack()

        # -------------------------------------------------
        # Temperature
        # -------------------------------------------------

        self.temperature = ctk.CTkLabel(
            self.root,
            text="Temperature : -- °C",
            font=("Arial",18)
        )

        self.temperature.pack()

        # -------------------------------------------------
        # Pressure
        # -------------------------------------------------

        self.pressure = ctk.CTkLabel(
            self.root,
            text="Pressure : -- hPa",
            font=("Arial",18)
        )

        self.pressure.pack()

        # -------------------------------------------------
        # Altitude
        # -------------------------------------------------

        self.altitude = ctk.CTkLabel(
            self.root,
            text="Altitude : -- m",
            font=("Arial",18)
        )

        self.altitude.pack()

        # -------------------------------------------------
        # Roll
        # -------------------------------------------------

        self.roll = ctk.CTkLabel(
            self.root,
            text="Roll : --°",
            font=("Arial",18)
        )

        self.roll.pack()

        # -------------------------------------------------
        # Pitch
        # -------------------------------------------------

        self.pitch = ctk.CTkLabel(
            self.root,
            text="Pitch : --°",
            font=("Arial",18)
        )

        self.pitch.pack()

        # -------------------------------------------------
        # Battery Voltage
        # -------------------------------------------------

        self.battery_voltage = ctk.CTkLabel(
            self.root,
            text="Battery : -- V",
            font=("Arial",18)
        )

        self.battery_voltage.pack()

        # -------------------------------------------------
        # Battery %
        # -------------------------------------------------

        self.battery_percent = ctk.CTkLabel(
            self.root,
            text="Charge : -- %",
            font=("Arial",18)
        )

        self.battery_percent.pack()

        # -------------------------------------------------
        # Faults
        # -------------------------------------------------

        self.faults = ctk.CTkTextbox(
            self.root,
            width=500,
            height=120
        )

        self.faults.pack(pady=20)

    # -----------------------------------------------------
    # Update Dashboard
    # -----------------------------------------------------

    def update(self, telemetry, faults):

        self.connection.configure(
            text="Connection : CONNECTED"
        )

        self.packet.configure(
            text=f"Packet : {telemetry['packet_counter']}"
        )

        self.temperature.configure(
            text=f"Temperature : {telemetry['temperature']:.2f} °C"
        )

        self.pressure.configure(
            text=f"Pressure : {telemetry['pressure']:.2f} hPa"
        )

        self.altitude.configure(
            text=f"Altitude : {telemetry['altitude']:.2f} m"
        )

        self.roll.configure(
            text=f"Roll : {telemetry['roll']:.2f}°"
        )

        self.pitch.configure(
            text=f"Pitch : {telemetry['pitch']:.2f}°"
        )

        self.battery_voltage.configure(
            text=f"Battery : {telemetry['battery_voltage']:.2f} V"
        )

        self.battery_percent.configure(
            text=f"Charge : {telemetry['battery_percentage']} %"
        )

        self.faults.delete("1.0","end")

        if len(faults)==0:

            self.faults.insert("end","No Faults\n")

        else:

            for fault in faults:

                self.faults.insert("end",fault+"\n")

        self.root.update()

    # -----------------------------------------------------
    # Run GUI
    # -----------------------------------------------------

    def run(self):

        self.root.mainloop()