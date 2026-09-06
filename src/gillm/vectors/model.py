import math
from typing import List, Tuple, Union, Sequence

class Vector:
    """
    General, reusable vector abstraction for physical state, velocity, acceleration,
    delta state, position, and arbitrary dimension calculations.
    """
    def __init__(self, components: Sequence[float]):
        if not components:
            raise ValueError("Vector components cannot be empty.")
        self.components: Tuple[float, ...] = tuple(float(x) for x in components)

    @property
    def dimension(self) -> int:
        return len(self.components)

    def _check_dim(self, other: 'Vector'):
        if self.dimension != other.dimension:
            raise ValueError(f"Vector dimension mismatch: {self.dimension} vs {other.dimension}")

    def __add__(self, other: 'Vector') -> 'Vector':
        self._check_dim(other)
        return Vector([a + b for a, b in zip(self.components, other.components)])

    def __sub__(self, other: 'Vector') -> 'Vector':
        self._check_dim(other)
        return Vector([a - b for a, b in zip(self.components, other.components)])

    def __mul__(self, scalar: Union[int, float]) -> 'Vector':
        return Vector([a * scalar for a in self.components])

    def __rmul__(self, scalar: Union[int, float]) -> 'Vector':
        return self.__mul__(scalar)

    def dot(self, other: 'Vector') -> float:
        self._check_dim(other)
        return sum(a * b for a, b in zip(self.components, other.components))

    def magnitude(self) -> float:
        return math.sqrt(sum(a * a for a in self.components))

    def norm(self) -> float:
        return self.magnitude()

    def normalize(self) -> 'Vector':
        mag = self.magnitude()
        if mag == 0:
            return Vector([0.0] * self.dimension)
        return Vector([a / mag for a in self.components])

    @classmethod
    def zero(cls, dimension: int) -> 'Vector':
        if dimension <= 0:
            raise ValueError("Dimension must be positive.")
        return cls([0.0] * dimension)

    def to_list(self) -> List[float]:
        return list(self.components)

    def to_tuple(self) -> Tuple[float, ...]:
        return self.components

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector):
            return False
        if self.dimension != other.dimension:
            return False
        return all(math.isclose(a, b, abs_tol=1e-9) for a, b in zip(self.components, other.components))

    def __repr__(self) -> str:
        return f"Vector({list(self.components)})"
