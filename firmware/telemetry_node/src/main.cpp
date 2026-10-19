
#include <Arduino.h>
#include <Wire.h>


#include "imu.h"
#include "bmp280_sensor.h"
#include "oled.h"
#include "battery.h"
#include "telemetry.h"

uint32_t sequenceNumber = 0;

void setup() {
    Serial.begin(115200);
    Wire.begin(21, 22);

    imuBegin();
    bmp280Begin();
    oledBegin();
    batteryBegin();
}

void loop() {
    BatteryData bat;
    IMUData imu;
    BMP280Data environment;
    bool batteryOK = readBattery(bat);
    bool imuOK = readIMU(imu);
    bool bmpOK = readBMP280(environment);

    // if (imuOK) {
    //     Serial.printf(
    //         "Accel X: %d | Y: %d | Z: %d\n",
    //         imu.accelX, imu.accelY, imu.accelZ
    //     );
    // }

    // if (bmpOK) {
    //     Serial.printf(
    //         "Temperature: %.2f C | Pressure: %.2f hPa\n",
    //         environment.temperatureC,
    //         environment.pressurePa / 100.0f
    //     );
    // }
    // if (batteryOK) {
    //     Serial.printf("Battery Voltage: %.2f V\n",
    //     bat.voltage);
    // }

    if (imuOK && bmpOK && batteryOK) {
        oledShowSensorData(
            environment.temperatureC,
            environment.pressurePa / 100.0f,
            imu.accelX,
            imu.accelY,
            imu.accelZ,
            bat.voltage
        );

        // Collect the readings into one telemetry structure.
        TelemetryData telemetry;

        telemetry.sequenceNumber = sequenceNumber++;
        telemetry.imu = imu;
        telemetry.environment = environment;
        telemetry.battery = bat;

        // Print one complete telemetry packet.
        printTelemetryPacket(telemetry);
    } else {
        Serial.println("ERROR: Sensor reading failed");
    }

    
    delay(500);
}
