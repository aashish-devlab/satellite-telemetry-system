#ifndef BATTERY_H
#define BATTERY_H

void batteryInit();

void batteryRead();

float getBatteryVoltage();

int getBatteryPercentage(float voltage);

#endif