""" Provides function to translate LED patterns into frames.

Patterns are simple human readable representations of the LED matrix state. That is
a coordinate system where each LED is addressed by its (column, row) position. The
output is a frame, which is an array that defines the shift register state for
controlling the LED matrix. Since a matrix has two high-side and two low-side shift
registers and each column must be multiplexed, then a full frame will consist of
16 x 32 bit.
"""
from itertools import product

def convert_all_patterns(patterns: dict[str, list[tuple[int, int]]]) -> dict[str, list[int]]:
    """
    Converts all patterns to frames.
    """
    frames = {}
    for key, pattern in patterns.items():
        frames[key] = pattern_to_frame(pattern)
    return frames

# Translates the control designators into actual bit positions in the chain of shift registers
t_ctrl2bit = {
    'L5': 0,
    'L2': 1,
    'L3': 2,
    'L4': 3,
    'L6': 4,
    'L1': 5,
    'L7': 6,
    'L8': 7,
    'H16': 8,
    'H11': 9,
    'H14': 10,
    'H9': 11,
    'H10': 12,
    'H12': 13,
    'H15': 14,
    'H13': 15,
    'L13': 16,
    'L10': 17,
    'L11': 18,
    'L16': 19,
    'L15': 20,
    'L9': 21,
    'L14': 22,
    'L12': 23,
    'H6': 24,
    'H1': 25,
    'H3': 26,
    'H2': 27,
    'H4': 28,
    'H8': 29,
    'H5': 30,
    'H7': 31
}

# A matrix is made out of four 8x8 modules. These maps translate columns and rows into a control designator
map_u203 = {
    'c4' : 'H12', # pin 1
    'c2' : 'H10', # pin 2
    'r2' : 'L2',  # pin 3
    'r3' : 'L3',  # pin 4
    'c1' : 'H9',  # pin 5
    'r5' : 'L5',  # pin 6
    'c3' : 'H11', # pin 7
    'c6' : 'H14', # pin 8
    'c8' : 'H16', # pin 9
    'r4' : 'L4',  # pin 10
    'r6' : 'L6',  # pin 11
    'c5' : 'H13', # pin 12
    'r1' : 'L1',  # pin 13
    'c7' : 'H15', # pin 14
    'r7' : 'L7',  # pin 15
    'r8' : 'L8'   # pin 16
}

map_u201 = {
    'c4' : 'H4',  # pin 1
    'c2' : 'H2',  # pin 2
    'r2' : 'L3',  # pin 3
    'r3' : 'L2',  # pin 4
    'c1' : 'H1',  # pin 5
    'r5' : 'L5',  # pin 6
    'c3' : 'H3',  # pin 7
    'c6' : 'H6',  # pin 8
    'c8' : 'H8',  # pin 9
    'r4' : 'L8',  # pin 10
    'r6' : 'L7',  # pin 11
    'c5' : 'H5',  # pin 12
    'r1' : 'L1',  # pin 13
    'c7' : 'H7',  # pin 14
    'r7' : 'L6',  # pin 15
    'r8' : 'L4'   # pin 16
}

map_u202 = {
    'c4' : 'H6',  # pin 1
    'c2' : 'H3',  # pin 2
    'r2' : 'L10', # pin 3
    'r3' : 'L11', # pin 4
    'c1' : 'H1',  # pin 5
    'r5' : 'L13', # pin 6
    'c3' : 'H2',  # pin 7
    'c6' : 'H4',  # pin 8
    'c8' : 'H7',  # pin 9
    'r4' : 'L12', # pin 10
    'r6' : 'L14', # pin 11
    'c5' : 'H5',  # pin 12
    'r1' : 'L9',  # pin 13
    'c7' : 'H8',  # pin 14
    'r7' : 'L15', # pin 15
    'r8' : 'L16'  # pin 16
}

map_u204 = {
    'c4' : 'H14', # pin 1
    'c2' : 'H11', # pin 2
    'r2' : 'L13', # pin 3
    'r3' : 'L11', # pin 4
    'c1' : 'H9',  # pin 5
    'r5' : 'L10', # pin 6
    'c3' : 'H10', # pin 7
    'c6' : 'H12', # pin 8
    'c8' : 'H15', # pin 9
    'r4' : 'L16', # pin 10
    'r6' : 'L15', # pin 11
    'c5' : 'H13', # pin 12
    'r1' : 'L9',  # pin 13
    'c7' : 'H16', # pin 14
    'r7' : 'L14', # pin 15
    'r8' : 'L12'  # pin 16
}

# Describes how the matrix is made up of 8x8 modules. There are 4, they are placed in a matrix, and can be rotated
# 90 degrees clockwise or counter clockwise.
matrix = {
    (1, 1) : {
        'map' : map_u203,
        'rot' : 1
    },
    (1, 2): {
        'map': map_u201,
        'rot': 1
    },
    (2, 1): {
        'map': map_u204,
        'rot': -1
    },
    (2, 2): {
        'map': map_u202,
        'rot': -1
    }
}

