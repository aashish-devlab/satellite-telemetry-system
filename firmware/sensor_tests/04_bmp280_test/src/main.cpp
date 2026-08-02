#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_BMP280.h>

Adafruit_BMP280 bmp;

void setup()
{
    Serial.begin(115200);

    Wire.begin(21, 22);

    Serial.println("Initializing BMP280...");

    if (!bmp.begin(0x76))
    {
        Serial.println("BMP280 NOT FOUND!");

        while (1);
    }

    Serial.println("BMP280 Initialized Successfully");
    Serial.println();
}

void loop()
{
    float temperature = bmp.readTemperature();
    float pressure = bmp.readPressure() / 100.0;   // hPa
    float altitude = bmp.readAltitude(1013.25);    // Sea-level pressure

    Serial.print("Temperature : ");
    Serial.print(temperature);
    Serial.println(" °C");

    Serial.print("Pressure    : ");
    Serial.print(pressure);
    Serial.println(" hPa");

    Serial.print("Altitude    : ");
    Serial.print(altitude);
    Serial.println(" m");

    Serial.println("-----------------------------");

    delay(1000);
}