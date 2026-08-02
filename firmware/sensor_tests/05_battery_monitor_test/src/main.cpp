#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

#define ADC_PIN 34

// Voltage divider (keep actual measured values if possible)
const float R1 = 100000.0;
const float R2 = 100000.0;

// ADC constants
const float adcMax = 4095.0;
const float ADC_REFERENCE = 3.30;

// FINAL calibration factor (based on your data ~1.09–1.10)
const float calibrationFactor = 1.156;

// -------- MEDIAN FILTER --------
int getMedian(int *arr, int size) {
  for (int i = 0; i < size - 1; i++) {
    for (int j = i + 1; j < size; j++) {
      if (arr[j] < arr[i]) {
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
      }
    }
  }
  return arr[size / 2];
}

// -------- STABLE ADC READ --------
int readADCStable() {
  const int samples = 15;
  int values[samples];

  for (int i = 0; i < samples; i++) {
    values[i] = analogRead(ADC_PIN);
    delay(3);
  }

  return getMedian(values, samples);
}

// -------- BATTERY PERCENT (BETTER APPROX) --------
int getBatteryPercentage(float v) {
  if (v >= 4.2) return 100;
  if (v <= 3.0) return 0;

  // Non-linear Li-ion approximation
  if (v > 3.7)
    return 50 + (v - 3.7) * 100;
  else
    return (v - 3.0) * 50 / (3.7 - 3.0);
}

void setup() {
  Serial.begin(115200);

  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println("OLED failed");
    while (true);
  }

  display.clearDisplay();
  display.setTextColor(WHITE);

  analogReadResolution(12);
  analogSetPinAttenuation(ADC_PIN, ADC_11db);
}

void loop() {

  int adcValue = readADCStable();

  const float dividerRatio = (R1 + R2) / R2;

  float batteryVoltage =
      ((float)adcValue / adcMax) *
      ADC_REFERENCE *
      dividerRatio *
      calibrationFactor;

  int percentage = getBatteryPercentage(batteryVoltage);

  // -------- OLED DISPLAY --------
  display.clearDisplay();

  display.setTextSize(1);
  display.setCursor(0, 0);
  display.print("Battery Monitor");

  display.setTextSize(2);
  display.setCursor(0, 18);
  display.print(batteryVoltage, 2);
  display.print(" V");

  display.setTextSize(1);
  display.setCursor(0, 45);
  display.print("Charge: ");
  display.print(percentage);
  display.print("%");

  display.setCursor(0, 55);

  if (batteryVoltage > 4.0) {
    display.print("FULL");
  } 
  else if (batteryVoltage > 3.6) {
    display.print("NORMAL");
  } 
  else if (batteryVoltage > 3.3) {
    display.print("LOW");
  } 
  else {
    display.print("CRITICAL");
  }

  display.display();

  // Debug output
  Serial.print("ADC: ");
  Serial.print(adcValue);

  Serial.print(" | Battery: ");
  Serial.print(batteryVoltage, 2);

  Serial.print(" V | ");
  Serial.print(percentage);

  Serial.println("%");

  delay(1000);
}