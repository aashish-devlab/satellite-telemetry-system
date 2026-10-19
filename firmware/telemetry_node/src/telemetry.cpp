
#include "telemetry.h"

void printTelemetryPacket(const TelemetryData &data) {
    char payload[160];

    int length = snprintf( //builds one complete text payload first, making it easier to calculate a checksum over precisely the bytes that will be transmitted
        payload,
        sizeof(payload),
        "AKTD,%lu,%.2f,%.2f,%d,%d,%d,%d,%d,%d,%.2f",
        (unsigned long)data.sequenceNumber,
        data.environment.temperatureC,
        data.environment.pressurePa / 100.0f,
        data.imu.accelX,
        data.imu.accelY,
        data.imu.accelZ,
        data.imu.gyroX,
        data.imu.gyroY,
        data.imu.gyroZ,
        data.battery.voltage
    );

    //Safety check to ensure that the snprintf call did not exceed the buffer size. If it did, we simply return without printing anything.
    if (length < 0 || length >= (int)sizeof(payload)) {
        return;
    }

    uint8_t checksum = 0;

    for (int i = 0; i < length; i++) {
        checksum ^= (uint8_t)payload[i]; //XORs each character's byte into the checksum
    }

    Serial.printf("%s,%02X\n", payload, checksum); //Print the checksum in uppercase hexadecimal, at least two digits wide
}
