from ast import TypeVar
from functools import reduce
from math import factorial
from typing import Literal

from hkociemba_twophase import cubie
from hkociemba_twophase.cubie import CubieCube
from hkociemba_twophase.enums import Color, Corner, Edge


# The lehmer code is a way to encode a permutation of n numbers
def lehmer(perms: list[int]) -> list[int]:
    n = len(perms)
    return [sum(1 for j in range(i + 1, n) if perms[j] < perms[i]) for i in range(n)]


# Since it's a bijective mapping, we can turn lehmer digits back into the specific original permutation
def unlehmer(digits: list[int]) -> list[int]:
    remaining = list(range(len(digits)))
    return [remaining.pop(d) for d in digits]


# We will be using a mixed-radix encoding using horner's method to actually encode the lehmer digits
# for each of the corner and edge permutation into indices (into the list of all possible perms).

# The size of the final integer is math.ceil(math.log2(43_252_003_274_489_856_000)) = 66 bits, which
# is unfortunately just barely too big for a `numpy.int64` and must be stored in a bigint.

# In our encoding we omit the parity digits (digits which *must* have a particular value in order to
# be a solveable cube [see CubieCube#verify]), we reconstruct these digits while decoding.


def encode(cube: CubieCube) -> int:
    cpdigs = lehmer([perm.value for perm in cube.cp])

    # Use horner's method
    cp_idx = 0
    for i in range(8):
        cp_idx = cp_idx * (8 - i) + cpdigs[i]

    epdigs = lehmer([perm.value for perm in cube.ep])
    ep_idx = 0
    for i in range(10):
        ep_idx = ep_idx * (12 - i) + epdigs[i]

    twist = 0
    for t in cube.co[:7]:
        twist = twist * 3 + int(t)
    flip = 0
    for f in cube.eo[:11]:
        flip = flip * 2 + int(f)

    res = cp_idx
    res = res * 3**7 + twist
    res = res * (factorial(12) // 2) + ep_idx
    res = res * 2**11 + flip
    return res


def decode(n: int) -> CubieCube:
    n, flip = divmod(n, 2**11)
    n, ep_idx = divmod(n, factorial(12) // 2)
    cp_idx, twist = divmod(n, 3**7)

    # corners
    cdig = [0] * 8
    for i in reversed(range(8)):
        cp_idx, cdig[i] = divmod(cp_idx, 8 - i)
    cp = unlehmer(cdig)
    cpar = sum(cdig) % 2

    # edges: rebuild forced digit from corner parity
    edig = [0] * 12
    for i in reversed(range(10)):
        ep_idx, edig[i] = divmod(ep_idx, 12 - i)
    edig[10] = (cpar - sum(edig[:10])) % 2
    edig[11] = 0
    ep = unlehmer(edig)

    # orientations: last one fixed by the sum constraint
    co = [0] * 8
    for i in reversed(range(7)):
        twist, co[i] = divmod(twist, 3)
    co[7] = (-sum(co[:7])) % 3
    eo = [0] * 12
    for i in reversed(range(11)):
        flip, eo[i] = divmod(flip, 2)
    eo[11] = sum(eo[:11]) % 2

    return CubieCube(cp=[Corner(i) for i in cp], co=co, ep=[Edge(i) for i in ep], eo=eo)


cube = CubieCube()
cube.multiply(cubie.basicMoveCube[Color.D])
encoded = encode(cube)
newcube = decode(encoded)
print(newcube.to_facelet_cube().to_2dstring())

# # Is an 8-tuple
# CornerPerms = tuple[Literal[0, 1, 2], ...]

# corner_orientation_lut: list[CornerPerms] = list(itertools.product((0, 1, 2), repeat=8))

# # Is a 12-tuple
# EdgePerms = tuple[Literal[0, 1], ...]

# edge_orientation_lut: list[EdgePerms] = list(itertools.product((0, 1), repeat=12))

# print(corner_orientation_lut)


# def cubie_repr_to_int(cubie: CubieCube) -> int:
#     corner_perms = 0
#     for i, perm in enumerate(cubie.cp):
#         corner_perms &= perm << i
#     print(corner_perms)

#     corner_orients = lookup(cubie.co, corner_orientation_lut)

#     edge_perms = 0
#     for i, perm in enumerate(cubie.ep):
#         edge_perms &= perm << i
#     print(edge_perms)

#     edge_orients = lookup(cubie.eo, edge_orientation_lut)

#     return 0


# def lookup(orients: list[int], orients_lut) -> int:
#     for i, orient in enumerate(orients_lut):
#         fits = True
#         for x, y in zip(orients, orient):
#             fits = fits and x == y
#         if fits:
#             return i
#     return -1


# # From LSB to MSB:
# # * First 24 bits = corner permutations (log_2(8) = 3 => 3 bytes * 8 corners = 24 bits)
# # * Next 16 bits = corner orientations (0, 1, 2 => 2 bits * 8 corners = 16 bits)
# # * Next 48 bits = edge permutations (0..12 => 4 bits * 12 edges = 48 bits)
# # * Next 12 bits = edge orientations (0, 1 => 1 bits * 12 edges = 12 bits)
