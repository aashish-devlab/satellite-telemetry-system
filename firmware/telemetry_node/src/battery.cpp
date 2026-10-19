#include "battery.h"

namespace {
    constexpr uint8_t BATTERY_PIN = 34;
    constexpr float correctionFActor = 0.03; // Adjust this value based on calibration
    constexpr float R1 = 935000.0f;
    constexpr float R2 = 951000.0f;
    constexpr float DIVIDER_RATIO = (R1 + R2) / R2;
}

bool batteryBegin() {
    pinMode(BATTERY_PIN, INPUT);
    analogReadResolution(12);
    analogSetPinAttenuation(
        BATTERY_PIN,
        ADC_11db
    );

    return true;
}

bool readBattery(BatteryData &data) {
    constexpr int SAMPLE_COUNT = 16;
    uint32_t total = 0;

    for (int i = 0; i < SAMPLE_COUNT; i++) {
        total += analogReadMilliVolts(BATTERY_PIN);
        delay(2);
    }

    float adcVoltage =
        (total / static_cast<float>(SAMPLE_COUNT)) / 1000.0f;

    data.voltage = (adcVoltage * DIVIDER_RATIO)-correctionFActor;

    return true;
}