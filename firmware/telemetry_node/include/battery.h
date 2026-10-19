#pragma once

#include <Arduino.h>

struct BatteryData {
    float voltage;
};

bool batteryBegin();
bool readBattery(BatteryData &data);