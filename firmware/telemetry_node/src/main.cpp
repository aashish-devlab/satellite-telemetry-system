#include <Arduino.h>

void setup()
{
    Serial.begin(115200);

    Serial.println();
    Serial.println("================================");
    Serial.println("Satellite Telemetry System");
    Serial.println("ESP32 Boot Successful");
    Serial.println("================================");
}

void loop()
{
    Serial.println("System Running...");
    delay(1000);
}