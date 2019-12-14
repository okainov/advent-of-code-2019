import math


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

    def get_kinetic(self):
        return abs(self.vx) + abs(self.vy) + abs(self.vz)

    def get_energy(self):
        potential = abs(self.x) + abs(self.y) + abs(self.z)
        kinetic = self.get_kinetic()
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


def lcm(a, b):
    return abs(a * b) // math.gcd(a, b)


if __name__ == '__main__':
    moons = [
        Moon(x, y, z) for x, y, z in [
            (19, -10, 7),
            (1, 2, -3),
            (14, -4, 1),
            (8, 7, -6),
        ]
    ]

    periods = {}
    i = 0
    while True:
        for a, b in produce_pairs(moons):
            apply_gravity(a, b)

        for a in moons:
            a.apply_velocity()
        i += 1

        # Assume:
        #  - cycle IS present in the input data
        #  - we ARE in the cycle already (so there is so some initial movement which *leads* us to the cycle)
        #    3-4-3-4-3-4-3-4-3.... <- we assume system behaves like that
        #    1-2-3-4-3-4-3-4-3-4.... <- and NOT like that
        #  Those are quite strong assumptions IMO, especially the second one.
        #
        # Known that X, Y and Z movements are completely independent from each other,
        # we can find X, Y and Z periods separately and then, given the assumptions, the period of the whole
        # system will be obviously equal to LCM(x_period, y_period, z_period)

        # Check x period
        if moons[0].x == 19 and moons[0].vx == 0 and \
                moons[1].x == 1 and moons[1].vx == 0 and \
                moons[2].x == 14 and moons[2].vx == 0 and \
                moons[3].x == 8 and moons[2].vx == 0 and 'x' not in periods:
            periods['x'] = i
            print(f'X is the same at {i}')

        # Check y period
        if moons[0].y == -10 and moons[0].vy == 0 and \
                moons[1].y == 2 and moons[1].vy == 0 and \
                moons[2].y == -4 and moons[2].vy == 0 and \
                moons[3].y == 7 and moons[2].vy == 0 and 'y' not in periods:
            periods['y'] = i
            print(f'Y is the same at {i}')

        # Check z period
        if moons[0].z == 7 and moons[0].vz == 0 and \
                moons[1].z == -3 and moons[1].vz == 0 and \
                moons[2].z == 1 and moons[2].vz == 0 and \
                moons[3].z == -6 and moons[2].vz == 0 and 'z' not in periods:
            periods['z'] = i
            print(f'z is the same at {i}')

        if len(periods) == 3:
            break

    # LCM(a,b,c) obviously == LCM(a, LCM(b,c))
    print(lcm(periods['z'], lcm(periods['x'], periods['y'])))

    # First part answer:  6227
    # Second part answer: 331346071640472
