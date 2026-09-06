from dataclasses import dataclass, field
from typing import Set, Any, Iterator, Iterable, Optional

@dataclass
class InformationSet:
    """
    General, reusable set abstraction adhering strictly to set-theoretic semantics.
    Duplicates are not separate elements.
    """
    name: str = "GenericSet"
    elements: Set[Any] = field(default_factory=set)

    def __init__(self, name: str = "GenericSet", elements: Optional[Iterable[Any]] = None):
        self.name = name
        self.elements = set(elements) if elements is not None else set()

    def add(self, item: Any):
        self.elements.add(item)

    def remove(self, item: Any):
        self.elements.remove(item)

    def contains(self, item: Any) -> bool:
        return item in self.elements

    def __contains__(self, item: Any) -> bool:
        return item in self.elements

    def union(self, other: 'InformationSet') -> 'InformationSet':
        return InformationSet(name=f"{self.name}_∪_{other.name}", elements=self.elements.union(other.elements))

    def intersection(self, other: 'InformationSet') -> 'InformationSet':
        return InformationSet(name=f"{self.name}_∩_{other.name}", elements=self.elements.intersection(other.elements))

    def difference(self, other: 'InformationSet') -> 'InformationSet':
        return InformationSet(name=f"{self.name}_\_{other.name}", elements=self.elements.difference(other.elements))

    def is_subset_of(self, other: 'InformationSet') -> bool:
        return self.elements.issubset(other.elements)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, InformationSet):
            return False
        return self.elements == other.elements

    def __iter__(self) -> Iterator[Any]:
        return iter(self.elements)

    def __len__(self) -> int:
        return len(self.elements)

    def size(self) -> int:
        return len(self.elements)
