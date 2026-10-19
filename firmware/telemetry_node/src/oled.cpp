#include "oled.h"
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

namespace {
    constexpr int SCREEN_WIDTH = 128;
    constexpr int SCREEN_HEIGHT = 64;
    constexpr int OLED_RESET = -1;
    constexpr uint8_t OLED_ADDRESS = 0x3C;

    Adafruit_SSD1306 display(
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
        &Wire,
        OLED_RESET
    );
}

bool oledBegin() {
    if (!display.begin(
            SSD1306_SWITCHCAPVCC,
            OLED_ADDRESS
        )) {
        Serial.println("OLED initialization failed");
        return false;
    }

    display.clearDisplay();
    display.setTextSize(1);
    display.setTextColor(SSD1306_WHITE);

    Serial.println("OLED initialized successfully");
    return true;
}

void oledShowSensorData(
    float temperatureC,
    float pressureHpa,
    int16_t accelX,
    int16_t accelY,
    int16_t accelZ,
    float batteryVoltage
) {
    display.clearDisplay();
    display.setCursor(0, 0);

    display.println("Satellite Telemetry");
    display.println("-------------------");

    display.print("Temp: ");
    display.print(temperatureC, 1);
    display.println(" C");

    display.print("Press: ");
    display.print(pressureHpa, 1);
    display.println(" hPa");

    display.print("AX: ");
    display.print(accelX);
    display.print(" AY: ");
    display.println(accelY);

    display.print("AZ: ");
    display.println(accelZ);

    display.print("Battery: ");
    display.print(batteryVoltage, 2);
    display.println(" V");

    display.display();
}