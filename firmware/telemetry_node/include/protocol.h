#ifndef PROTOCOL_H
#define PROTOCOL_H

#include <Arduino.h>
#include "telemetry.h"

// ------------------------------
// Packet Constants
// ------------------------------
#define PACKET_HEADER 0xAA55
#define PACKET_FOOTER 0x55AA

#define PACKET_ID_TELEMETRY 0x01

// ------------------------------
// Status Flags
// ------------------------------
#define STATUS_OK               0x00
#define STATUS_LOW_BATTERY      0x01
#define STATUS_HIGH_TEMP        0x02
#define STATUS_BMP_ERROR        0x04
#define STATUS_MPU_ERROR        0x08
#define STATUS_SENSOR_TIMEOUT   0x10

// ------------------------------
// Telemetry Packet Structure
// ------------------------------
struct TelemetryPacket
{
    uint16_t header;

    uint8_t packetID;

    uint16_t packetCounter;

    uint32_t timestamp;

    float temperature;
    float pressure;
    float altitude;

    float roll;
    float pitch;

    float batteryVoltage;

    uint8_t batteryPercentage;

    uint8_t statusFlags;

    uint8_t checksum;

    uint16_t footer;
};

// ------------------------------
// Functions
// ------------------------------
void createPacket();

uint8_t calculateChecksum(uint8_t *data, size_t length);

void sendPacket();

#endif