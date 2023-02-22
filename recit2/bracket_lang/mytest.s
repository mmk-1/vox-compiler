#include "lib_bracket.h"

  .global main
  .text
  .align 2
main:
  addi sp, sp, -40
  sd ra, 32(sp)
            # PARAM 1
  addi sp, sp, -16
  sd zero, (sp)
  li t0, 1
  sd t0, 8(sp)
            # PARAM 2
  addi sp, sp, -16
  sd zero, (sp)
  li t0, 2
  sd t0, 8(sp)
            # CALL tmp0, __br_add__, 2
  mv a1, sp
  li a0, 2
  call __br_add__
  addi sp, sp, 32
  sd a0, 0(sp)
  sd a1, 8(sp)
            # COPY b, tmp0
  ld t0, 0(sp)
  sd t0, 16(sp)
  ld t0, 8(sp)
  sd t0, 24(sp)
  ld ra, 32(sp)
  addi sp, sp, 40
  mv a0, zero
  ret
