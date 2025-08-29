#include "ledtrix.h"

/**
 * @brief Applies a 32-bit frame value to the output array for a specific module.
 *
 * This function splits the 32-bit frame value into four 8-bit segments and stores them
 * in the output array at the position corresponding to the given module.
 *
 * @param value   The 32-bit frame value to apply.
 * @param screen  The output screen array where the frame bytes will be stored.
 * @param module  The module index (used to calculate the offset in the output array).
 */
void apply_frame(uint32_t value, uint8_t screen[], uint8_t module) {
  uint8_t offset = module * 4;
  screen[offset + 3] = (uint8_t)((value >> 24) & 0xFF);
  screen[offset + 2] = (uint8_t)((value >> 16) & 0xFF);
  screen[offset + 1] = (uint8_t)((value >> 8) & 0xFF);
  screen[offset + 0] = (uint8_t)(value & 0xFF);
}