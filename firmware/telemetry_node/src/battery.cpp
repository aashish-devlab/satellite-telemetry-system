#include <Arduino.h>

#include "config.h"
#include "battery.h"
#include "telemetry.h"

// --------------------------------------------------
// Median Filter
// --------------------------------------------------
int getMedian(int *arr, int size)
{
    for (int i = 0; i < size - 1; i++)
    {
        for (int j = i + 1; j < size; j++)
        {
            if (arr[j] < arr[i])
            {
                int temp = arr[i];
                arr[i] = arr[j];
                arr[j] = temp;
            }
        }
    }

    return arr[size / 2];
}

// --------------------------------------------------
// Stable ADC Read
// --------------------------------------------------
int readADCStable()
{
    const int samples = 15;

    int values[samples];

    for (int i = 0; i < samples; i++)
    {
        values[i] = analogRead(BATTERY_PIN);
        delay(3);
    }

    return getMedian(values, samples);
}

// --------------------------------------------------
// Initialization
// --------------------------------------------------
void batteryInit()
{
    analogReadResolution(12);

    analogSetPinAttenuation(BATTERY_PIN, ADC_11db);

    Serial.println("Battery Monitor Initialized");
}

// --------------------------------------------------
// Voltage
// --------------------------------------------------
float getBatteryVoltage()
{
    int adcValue = readADCStable();

    const float dividerRatio = (R1 + R2) / R2;

    float batteryVoltage =
        ((float)adcValue / ADC_MAX) *
        ADC_REF *
        dividerRatio *
        CALIBRATION_FACTOR;

    return batteryVoltage;
}

// --------------------------------------------------
// Battery Percentage
// --------------------------------------------------
int getBatteryPercentage(float v)
{
    if (v >= 4.2)
        return 100;

    if (v <= 3.0)
        return 0;

    if (v > 3.7)
        return 50 + (v - 3.7) * 100;

    return (v - 3.0) * 50 / (3.7 - 3.0);
}

// --------------------------------------------------
// Update Telemetry Structure
// --------------------------------------------------
void batteryRead()
{
    telemetry.batteryVoltage = getBatteryVoltage();

    telemetry.batteryPercentage =
        getBatteryPercentage(
            telemetry.batteryVoltage);
}