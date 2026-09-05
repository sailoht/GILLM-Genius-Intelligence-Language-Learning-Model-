from dataclasses import dataclass, field
from typing import Set, Any, List

@dataclass
class InformationSet:
    """
    Set structure adhering strictly to set-theoretic semantics.
    Supports membership, union, intersection, difference, subset.
    """
    name: str
    elements: Set[Any] = field(default_factory=set)

    def add(self, item: Any):
        self.elements.add(item)

    def union(self, other: 'InformationSet') -> 'InformationSet':
        return InformationSet(name=f"{self.name}_∪_{other.name}", elements=self.elements.union(other.elements))

    def intersection(self, other: 'InformationSet') -> 'InformationSet':
        return InformationSet(name=f"{self.name}_∩_{other.name}", elements=self.elements.intersection(other.elements))

    def difference(self, other: 'InformationSet') -> 'InformationSet':
        return InformationSet(name=f"{self.name}_\_{other.name}", elements=self.elements.difference(other.elements))

    def is_subset_of(self, other: 'InformationSet') -> bool:
        return self.elements.issubset(other.elements)
