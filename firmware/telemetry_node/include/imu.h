
#pragma once //tells the compiler to include this header only once per translation unit

#include <Arduino.h> //makes Arduino types and functions available

struct IMUData {
    int16_t accelX;
    int16_t accelY;
    int16_t accelZ;

    int16_t temperatureRaw;

    int16_t gyroX;
    int16_t gyroY;
    int16_t gyroZ;
};

bool imuBegin();
bool readIMU(IMUData &data);
