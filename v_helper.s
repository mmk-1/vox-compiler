.global _vv_add

.text
.align 2

_vv_add:
  blez a3, .L4
.L3:
  vsetvli t0, a3, e64, m8, tu, mu
  vle64.v v0, (a0)
  vle64.v v8, (a1)
  vadd.vv v0, v0, v8
  vse64.v v0, (a2)
  sub a3, a3, t0
  slli t1, t0, 3
  add a0, a0, t1
  add a1, a1, t1
  add a2, a2, t1
  bgtz a3, .L3
.L4:
  ret
