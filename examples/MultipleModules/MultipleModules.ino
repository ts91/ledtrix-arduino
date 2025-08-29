#include <ShiftRegister74HC595.h>
#include <ledtrix.h>

#define N_LEDTRIX 2 // number of ledtrix in the system

uint8_t screen[N_SR * N_LEDTRIX] = { };

#define blank 7
// create a global shift register object
// parameters: <number of shift registers> (data pin, clock pin, latch pin)
ShiftRegister74HC595<N_SR * N_LEDTRIX> sr(0, 1, 2);
// 0b(QH, QG, QF, QE, QD, QC, QB, QA)

void setup() {
  pinMode(blank, OUTPUT);
  digitalWrite(blank, LOW);
}

void loop() {
  for (uint8_t i = 0; i < (N_ROWS); i++) { // each column
    apply_frame(frame_9[i], screen, 0); // module 1
    apply_frame(frame_1[i], screen, 1); // module 2
    sr.setAll(screen);
  }
}
