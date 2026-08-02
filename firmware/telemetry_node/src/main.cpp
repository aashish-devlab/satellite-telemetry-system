#include <Arduino.h>
#include <Wire.h>

#include "config.h"
#include "oled.h"
#include "bmp280.h"
#include "mpu6050.h"
#include "battery.h"
#include "telemetry.h"

void setup()
{
    Serial.begin(115200);

    // Initialize I2C
    Wire.begin(SDA_PIN, SCL_PIN);

    Serial.println();
    Serial.println("======================================");
    Serial.println(" Satellite Telemetry System");
    Serial.println(" Initializing...");
    Serial.println("======================================");

    // Initialize OLED
    oledInit();

    // Initialize BMP280
    if (!bmpInit())
    {
        Serial.println("BMP280 Initialization Failed!");
        while (true);
    }

    // Initialize MPU6050
    if (!mpuInit())
    {
        Serial.println("MPU6050 Initialization Failed!");
        while (true);
    }

    // Calibrate MPU6050
    mpuCalibrate();

    // Initialize Battery Monitor
    batteryInit();

    Serial.println("Initialization Complete");
    Serial.println();
}

void loop()
{
    // Read all sensors
    bmpRead();
    mpuRead();
    batteryRead();

    // Print telemetry packet
    printTelemetry();

    // Update OLED display
    oledUpdate();

    delay(LOOP_DELAY);
}