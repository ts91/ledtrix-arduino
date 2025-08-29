def format_c_code(name: str, frame: list[int]) -> str:
    """
    Formats the frame as a C array. These are MSB first such that 0b(SREG1(U208): QH, QG, QF, QE, QD, QC, QB, QA)(SREG2(U207): QH, QG, QF, QE, QD, QC, QB, QA)(SREG3(U206): QH, QG, QF, QE, QD, QC, QB, QA)(SREG4(U205): QH, QG, QF, QE, QD, QC, QB, QA)
    :param frame: list of 32-bit integers
    :return: C array
    """
    ret = 'uint32_t frame_' + name + '[' + str(len(frame)) + '] = {\n'

    for _, f in enumerate(frame):
        ret += '0b' + format(f, '032b') + ',\n'

    ret += '};'

    return ret

def h_file(frames: dict[str, list[int]]) -> str:
    """
    Generates a C header file with the given names.
    :param names: list of names to include in the header
    :return: C header file as a string
    """
    ret = '#ifndef FRAME_H\n#define FRAME_H\n\n#include <stdint.h>\n\n'

    for name, frame in frames.items():
        ret += f'extern uint32_t frame_{name}[{len(frame)}];\n'

    ret += '\n#endif // FRAME_H\n'

    return ret

def c_file(frames: dict[str, list[int]]) -> str:
    """
    Generates a C source file with the given frames.
    :param frames: list of tuples of (name, frame)
    :return: C source file as a string
    """
    ret = '#include "frame.h"\n\n'

    for name, frame in frames.items():
        ret += format_c_code(name, frame) + '\n\n'

    return ret
