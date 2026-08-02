#ifndef TELEMETRY_H
#define TELEMETRY_H

struct TelemetryData
{
    // BMP280
    float temperature;
    float pressure;
    float altitude;

    // MPU6050
    float roll;
    float pitch;

    // Battery
    float batteryVoltage;
    int batteryPercentage;
};

// Global telemetry object
extern TelemetryData telemetry;

// Functions
void printTelemetry();

#endif