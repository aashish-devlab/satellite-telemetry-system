#pragma once

#include <Arduino.h>

bool oledBegin();

void oledShowSensorData(
    float temperatureC,
    float pressureHpa,
    int16_t accelX,
    int16_t accelY,
    int16_t accelZ,
    float batteryVoltage
);