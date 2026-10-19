#pragma once

#include <Arduino.h>
#include "imu.h"
#include "bmp280_sensor.h"
#include "battery.h"

struct TelemetryData {
    uint32_t sequenceNumber; //counter that will increase for each telemetry packet

    IMUData imu;
    BMP280Data environment;
    BatteryData battery;
};

void printTelemetryPacket(const TelemetryData &data); //passes your collected sensor data without copying the entire structure