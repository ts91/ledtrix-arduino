#ifndef LEDTRIX_H
#define LEDTRIX_H

#ifdef __cplusplus
extern "C" {
#endif

#include "frame.h"

#define N_SR 4 // number of shift registers per ledtrix
#define N_ROWS 16 // number of multiplexed columns per ledmatrix

void apply_frame(uint32_t value, uint8_t screen[], uint8_t module);

#ifdef __cplusplus
}
#endif

#endif // LEDTRIX_H
