#include <Arduino.h>
#include <Wire.h>

const int MPU_addr = 0x68;

// Raw data
int16_t AccX, AccY, AccZ;
int16_t GyroX, GyroY, GyroZ;

// Offsets
float accX_offset = 0, accY_offset = 0, accZ_offset = 0;
float gyroX_offset = 0, gyroY_offset = 0, gyroZ_offset = 0;

// --- Read MPU6050 ---
void readMPU() {
  Wire.beginTransmission(MPU_addr);
  Wire.write(0x3B);
  Wire.endTransmission(false);
  Wire.requestFrom(MPU_addr, 14, true);

  AccX = Wire.read() << 8 | Wire.read();
  AccY = Wire.read() << 8 | Wire.read();
  AccZ = Wire.read() << 8 | Wire.read();

  Wire.read(); Wire.read(); // skip temp

  GyroX = Wire.read() << 8 | Wire.read();
  GyroY = Wire.read() << 8 | Wire.read();
  GyroZ = Wire.read() << 8 | Wire.read();
}

void setup() {
  Serial.begin(115200);
  Wire.begin(21, 22);

  // Wake MPU6050
  Wire.beginTransmission(MPU_addr);
  Wire.write(0x6B);
  Wire.write(0);
  Wire.endTransmission(true);

  Serial.println("Calibrating... KEEP SENSOR STILL");

  // --- Calibration ---
  for (int i = 0; i < 2000; i++) {
    readMPU();

    accX_offset += AccX;
    accY_offset += AccY;
    accZ_offset += AccZ;

    gyroX_offset += GyroX;
    gyroY_offset += GyroY;
    gyroZ_offset += GyroZ;

    delay(2);
  }

  accX_offset /= 2000;
  accY_offset /= 2000;
  accZ_offset = (accZ_offset / 2000) - 16384; // remove gravity

  gyroX_offset /= 2000;
  gyroY_offset /= 2000;
  gyroZ_offset /= 2000;

  Serial.println("Calibration Done\n");
}


void loop() {
  readMPU();

  // Apply calibration + convert units
  float Ax = (AccX - accX_offset) / 16384.0;
  float Ay = (AccY - accY_offset) / 16384.0;
  float Az = (AccZ - accZ_offset) / 16384.0;

  float Gx = (GyroX - gyroX_offset) / 131.0;
  float Gy = (GyroY - gyroY_offset) / 131.0;
  float Gz = (GyroZ - gyroZ_offset) / 131.0;

  // Print clean output
  Serial.print("ACC (g): ");
  Serial.print(Ax, 3); Serial.print(", ");
  Serial.print(Ay, 3); Serial.print(", ");
  Serial.print(Az, 3);

  Serial.print(" || GYRO (deg/s): ");
  Serial.print(Gx, 2); Serial.print(", ");
  Serial.print(Gy, 2); Serial.print(", ");
  Serial.println(Gz, 2);

  delay(200);
}

