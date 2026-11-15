import itertools
from math import factorial

from hkociemba_twophase import cubie
from hkociemba_twophase.cubie import CubieCube
from hkociemba_twophase.enums import Color, Corner, Edge
from hkociemba_twophase.solver import SolverThread, solve


# The lehmer code is a way to encode a permutation of n numbers
def lehmer(perm: list[int]) -> list[int]:
    n = len(perm)
    return [sum(1 for j in range(i + 1, n) if perm[j] < perm[i]) for i in range(n)]


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
    corner_perm_digits = lehmer([perm for perm in cube.cp])

    # Use horner's method
    corner_perm_index = 0
    for i in range(8):
        corner_perm_index = corner_perm_index * (8 - i) + corner_perm_digits[i]

    edge_perm_digits = lehmer([perm for perm in cube.ep])
    edge_perm_index = 0
    for i in range(10):
        edge_perm_index = edge_perm_index * (12 - i) + edge_perm_digits[i]

    # A trinary number where each digit is a corner orientation (a twist)
    twist = 0
    for t in cube.co[:7]:
        twist = twist * 3 + int(t)
    # Just a binary number where each digit is an edge orientation (a flip)
    flip = 0
    for f in cube.eo[:11]:
        flip = flip * 2 + int(f)

    res = corner_perm_index
    res = res * 3**7 + twist
    res = res * (factorial(12) // 2) + edge_perm_index
    res = res * 2**11 + flip
    return res


def decode(n: int) -> CubieCube:
    n, flip = divmod(n, 2**11)
    n, edge_perm_index = divmod(n, factorial(12) // 2)
    corner_perm_index, twist = divmod(n, 3**7)

    corner_perm_digits = [0] * 8
    for i in reversed(range(8)):
        corner_perm_index, corner_perm_digits[i] = divmod(corner_perm_index, 8 - i)
    corner_perm = unlehmer(corner_perm_digits)
    corner_parity = sum(corner_perm_digits) % 2

    # edges: rebuild forced digit from corner parity
    edge_perm_digits = [0] * 12
    for i in reversed(range(10)):
        edge_perm_index, edge_perm_digits[i] = divmod(edge_perm_index, 12 - i)
    edge_perm_digits[10] = (corner_parity - sum(edge_perm_digits[:10])) % 2
    edge_perm_digits[11] = 0
    edge_perm = unlehmer(edge_perm_digits)

    # orientations: last one fixed by the sum constraint
    corner_orient = [0] * 8
    for i in reversed(range(7)):
        twist, corner_orient[i] = divmod(twist, 3)
    corner_orient[7] = (-sum(corner_orient[:7])) % 3

    edge_orient = [0] * 12
    for i in reversed(range(11)):
        flip, edge_orient[i] = divmod(flip, 2)
    edge_orient[11] = sum(edge_orient[:11]) % 2

    return CubieCube(
        cp=[Corner(i) for i in corner_perm],
        co=corner_orient,
        ep=[Edge(i) for i in edge_perm],
        eo=edge_orient,
    )


def load_words() -> list[str]:
    with open("durhack_word_list.csv", "r") as f:
        return f.read().splitlines()


def test():
    c = CubieCube()
    c.multiply(cubie.basicMoveCube[Color.U])
    solution = solve(c.to_facelet_cube().to_string(), max_length=30)
    print(solution)
    # Now we need to invert this to get the original scramble


def inverse_moves(moves: str) -> str:
    res: list[str] = []
    moves_list = moves.split()
    moves_list.pop()  # Remove the (20f) stuff
    for move in moves_list:
        dir = move[0]
        if len(move) > 1:
            if move[1] == "1":
                res.append(dir + "'")
            # elif move[1] == "'":
            #     res.append(dir)
            elif move[1] == "2":
                res.append(move)
            elif move[1] == "3":
                res.append(dir)
        else:
            res.append(dir + "'")

    return " ".join(reversed(res))


def process_moves(moves: str) -> str:
    res: list[str] = []
    moves_list = moves.split()
    moves_list.pop()  # Remove the (20f) stuff
    for move in moves_list:
        dir = move[0]
        if len(move) > 1:
            if move[1] == "1":
                res.append(dir)
            elif move[1] == "2":
                res.append(move)
            elif move[1] == "3":
                res.append(dir + "'")
        else:
            res.append(move)

    return " ".join(res)


if __name__ == "__main__":
    c = CubieCube()
    c.randomize()
    solution = solve(c.to_facelet_cube().to_string(), max_length=30)

    print("Scramble: ", inverse_moves(solution))
    print("Solution: ", process_moves(solution))

# cube = CubieCube()
# cube.multiply(cubie.basicMoveCube[Color.D])
# encoded = encode(cube)
# newcube = decode(1)
# print(newcube.to_facelet_cube().to_2dstring())

# for _ in range(1000):
#     c = CubieCube()
#     c.randomize()
#     d = decode(encode(c))
#     assert (d.cp, d.co, d.ep, d.eo) == (c.cp, c.co, c.ep, c.eo)

# === OLD FAILED REPRESENTATION ===
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
