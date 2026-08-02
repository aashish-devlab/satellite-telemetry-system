#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#include "config.h"
#include "oled.h"
#include "telemetry.h"

Adafruit_SSD1306 display(
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    &Wire,
    -1
);

// --------------------------------------------------
// OLED Initialization
// --------------------------------------------------
void oledInit()
{
    if (!display.begin(SSD1306_SWITCHCAPVCC, OLED_ADDRESS))
    {
        Serial.println("OLED Initialization Failed!");

        while (true);
    }

    display.clearDisplay();
    display.setTextColor(SSD1306_WHITE);

    display.setTextSize(2);
    display.setCursor(0, 0);
    display.println("Satellite");

    display.setTextSize(1);
    display.println("Telemetry System");

    display.display();

    delay(1500);

    display.clearDisplay();
    display.display();

    Serial.println("OLED Initialized");
}

// --------------------------------------------------
// OLED Dashboard
// --------------------------------------------------
void oledUpdate()
{
    display.clearDisplay();

    // ---------- Title ----------
    display.setTextSize(1);
    display.setCursor(0, 0);
    display.println("Satellite Telemetry");

    // ---------- Temperature ----------
    display.setCursor(0, 12);
    display.print("T:");
    display.print(telemetry.temperature, 1);
    display.print("C");

    // ---------- Pressure ----------
    display.setCursor(70, 12);
    display.print("P:");
    display.print(telemetry.pressure, 0);

    // ---------- Altitude ----------
    display.setCursor(0, 24);
    display.print("Alt:");
    display.print(telemetry.altitude, 0);
    display.print("m");

    // ---------- Roll ----------
    display.setCursor(0, 36);
    display.print("R:");
    display.print(telemetry.roll, 1);

    // ---------- Pitch ----------
    display.setCursor(64, 36);
    display.print("P:");
    display.print(telemetry.pitch, 1);

    // ---------- Battery ----------
    display.setCursor(0, 52);

    display.print("Bat:");

    display.print(telemetry.batteryVoltage, 2);

    display.print("V ");

    display.print(telemetry.batteryPercentage);

    display.print("%");

    display.display();
}