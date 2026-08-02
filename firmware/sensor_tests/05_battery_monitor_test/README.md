# 06 - Battery Monitor Test

## Hardware Used

| Component | Quantity |
|-----------|---------:|
| ESP32 DevKit V1 | 1 |
| 18650 Li-ion Battery | 1 |
| TP4056 Charging Module (with Protection) | 1 |
| XL6009 DC-DC Boost Converter | 1 |
| SSD1306 OLED Display (128×64, I²C) | 1 |
| 100kΩ Resistor | 2 |
| Breadboard | 1 |
| Jumper Wires | As Required |

---

# Hardware Connections

## 1. 18650 Battery → TP4056

| 18650 Battery | TP4056 |
|---------------|--------|
| Positive (+) | B+ |
| Negative (-) | B- |

---

## 2. TP4056 → XL6009

| TP4056 | XL6009 |
|---------|--------|
| OUT+ | IN+ |
| OUT- | IN- |

> **Note:** Use the **OUT+** and **OUT-** terminals of the TP4056, not the battery terminals (B+ / B-), to power the circuit through the protection module.

---

## 3. XL6009 → ESP32

> Adjust the XL6009 output to **5.0 V** before connecting it to the ESP32.

| XL6009 | ESP32 |
|---------|-------|
| OUT+ | VIN (5V) |
| OUT- | GND |

---

## 4. Battery Voltage Divider

Use two **100kΩ** resistors to safely measure the battery voltage.

```
TP4056 OUT+
      |
    100kΩ
      |
      +-----------> GPIO34 (ADC)
      |
    100kΩ
      |
TP4056 OUT-
```

| Connection | ESP32 |
|------------|-------|
| Voltage Divider Midpoint | GPIO34 |
| Common Ground | GND |

---

## 5. OLED Display

| OLED | ESP32 |
|------|-------|
| VCC | 3.3V |
| GND | GND |
| SDA | GPIO21 |
| SCL | GPIO22 |

---

# Complete Power Flow

```
USB
 │
 ▼
TP4056
 │
 ├── B+ / B- → 18650 Battery
 │
 ├── OUT+ ───────────────► XL6009 IN+
 ├── OUT- ───────────────► XL6009 IN-
 │
 ├── OUT+ ──100kΩ──┐
 │                 ├────► GPIO34 (Battery Voltage Measurement)
 └── OUT- ─100kΩ───┘

XL6009
 │
 ├── OUT+ ───────────────► ESP32 VIN
 └── OUT- ───────────────► ESP32 GND

ESP32
 │
 ├── GPIO21 ─────────────► OLED SDA
 ├── GPIO22 ─────────────► OLED SCL
 ├── 3.3V ───────────────► OLED VCC
 └── GND ────────────────► OLED GND
```

---

## Notes

- Measure the battery voltage **before the XL6009 boost converter** using the voltage divider.
- Do **not** connect the battery directly to GPIO34.
- Verify the XL6009 output with a multimeter and adjust it to **5.0 V** before connecting it to the ESP32.
- Ensure all modules share a common ground.