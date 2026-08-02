#include <Arduino.h>

#include "telemetry.h"

// --------------------------------------------------
// Global Telemetry Object
// --------------------------------------------------
TelemetryData telemetry;

// --------------------------------------------------
// Print Telemetry Packet
// --------------------------------------------------
void printTelemetry()
{
    Serial.println();
    Serial.println("========================================");
    Serial.println("      SATELLITE TELEMETRY DATA");
    Serial.println("========================================");

    Serial.print("Temperature       : ");
    Serial.print(telemetry.temperature, 2);
    Serial.println(" C");

    Serial.print("Pressure          : ");
    Serial.print(telemetry.pressure, 2);
    Serial.println(" hPa");

    Serial.print("Altitude          : ");
    Serial.print(telemetry.altitude, 2);
    Serial.println(" m");

    Serial.println("----------------------------------------");

    Serial.print("Roll              : ");
    Serial.print(telemetry.roll, 2);
    Serial.println(" deg");

    Serial.print("Pitch             : ");
    Serial.print(telemetry.pitch, 2);
    Serial.println(" deg");

    Serial.println("----------------------------------------");

    Serial.print("Battery Voltage   : ");
    Serial.print(telemetry.batteryVoltage, 2);
    Serial.println(" V");

    Serial.print("Battery Level     : ");
    Serial.print(telemetry.batteryPercentage);
    Serial.println(" %");

    Serial.println("========================================");
    Serial.println();
}