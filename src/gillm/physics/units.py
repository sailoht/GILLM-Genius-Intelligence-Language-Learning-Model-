from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class QuantityUnit:
    """Represents physical dimensions (mass, length, time) for unit checking."""
    mass_power: int = 0      # kg
    length_power: int = 0    # m
    time_power: int = 0      # s

    def multiply(self, other: 'QuantityUnit') -> 'QuantityUnit':
        return QuantityUnit(
            mass_power=self.mass_power + other.mass_power,
            length_power=self.length_power + other.length_power,
            time_power=self.time_power + other.time_power
        )

    def divide(self, other: 'QuantityUnit') -> 'QuantityUnit':
        return QuantityUnit(
            mass_power=self.mass_power - other.mass_power,
            length_power=self.length_power - other.length_power,
            time_power=self.time_power - other.time_power
        )

    def is_dimensionally_equal(self, other: 'QuantityUnit') -> bool:
        return (
            self.mass_power == other.mass_power and
            self.length_power == other.length_power and
            self.time_power == other.time_power
        )

# Preset standard physical units
UNIT_MASS = QuantityUnit(mass_power=1, length_power=0, time_power=0)        # kg
UNIT_LENGTH = QuantityUnit(mass_power=0, length_power=1, time_power=0)      # m
UNIT_TIME = QuantityUnit(mass_power=0, length_power=0, time_power=1)        # s
UNIT_VELOCITY = QuantityUnit(mass_power=0, length_power=1, time_power=-1)   # m/s
UNIT_ACCELERATION = QuantityUnit(mass_power=0, length_power=1, time_power=-2)# m/s^2
UNIT_FORCE = QuantityUnit(mass_power=1, length_power=1, time_power=-2)       # N (kg*m/s^2)
