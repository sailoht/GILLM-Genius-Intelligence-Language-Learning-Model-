from dataclasses import dataclass, field
from typing import Dict, Any, Iterator, Iterable, Optional

def _get_identity(item: Any) -> str:
    if hasattr(item, 'id') and item.id:
        return str(item.id)
    if hasattr(item, 'molecule_id') and item.molecule_id:
        return str(item.molecule_id)
    return str(hash(item))

@dataclass
class InformationSet:
    """
    Logical set of stable Data Molecule identities.
    Membership is based on stable object identity (e.g. DataMolecule.id),
    preserving DataMolecule mutability without depending on Python object hashing.
    """
    name: str = "GenericSet"
    _elements: Dict[str, Any] = field(default_factory=dict)

    def __init__(self, name: str = "GenericSet", elements: Optional[Iterable[Any]] = None):
        self.name = name
        self._elements = {}
        if elements is not None:
            for item in elements:
                self.add(item)

    def add(self, item: Any):
        key = _get_identity(item)
        self._elements[key] = item

    def remove(self, item: Any):
        key = _get_identity(item)
        if key in self._elements:
            del self._elements[key]
        else:
            raise KeyError(key)

    def contains(self, item: Any) -> bool:
        key = _get_identity(item)
        return key in self._elements

    def __contains__(self, item: Any) -> bool:
        return self.contains(item)

    def union(self, other: 'InformationSet') -> 'InformationSet':
        new_set = InformationSet(name=f"{self.name}_U_{other.name}")
        for item in self._elements.values():
            new_set.add(item)
        for item in other._elements.values():
            new_set.add(item)
        return new_set

    def intersection(self, other: 'InformationSet') -> 'InformationSet':
        new_set = InformationSet(name=f"{self.name}_I_{other.name}")
        for key, item in self._elements.items():
            if key in other._elements:
                new_set.add(item)
        return new_set

    def difference(self, other: 'InformationSet') -> 'InformationSet':
        new_set = InformationSet(name=f"{self.name}_diff_{other.name}")
        for key, item in self._elements.items():
            if key not in other._elements:
                new_set.add(item)
        return new_set

    def is_subset_of(self, other: 'InformationSet') -> bool:
        return set(self._elements.keys()).issubset(set(other._elements.keys()))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, InformationSet):
            return False
        return set(self._elements.keys()) == set(other._elements.keys())

    def __iter__(self) -> Iterator[Any]:
        return iter(self._elements.values())

    def __len__(self) -> int:
        return len(self._elements)

    def size(self) -> int:
        return len(self._elements)
