from dataclasses import dataclass

@dataclass
class QuantityUnit:
    mass_pow: int = 0
    length_pow: int = 0
    time_pow: int = 0

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, QuantityUnit):
            return False
        return (self.mass_pow == other.mass_pow and
                self.length_pow == other.length_pow and
                self.time_pow == other.time_pow)

    def __truediv__(self, other: 'QuantityUnit') -> 'QuantityUnit':
        return QuantityUnit(
            mass_pow=self.mass_pow - other.mass_pow,
            length_pow=self.length_pow - other.length_pow,
            time_pow=self.time_pow - other.time_pow
        )

    def __mul__(self, other: 'QuantityUnit') -> 'QuantityUnit':
        return QuantityUnit(
            mass_pow=self.mass_pow + other.mass_pow,
            length_pow=self.length_pow + other.length_pow,
            time_pow=self.time_pow + other.time_pow
        )

    def __str__(self) -> str:
        if self.mass_pow == 0 and self.length_pow == 1 and self.time_pow == -2:
            return "m/s^2"
        if self.mass_pow == 1 and self.length_pow == 1 and self.time_pow == -2:
            return "N"
        if self.mass_pow == 1 and self.length_pow == 0 and self.time_pow == 0:
            return "kg"
        return f"M^{self.mass_pow}_L^{self.length_pow}_T^{self.time_pow}"

    @classmethod
    def from_string(cls, unit_str: str) -> 'QuantityUnit':
        s = unit_str.strip().lower()
        if s in ["kg", "kilogram", "mass"]:
            return cls(mass_pow=1, length_pow=0, time_pow=0)
        if s in ["n", "newton", "force"]:
            return cls(mass_pow=1, length_pow=1, time_pow=-2)
        if s in ["m/s^2", "m/s2", "acceleration"]:
            return cls(mass_pow=0, length_pow=1, time_pow=-2)
        if s in ["m", "meter", "length"]:
            return cls(mass_pow=0, length_pow=1, time_pow=0)
        if s in ["s", "second", "time"]:
            return cls(mass_pow=0, length_pow=0, time_pow=1)
        return cls()
