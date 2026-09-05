import math
from dataclasses import dataclass
from typing import Tuple

@dataclass
class GaussianInformationField:
    """
    Gaussian Information Field representation:
    G(x,y,z) = amplitude * exp(-((x-x0)^2 + (y-y0)^2 + (z-z0)^2) / (2 * sigma^2))
    Serves as an information search/synthesis signal (NOT automatic truth value).
    """
    center: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    amplitude: float = 1.0
    sigma: float = 1.0

    def evaluate(self, x: float, y: float, z: float) -> float:
        x0, y0, z0 = self.center
        dist_sq = (x - x0)**2 + (y - y0)**2 + (z - z0)**2
        return self.amplitude * math.exp(-dist_sq / (2.0 * (self.sigma ** 2)))

    def field_overlap(self, other: 'GaussianInformationField') -> float:
        """Evaluates field-overlap score at midpoint as a search signal."""
        mid_x = (self.center[0] + other.center[0]) / 2.0
        mid_y = (self.center[1] + other.center[1]) / 2.0
        mid_z = (self.center[2] + other.center[2]) / 2.0
        return self.evaluate(mid_x, mid_y, mid_z) * other.evaluate(mid_x, mid_y, mid_z)
