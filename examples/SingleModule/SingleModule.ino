#include <ShiftRegister74HC595.h>
#include <ledtrix.h>

uint8_t screen[N_SR] = { };

#define blank 7
// create a global shift register object
// parameters: <number of shift registers> (data pin, clock pin, latch pin)
ShiftRegister74HC595<N_SR> sr(0, 1, 2);
// 0b(QH, QG, QF, QE, QD, QC, QB, QA)

void setup() {
  pinMode(blank, OUTPUT);
  digitalWrite(blank, LOW);
}

void loop() {
  for (uint8_t i = 0; i < (N_ROWS); i++) { // each column
    apply_frame(frame_9[i], screen, 0);
    sr.setAll(screen);
  }
}
