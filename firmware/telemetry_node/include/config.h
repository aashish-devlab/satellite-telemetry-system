#ifndef CONFIG_H
#define CONFIG_H

// ================================
// OLED Configuration
// ================================
#define SCREEN_WIDTH   128
#define SCREEN_HEIGHT  64
#define OLED_ADDRESS   0x3C

// ================================
// I2C Pins
// ================================
#define SDA_PIN        21
#define SCL_PIN        22

// ==============================
// Battery Monitor
// ==============================

#define BATTERY_PIN 34

#define ADC_MAX 4095.0
#define ADC_REF 3.30

#define R1 100000.0
#define R2 100000.0

#define CALIBRATION_FACTOR 1.156

// ================================
// BMP280
// ================================
#define BMP_ADDRESS    0x76
#define SEA_LEVEL_PRESSURE 1013.25

// ================================
// MPU6050
// ================================
#define MPU_ADDRESS    0x68

// ================================
// Loop Timing
// ================================
#define LOOP_DELAY     100

#endif