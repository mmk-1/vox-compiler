#include "lib_bracket.h"

  .global main
  .text
  .align 2
main:
  addi sp, sp, -40
  sd ra, 32(sp)
            # COPY a, 5
  sd zero, 0(sp)
  li t0, 5
  sd t0, 8(sp)
            # PARAM a
  addi sp, sp, -16
  ld t0, 16(sp)
  sd t0, (sp)
  ld t0, 24(sp)
  sd t0, 8(sp)
            # PARAM a
  addi sp, sp, -16
  ld t0, 32(sp)
  sd t0, (sp)
  ld t0, 40(sp)
  sd t0, 8(sp)
            # CALL tmp0, __br_add__, 2
  mv a1, sp
  li a0, 2
  call __br_add__
  addi sp, sp, 32
  sd a0, 16(sp)
  sd a1, 24(sp)
            # PARAM tmp0
  addi sp, sp, -16
  ld t0, 32(sp)
  sd t0, (sp)
  ld t0, 40(sp)
  sd t0, 8(sp)
            # CALL __br_print__, 1
  mv a1, sp
  li a0, 1
  call __br_print__
  addi sp, sp, 16
  ld ra, 32(sp)
  addi sp, sp, 40
  mv a0, zero
  ret
