#include <Arduino.h>
#include <Wire.h>
#include <math.h>

#include "config.h"
#include "mpu6050.h"
#include "telemetry.h"

// -------------------------------------------------
// Raw Sensor Data
// -------------------------------------------------
int16_t AccX, AccY, AccZ;
int16_t GyroX, GyroY, GyroZ;

// -------------------------------------------------
// Calibration Offsets
// -------------------------------------------------
float accX_offset = 0;
float accY_offset = 0;
float accZ_offset = 0;

float gyroX_offset = 0;
float gyroY_offset = 0;
float gyroZ_offset = 0;

// -------------------------------------------------
// Orientation
// -------------------------------------------------
float roll = 0;
float pitch = 0;

// -------------------------------------------------
// Read MPU6050 Registers
// -------------------------------------------------
void readMPU()
{
    Wire.beginTransmission(MPU_ADDRESS);
    Wire.write(0x3B);
    Wire.endTransmission(false);

    Wire.requestFrom(MPU_ADDRESS, 14, true);

    AccX = Wire.read() << 8 | Wire.read();
    AccY = Wire.read() << 8 | Wire.read();
    AccZ = Wire.read() << 8 | Wire.read();

    Wire.read();
    Wire.read();

    GyroX = Wire.read() << 8 | Wire.read();
    GyroY = Wire.read() << 8 | Wire.read();
    GyroZ = Wire.read() << 8 | Wire.read();
}

// -------------------------------------------------
// Initialize MPU6050
// -------------------------------------------------
bool mpuInit()
{
    Wire.beginTransmission(MPU_ADDRESS);

    if (Wire.endTransmission() != 0)
    {
        return false;
    }

    Wire.beginTransmission(MPU_ADDRESS);

    Wire.write(0x6B);
    Wire.write(0);

    Wire.endTransmission(true);

    delay(100);

    Serial.println("MPU6050 Initialized");

    return true;
}

// -------------------------------------------------
// Calibration
// -------------------------------------------------
void mpuCalibrate()
{
    Serial.println("Calibrating MPU6050...");
    Serial.println("Keep Sensor Still");

    for (int i = 0; i < 2000; i++)
    {
        readMPU();

        accX_offset += AccX;
        accY_offset += AccY;
        accZ_offset += AccZ;

        gyroX_offset += GyroX;
        gyroY_offset += GyroY;
        gyroZ_offset += GyroZ;

        delay(2);
    }

    accX_offset /= 2000.0;
    accY_offset /= 2000.0;
    accZ_offset = (accZ_offset / 2000.0) - 16384.0;

    gyroX_offset /= 2000.0;
    gyroY_offset /= 2000.0;
    gyroZ_offset /= 2000.0;

    Serial.println("Calibration Complete");
}

// -------------------------------------------------
// Read Orientation
// -------------------------------------------------
void mpuRead()
{
    readMPU();

    float Ax = (AccX - accX_offset) / 16384.0;
    float Ay = (AccY - accY_offset) / 16384.0;
    float Az = (AccZ - accZ_offset) / 16384.0;

    float Gx = (GyroX - gyroX_offset) / 131.0;
    float Gy = (GyroY - gyroY_offset) / 131.0;

    if (fabs(Gx) < 0.30)
        Gx = 0;

    if (fabs(Gy) < 0.30)
        Gy = 0;

    const float dt = 0.01;

    float accRoll =
        atan2(Ay, Az) * 180.0 / PI;

    float accPitch =
        atan2(-Ax, sqrt(Ay * Ay + Az * Az))
        * 180.0 / PI;

    roll =
        0.96 * (roll + Gx * dt) +
        0.04 * accRoll;

    pitch =
        0.96 * (pitch + Gy * dt) +
        0.04 * accPitch;

    telemetry.roll = roll;
    telemetry.pitch = pitch;
}