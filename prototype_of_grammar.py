from dataclasses import dataclass, field
from collections import deque
import math

# -----------------------------
# Information Particle
# -----------------------------

@dataclass
class Particle:
    name: str
    mass: float = 1.0
    energy: float = 1.0
    position: list = field(default_factory=lambda: [0.0, 0.0, 0.0])
    links: set = field(default_factory=set)


# -----------------------------
# GillM Prototype
# -----------------------------

class GillM:

    def __init__(self):
        self.nodes = {}

    # -------------------------

    def get_particle(self, name):

        name = name.lower()

        if name not in self.nodes:

            # deterministic pseudo-position
            h = abs(hash(name))

            x = (h % 97) / 10
            y = ((h // 97) % 97) / 10
            z = ((h // 97 // 97) % 97) / 10

            self.nodes[name] = Particle(
                name=name,
                position=[x, y, z]
            )

        return self.nodes[name]

    # -------------------------

    def connect(self, a, b):

        pa = self.get_particle(a)
        pb = self.get_particle(b)

        pa.links.add(pb.name)
        pb.links.add(pa.name)

        pa.mass += 0.5
        pb.mass += 0.5

        pa.energy += 0.2
        pb.energy += 0.2

    # -------------------------

    def learn(self, sentence):

        words = (
            sentence.lower()
            .replace(".", "")
            .replace(",", "")
            .split()
        )

        if len(words) < 3:
            return

        subject = words[0]
        verb = words[1]
        obj = words[-1]

        self.connect(subject, verb)
        self.connect(verb, obj)

    # -------------------------

    def search(self, word):

        word = word.lower()

        if word not in self.nodes:
            return []

        return sorted(self.nodes[word].links)

    # -------------------------

    def center_of_mass(self):

        total_mass = 0

        cx = cy = cz = 0

        for p in self.nodes.values():

            m = p.mass

            total_mass += m

            cx += m * p.position[0]
            cy += m * p.position[1]
            cz += m * p.position[2]

        if total_mass == 0:
            return None

        return (
            round(cx / total_mass, 3),
            round(cy / total_mass, 3),
            round(cz / total_mass, 3),
        )

    # -------------------------

    def reasoning_path(self, start, goal):

        start = start.lower()
        goal = goal.lower()

        if start not in self.nodes:
            return None

        q = deque([[start]])
        visited = {start}

        while q:

            path = q.popleft()

            node = path[-1]

            if node == goal:
                return path

            for nxt in self.nodes[node].links:

                if nxt not in visited:
                    visited.add(nxt)
                    q.append(path + [nxt])

        return None

    # -------------------------

    def show(self):

        print("\n========== KNOWLEDGE ==========\n")

        for p in sorted(self.nodes.values(), key=lambda x: x.name):

            print("Particle :", p.name)
            print("Mass     :", round(p.mass,2))
            print("Energy   :", round(p.energy,2))
            print("Position :", p.position)
            print("Links    :", sorted(p.links))
            print()


# -----------------------------
# Example Training
# -----------------------------

brain = GillM()

brain.learn("Car uses fuel.")
brain.learn("Tesla is car.")
brain.learn("Tesla uses battery.")
brain.learn("Battery stores energy.")
brain.learn("Car moves road.")

brain.show()

print("Center Of Mass")
print(brain.center_of_mass())

print()

print("Search 'car'")
print(brain.search("car"))

print()

print("Reasoning Tesla -> Energy")

print(brain.reasoning_path("tesla","energy"))
