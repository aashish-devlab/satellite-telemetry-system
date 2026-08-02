#include <Arduino.h>
#include <string.h>

#include "protocol.h"
#include "telemetry.h"

// --------------------------------------------------
// Global Packet
// --------------------------------------------------
TelemetryPacket packet;

// Packet Counter
static uint16_t packetCounter = 0;

// --------------------------------------------------
// XOR Checksum
// --------------------------------------------------
uint8_t calculateChecksum(uint8_t *data, size_t length)
{
    uint8_t checksum = 0;

    for (size_t i = 0; i < length; i++)
    {
        checksum ^= data[i];
    }

    return checksum;
}

// --------------------------------------------------
// Create Telemetry Packet
// --------------------------------------------------
void createPacket()
{
    packet.header = PACKET_HEADER;

    packet.packetID = PACKET_ID_TELEMETRY;

    packet.packetCounter = packetCounter++;

    packet.timestamp = millis();

    // Copy Telemetry Data
    packet.temperature = telemetry.temperature;
    packet.pressure = telemetry.pressure;
    packet.altitude = telemetry.altitude;

    packet.roll = telemetry.roll;
    packet.pitch = telemetry.pitch;

    packet.batteryVoltage = telemetry.batteryVoltage;
    packet.batteryPercentage = telemetry.batteryPercentage;

    // Status Flags
    packet.statusFlags = STATUS_OK;

    if (telemetry.batteryPercentage < 20)
        packet.statusFlags |= STATUS_LOW_BATTERY;

    if (telemetry.temperature > 70)
        packet.statusFlags |= STATUS_HIGH_TEMP;

    // Footer
    packet.footer = PACKET_FOOTER;

    // Calculate checksum
    packet.checksum = calculateChecksum(
        (uint8_t*)&packet,
        sizeof(TelemetryPacket) - 3
    );
}

// --------------------------------------------------
// Send Packet
// --------------------------------------------------
void sendPacket()
{
    Serial.write(
        (uint8_t*)&packet,
        sizeof(TelemetryPacket)
    );
}