# Ledtrix a LED matrix module library

This is the library for 

## Install (Arduino)

1. Two ways:
   - Click Add .ZIP Library from Arduino IDE under Sketch > Include Library (prefered) 
   - Copy the entire `Ledtrix` folder (including `src` and `library.properties`) into your Arduino libraries directory (On Windows, this is usually: `Documents\Arduino\libraries`)
2. Restart the Arduino IDE if it was open.
3. In your sketch, include your library with:
   ```cpp
   #include <ledtrix.h>
   ```
4. The library will now be available in the Arduino IDE under Sketch > Include Library and examles are provided under File > Examples > Ledtrix

## TODO

NOTE:

make python script that extracts pin configurations directly from a KICAD file

NOTE:

Awkward multi step process to generate pattern.c/h
Better to have it all in javascript. 

Right side: a graphical view of the matrix, Left side: the c pattern for copy/paste

