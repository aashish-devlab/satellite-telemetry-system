#include "imu.h" //imports the interface
#include <Wire.h> //provides Arduino's I²C communication functions
#include <Arduino.h> //provides Arduino's core functions

namespace { //creates an anonymous namespace
    //value is intended to be known at compile time
    constexpr uint8_t MPU_ADDR = 0x68; // I2C address of the MPU-6050 IMU

    // The 'f' at the end of each number indicates a floating-point literal
    constexpr float GYRO_X_BIAS = -418.81f;
    constexpr float GYRO_Y_BIAS = 39.71f;
    constexpr float GYRO_Z_BIAS = -111.14f;

    int16_t readInt16() {
        uint8_t highByte = Wire.read(); // read high 8 bits
        uint8_t lowByte = Wire.read(); // read low 8 bits

        return (int16_t)(  //combine high and low bytes into a signed 16-bit integer
            ((uint16_t)highByte << 8) | lowByte ////left shift with bitwise OR operation
        );
    }

    /// Declares a function that doesn't return a value.
    //Reading a register
    void readRegister(uint8_t reg, const char* name) { 
        Wire.beginTransmission(MPU_ADDR); //Begins an I²C transmission to the sensor's address
        Wire.write(reg); //Selects the register address
 
        if (Wire.endTransmission(false) != 0) { //requesting that the I²C bus remain active for the subsequent read
            Serial.printf("%s: register access failed\n", name);
            return;
        }

        if (Wire.requestFrom(MPU_ADDR, (uint8_t)1) == 1) { //Requests one byte from the sensor
            uint8_t value = Wire.read(); //Retrieves the received byte
            Serial.printf(
                "%s (0x%02X): 0x%02X\n",
                name, reg, value
            );
        } else {
            Serial.printf("%s: read failed\n", name);
        }
    }
}

//Initializing the IMU
bool imuBegin() {
    Wire.beginTransmission(MPU_ADDR);
    Wire.write(0x6B); //power management register
    Wire.write(0x00); // Wake up the MPU
 
    if (Wire.endTransmission() != 0) {
        Serial.println("MPU communication error");
        return false;
    }

    Serial.println("MPU wake-up command sent");

    Wire.beginTransmission(MPU_ADDR);
    Wire.write(0x75); // who am i register

    if (Wire.endTransmission(false) != 0 || //Keep the bus active for the read
        Wire.requestFrom(MPU_ADDR, (uint8_t)1) != 1) { // Request one byte from the MPU
        Serial.println("Failed to read MPU identity");
        return false;
    }

    uint8_t identity = Wire.read();

    Serial.printf("MPU identity: 0x%02X\n", identity);

    Serial.println("Reading registers...");
    readRegister(0x1B, "GYRO_CONFIG");
    readRegister(0x1C, "ACCEL_CONFIG");
    readRegister(0x1A, "CONFIG");
    readRegister(0x19, "SMPLRT_DIV");

    return true;
}

//Reading all six axes
bool readIMU(IMUData &data) {
    Wire.beginTransmission(MPU_ADDR);
    Wire.write(0x3B);

    if (Wire.endTransmission(false) != 0) {
        return false;
    }

    if (Wire.requestFrom(MPU_ADDR, (uint8_t)14) != 14) {
        return false;
    }

    data.accelX = readInt16();
    data.accelY = readInt16();
    data.accelZ = readInt16();

    data.temperatureRaw = readInt16();

    int16_t rawGyroX = readInt16();
    int16_t rawGyroY = readInt16();
    int16_t rawGyroZ = readInt16();

    // Keep the established raw-count bias correction.
    // Rounded back to integers to preserve raw-count units.
    data.gyroX = (int16_t)(rawGyroX - GYRO_X_BIAS);
    data.gyroY = (int16_t)(rawGyroY - GYRO_Y_BIAS);
    data.gyroZ = (int16_t)(rawGyroZ - GYRO_Z_BIAS);

    return true;
}