import math
from dataclasses import dataclass
from typing import Tuple

@dataclass
class SpatialCoordinate:
    """Extensible 3D coordinate representation (x, y, z)."""
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    def distance_to(self, other: 'SpatialCoordinate') -> float:
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2 + (self.z - other.z)**2)

    def to_tuple(self) -> Tuple[float, float, float]:
        return (self.x, self.y, self.z)
