#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_BMP280.h>

#include "config.h"
#include "bmp280.h"
#include "telemetry.h"

Adafruit_BMP280 bmp;

// --------------------------------------------------
// Initialize BMP280
// --------------------------------------------------
bool bmpInit()
{
    if (!bmp.begin(BMP_ADDRESS))
    {
        return false;
    }

    // Recommended settings
    bmp.setSampling(
        Adafruit_BMP280::MODE_NORMAL,
        Adafruit_BMP280::SAMPLING_X2,
        Adafruit_BMP280::SAMPLING_X16,
        Adafruit_BMP280::FILTER_X16,
        Adafruit_BMP280::STANDBY_MS_500
    );

    Serial.println("BMP280 Initialized");

    return true;
}

// --------------------------------------------------
// Read BMP280 Sensor
// --------------------------------------------------
void bmpRead()
{
    telemetry.temperature = bmp.readTemperature();

    telemetry.pressure = bmp.readPressure() / 100.0F;

    telemetry.altitude =
        bmp.readAltitude(SEA_LEVEL_PRESSURE);
}