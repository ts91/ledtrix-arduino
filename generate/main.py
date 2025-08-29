""" Generates C source and header files for LED matrix frames.

It imports LED patterns, translates them into frames using the translator module,
and writes the resulting data to frame.c and frame.h for use in firmware.
"""
from patterns import my_patterns
from translator import convert_all_patterns
from writer import c_file, h_file

my_frames = convert_all_patterns(my_patterns)

with open("./frame.c", "w", encoding="utf-8") as f:
    f.write(c_file(my_frames))

with open("./frame.h", "w", encoding="utf-8") as f:
    f.write(h_file(my_frames))
