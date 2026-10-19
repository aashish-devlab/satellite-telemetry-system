
#pragma once //tells the compiler to include this header only once per translation unit

#include <Arduino.h> //makes Arduino types and functions available

struct BMP280Data {
    float temperatureC;
    float pressurePa;
};

bool bmp280Begin();
bool readBMP280(BMP280Data &data);
