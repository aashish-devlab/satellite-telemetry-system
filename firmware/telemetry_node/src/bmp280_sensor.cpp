
#include "bmp280_sensor.h"
#include <Wire.h>
#include <Adafruit_BMP280.h>

namespace {
    Adafruit_BMP280 bmp;
}

bool bmp280Begin() {
    if (!bmp.begin(0x76)) {
        Serial.println("BMP Error");
        return false;
    }

    Serial.println("BMP Working");
    return true;
}

bool readBMP280(BMP280Data &data) {
    data.temperatureC = bmp.readTemperature();
    data.pressurePa = bmp.readPressure();

    return true;
}