def module_position_to_designator(map_ux: dict[str, str]) -> dict[tuple[int, int], tuple[str, str]]:
    """
    Makes a map from rows and columns into the designators. This is the designators needed to turn on
    in order for the LED at the row and column to light up. Example:
    (1, 1) -> ("L8", H3")
    :return: map from rows and columns to designators
    """
    module_map = {}

    for x in product(tuple(range(1, 8 + 1)),
                     tuple(range(1, 8 + 1))):
        module_map[(x[0], x[1])] = (map_ux['r' + str(x[0])] , map_ux['c' + str(x[1])])

    return module_map

def place_module_in_matrix(module_map: dict[tuple[int, int], tuple[str, str]], rot: int, pos: tuple[int, int]) -> dict[tuple[int, int], tuple[str, str]]:
    """
    Places module along other modules in the matrix and adjust the map accordingly
    :param module_map: map of rows and columns to designators for the module
    :param rot: rotation. Can rotate clockwise and ccw
    :param pos: Translate to the position in matrix
    :return: map of rows and columns to designators for the module in the matrix
    """

    # rotate
    def rotate_module_map(module_map, rot):
        ret = {}

        for k, v in module_map.items():
            if rot == 1:
                #  90:
                ret[((8 + 1) - k[1], k[0])] = v

            elif rot == -1:
                # -90
                ret[(k[1], (8 + 1) - k[0])] = v
            
            else: # no rotation
                ret[(k[0], k[1])] = v
        
        return ret

    # translate
    def translate_module_map(module_map, pos):
        ret = {}

        for k, v in module_map.items():
            ret[(k[0] + (pos[0] - 1) * 8, k[1] + (pos[1] - 1) * 8)] = v

        return ret
    
    matrix_map = rotate_module_map(module_map, rot)
    matrix_map = translate_module_map(matrix_map, pos)

    return matrix_map

def manipulation_map() -> dict[tuple[int, int], tuple[int, int]]:
    """
    Makes the map from rows and columns into the bits in the chain of shift registers. This is the the two bits needed to be manipulated
    in order for the LED at the row and column to light up. The two bits is always low-side and high-side. Example:

    (1, 1) -> (4, 12) // for the LED at row 1 and column 1, the bits 4 and 12 needs to be manipulated

    :return: map from rows and columns to bits in the chain of shift registers
    """
    ret = {}

    for k, v in matrix.items():
        for k, v in place_module_in_matrix(module_position_to_designator(v['map']), v['rot'], pos=k).items():
            ret[k] = v

    return {k: (t_ctrl2bit[v[0]], t_ctrl2bit[v[1]]) for k, v in ret.items()}

def pattern_to_frame(pattern: list[tuple[int, int]]) -> list[int]:
    """
    Converts a pattern to a frame. A frame is a list of 32-bit integers, where each integer represents a row in the matrix. There
    are 16 integers in the list, scanning over each of these produces the frame. This is MSB first.
    :param pattern: list of tuples of rows and columns
    :return: list of 16 32-bit integers
    """
    manmap = manipulation_map()
    all_off = 0b11111111000000001111111100000000
    ret = [all_off] * 16

    for p in pattern:
        led = manmap[p]
        # scan over low-side - row. NOTE: This causes brightness issues!!!
        #row = led_to_row(led)
        #ret[row] |= (1 << led[0])
        #ret[row] &= ~(1 << led[1]) # high-side is inverted

        # scan over high-side - column.
        col = led_to_col(led)
        ret[col] |= (1 << led[0])
        ret[col] &= ~(1 << led[1]) # high-side is inverted

        # debug:
        #print(f'Pattern: {p}, Manipulation: {led}, Frame: {ret[p[1] - 1]:032b}')

    return ret

def led_to_row(led: tuple[int]) -> int:
    """ Converts a LED position to a row in the frame.
    :param led: tuple of (row, column)
    :return: row in the frame"""
    return (led[0] - 1) % 16 + (8 * ((led[0] - 1) // 16))

def led_to_col(led: tuple[int]) -> int:
    """ Converts a LED position to a column in the frame.
    :param led: tuple of (row, column)
    :return: column in the frame"""
    return (led[1] - 1) % 16 + (8 * ((led[1] - 1) // 16) - 8)

def all_in_row(n, pattern=None):
    """ Turns all the LEDs on in a row
    :param n: row number
    :param pattern: pattern to append to
    """
    if pattern is None:
        pattern = []
    for i in range(1, 16 + 1):
        pattern.append((n, i))

    return pattern


def all_in_col(n, pattern=None):
    """ Turns all the LEDs on in a column
    :param n: column number
    :param pattern: pattern to append to
    """
    if pattern is None:
        pattern = []
    for i in range(1, 16 + 1):
        pattern.append((i, n))

    return pattern

def chain_modules(patterns: list[list[tuple[int, int]]]) -> list[tuple[int, int]]:
    """
    Chains multiple patterns together.
    :param patterns: list of patterns to chain
    :return: chained pattern
    """
    for p in patterns:
        if len(p) != 16:
            raise ValueError("Each pattern must have exactly 16 elements.")
    
    zipped = zip(*patterns)

    ret = []
    for element in zipped:
        for e in element:
            ret.append(e)

    return ret
