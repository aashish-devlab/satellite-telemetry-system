from dataclasses import dataclass


@dataclass
class TelemetryPacket:
    sequence: int
    temperature_c: float
    pressure_hpa: float
    accel_x: int
    accel_y: int
    accel_z: int
    gyro_x: int
    gyro_y: int
    gyro_z: int
    battery_v: float


def parse_packet(line: str) -> TelemetryPacket:
    """Validate and parse one AKTD telemetry packet."""

    line = line.strip()
    fields = line.split(",")

    if len(fields) != 12:
        raise ValueError("Incorrect number of fields")

    if fields[0] != "AKTD":
        raise ValueError("Invalid packet prefix")

    payload = ",".join(fields[:-1])

    try:
        received_checksum = int(fields[-1], 16)
    except ValueError:
        raise ValueError("Invalid checksum format") from None

    if not 0 <= received_checksum <= 0xFF:
        raise ValueError("Checksum must be one byte")

    calculated_checksum = 0
    for character in payload:
        calculated_checksum ^= ord(character)

    if calculated_checksum != received_checksum:
        raise ValueError("Checksum mismatch")

    try:
        return TelemetryPacket(
            sequence=int(fields[1]),
            temperature_c=float(fields[2]),
            pressure_hpa=float(fields[3]),
            accel_x=int(fields[4]),
            accel_y=int(fields[5]),
            accel_z=int(fields[6]),
            gyro_x=int(fields[7]),
            gyro_y=int(fields[8]),
            gyro_z=int(fields[9]),
            battery_v=float(fields[10]),
        )
    except ValueError:
        raise ValueError("Invalid numeric telemetry field") from None
