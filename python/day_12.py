class Moon:
    def __init__(self, x, y, z, vx=0, vy=0, vz=0):
        self.x = x
        self.y = y
        self.z = z
        self.vx = vx
        self.vy = vy
        self.vz = vz

    def apply_velocity(self):
        self.x += self.vx
        self.y += self.vy
        self.z += self.vz

    def get_energy(self):
        potential = abs(self.x) + abs(self.y) + abs(self.z)
        kinetic = abs(self.vx) + abs(self.vy) + abs(self.vz)
        return potential * kinetic

    def __repr__(self):
        return f'({self.x}, {self.y}, {self.z}) -> ({self.vx}, {self.vy}, {self.vz})'


def apply_gravity(a: Moon, b: Moon):
    if a.x > b.x:
        a.vx -= 1
        b.vx += 1
    elif a.x < b.x:
        a.vx += 1
        b.vx -= 1
    if a.y > b.y:
        a.vy -= 1
        b.vy += 1
    elif a.y < b.y:
        a.vy += 1
        b.vy -= 1
    if a.z > b.z:
        a.vz -= 1
        b.vz += 1
    elif a.z < b.z:
        a.vz += 1
        b.vz -= 1


def produce_pairs(moons):
    for i in range(len(moons) - 1):
        for j in range(i + 1, len(moons)):
            yield moons[i], moons[j]


if __name__ == '__main__':
    moons = [
        Moon(x, y, z) for x, y, z in [
            (19, -10, 7),
            (1, 2, -3),
            (14, -4, 1),
            (8, 7, -6),
        ]
    ]

    for step in range(1000):
        for a, b in produce_pairs(moons):
            apply_gravity(a, b)
        for a in moons:
            a.apply_velocity()

    total_energy = 0
    for a in moons:
        total_energy += a.get_energy()
    print(total_energy)

    # First part answer:  6227
    # Second part answer:
