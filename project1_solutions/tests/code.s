  .global main
      .text
      .align 2
    main:
      addi sp, sp, -96
      sd ra, 88(sp)
    		#('STRING', 'Fibonacci', 9, 'tmp0')
  addi sp, sp, -8
  sd zero, (sp)
  li t0, 105
  sd t0, (sp)
  addi sp, sp, -8
  sd zero, (sp)
  li t0, 99
  sd t0, (sp)
  addi sp, sp, -8
  sd zero, (sp)
  li t0, 99
  sd t0, (sp)
  addi sp, sp, -8
  sd zero, (sp)
  li t0, 97
  sd t0, (sp)
  addi sp, sp, -8
  sd zero, (sp)
  li t0, 110
  sd t0, (sp)
  addi sp, sp, -8
  sd zero, (sp)
  li t0, 111
  sd t0, (sp)
  addi sp, sp, -8
  sd zero, (sp)
  li t0, 98
  sd t0, (sp)
  addi sp, sp, -8
  sd zero, (sp)
  li t0, 105
  sd t0, (sp)
  addi sp, sp, -8
  sd zero, (sp)
  li t0, 70
  sd t0, (sp)
  mv a1, sp
  li a0, 9
  call __init_string__
  addi sp, sp, 72
  sd a0, 8(sp)
		#('PRINT', 'NULL', 'STRING', 'tmp0')
  ld a0, 8(sp)
  addi sp, sp, -8
  sd a0, 0(sp)
  call __string_print__
  ld a0, 0(sp)
  addi sp, sp, 8
		#('COPY', '10', 'NULL', 'tmp2')
  sd zero, 48(sp)
  li t0, 10
  sd t0, 48(sp)
		#('PARAM', 0, 'NULL', 'tmp2')
  ld a0, 48(sp)
		#('CALL', 'tmp2', 1, 'fib')
  jal fib
  sd a0, 48(sp)
		#('COPY', 'tmp2', 'NULL', 'c')
  ld t0, 48(sp)
  sd t0, 56(sp)
		#('PRINT', 'NULL', 'NULL', 'c')
  ld a0, 56(sp)
  addi sp, sp, -8
  sd a0, 0(sp)
  call __print_helper__
  ld a0, 0(sp)
  addi sp, sp, 8
		#('STRING', 'Factorial', 9, 'tmp3')
  addi sp, sp, -8
  sd zero, (sp)
  li t0, 108
  sd t0, (sp)
  addi sp, sp, -8
  sd zero, (sp)
  li t0, 97
  sd t0, (sp)
  addi sp, sp, -8
  sd zero, (sp)
  li t0, 105
  sd t0, (sp)
  addi sp, sp, -8
  sd zero, (sp)
  li t0, 114
  sd t0, (sp)
  addi sp, sp, -8
  sd zero, (sp)
  li t0, 111
  sd t0, (sp)
  addi sp, sp, -8
  sd zero, (sp)
  li t0, 116
  sd t0, (sp)
  addi sp, sp, -8
  sd zero, (sp)
  li t0, 99
  sd t0, (sp)
  addi sp, sp, -8
  sd zero, (sp)
  li t0, 97
  sd t0, (sp)
  addi sp, sp, -8
  sd zero, (sp)
  li t0, 70
  sd t0, (sp)
  mv a1, sp
  li a0, 9
  call __init_string__
  addi sp, sp, 72
  sd a0, 72(sp)
		#('PRINT', 'NULL', 'STRING', 'tmp3')
  ld a0, 72(sp)
  addi sp, sp, -8
  sd a0, 0(sp)
  call __string_print__
  ld a0, 0(sp)
  addi sp, sp, 8
		#('COPY', '7', 'NULL', 'tmp5')
  sd zero, 0(sp)
  li t0, 7
  sd t0, 0(sp)
		#('PARAM', 0, 'NULL', 'tmp5')
  ld a0, 0(sp)
		#('CALL', 'tmp5', 1, 'factorial')
  jal factorial
  sd a0, 0(sp)
		#('COPY', 'tmp5', 'NULL', 'c')
  ld t0, 0(sp)
  sd t0, 56(sp)
		#('PRINT', 'NULL', 'NULL', 'c')
  ld a0, 56(sp)
  addi sp, sp, -8
  sd a0, 0(sp)
  call __print_helper__
  ld a0, 0(sp)
  addi sp, sp, 8
		#('OP+', '1', '1', 'tmp7')
  li t0, 1
  li t1, 1
  add t0, t0, t1
  sd t0, 24(sp)
		#('PARAM', 0, 'NULL', 'tmp7')
  ld a0, 24(sp)
		#('COPY', '2', 'NULL', 'tmp8')
  sd zero, 32(sp)
  li t0, 2
  sd t0, 32(sp)
		#('PARAM', 1, 'NULL', 'tmp8')
  ld a1, 32(sp)
		#('COPY', '3', 'NULL', 'tmp9')
  sd zero, 64(sp)
  li t0, 3
  sd t0, 64(sp)
		#('PARAM', 2, 'NULL', 'tmp9')
  ld a2, 64(sp)
		#('CALL', 'tmp9', 3, 'sum')
  jal sum
  sd a0, 64(sp)
		#('COPY', 'tmp9', 'NULL', 'c')
  ld t0, 64(sp)
  sd t0, 56(sp)
		#('PRINT', 'NULL', 'NULL', 'c')
  ld a0, 56(sp)
  addi sp, sp, -8
  sd a0, 0(sp)
  call __print_helper__
  ld a0, 0(sp)
  addi sp, sp, 8
		#('EPILOGUE',)
  ld ra, 88(sp)
  addi sp, sp, 96
  mv a0, zero
  ret
		#('LABEL', 'NULL', 'NULL', 'sum:')
sum:
		#('FUNPUSH', 3, 'NULL', 'env0')
  addi sp, sp, -72
sd a0, 0(sp)
sd a1, 32(sp)
sd a2, 16(sp)
  sd ra, 64(sp)
		#('COPY', '0', 'NULL', 'i')
  sd zero, 40(sp)
  li t0, 0
  sd t0, 40(sp)
		#('STRING', 'Inside sum', 10, 'tmp10')
  addi sp, sp, -8
  sd zero, (sp)
  li t0, 109
  sd t0, (sp)
  addi sp, sp, -8
  sd zero, (sp)
  li t0, 117
  sd t0, (sp)
  addi sp, sp, -8
  sd zero, (sp)
  li t0, 115
  sd t0, (sp)
  addi sp, sp, -8
  sd zero, (sp)
  li t0, 32
  sd t0, (sp)
  addi sp, sp, -8
  sd zero, (sp)
  li t0, 101
  sd t0, (sp)
  addi sp, sp, -8
  sd zero, (sp)
  li t0, 100
  sd t0, (sp)
  addi sp, sp, -8
  sd zero, (sp)
  li t0, 105
  sd t0, (sp)
  addi sp, sp, -8
  sd zero, (sp)
  li t0, 115
  sd t0, (sp)
  addi sp, sp, -8
  sd zero, (sp)
  li t0, 110
  sd t0, (sp)
  addi sp, sp, -8
  sd zero, (sp)
  li t0, 73
  sd t0, (sp)
  mv a1, sp
  li a0, 10
  call __init_string__
  addi sp, sp, 80
  sd a0, 24(sp)
		#('PRINT', 'NULL', 'STRING', 'tmp10')
  ld a0, 24(sp)
  addi sp, sp, -8
  sd a0, 0(sp)
  call __string_print__
  ld a0, 0(sp)
  addi sp, sp, 8
		#('LABEL', 'NULL', 'NULL', 'L0:')
L0:
		#('IF<', 'i', 'z', 'L1')
  ld t0, 40(sp)
  ld t1, 16(sp)
  blt t0, t1, L1
		#('GOTO', 'NULL', 'NULL', 'L2')
  j L2
		#('LABEL', 'NULL', 'NULL', 'L1:')
L1:
		#('PRINT', 'NULL', 'NULL', 'i')
  ld a0, 40(sp)
  addi sp, sp, -8
  sd a0, 0(sp)
  call __print_helper__
  ld a0, 0(sp)
  addi sp, sp, 8
		#('OP+', 'i', '1', 'tmp12')
  ld t0, 40(sp)
  li t1, 1
  add t0, t0, t1
  sd t0, 56(sp)
		#('COPY', 'tmp12', 'NULL', 'i')
  ld t0, 56(sp)
  sd t0, 40(sp)
		#('GOTO', 'NULL', 'NULL', 'L0')
  j L0
		#('LABEL', 'NULL', 'NULL', 'L2:')
L2:
		#('RETURN', 'NULL', 'NULL', 'x')
  ld a0, 0(sp)
		#('GOTO', 'NULL', 'NULL', 'sum_end')
  j sum_end
		#('LABEL', 'NULL', 'NULL', 'sum_end:')
sum_end:
		#('FUNPOP', 3, 'NULL', 'env0')
  ld ra, 64(sp)
  addi sp, sp, 72
  jr ra
		#('LABEL', 'NULL', 'NULL', 'factorial:')
factorial:
		#('FUNPUSH', 1, 'NULL', 'env1')
  addi sp, sp, -32
sd a0, 16(sp)
  sd ra, 24(sp)
		#('CMP==', 'n', '1', 'tmp13')
  ld t0, 16(sp)
  li t1, 1
  beq t0, t1, true0
  li t2, 0
true0:
  li t2, 1
  sd t2, 8(sp)
		#('IF==', 'n', '1', 'L3')
  ld t0, 16(sp)
  li t1, 1
  beq t0, t1, L3
		#('GOTO', 'NULL', 'NULL', 'L4')
  j L4
		#('LABEL', 'NULL', 'NULL', 'L3:')
L3:
		#('PUSH', 'NULL', 'NULL', 'env2')
  addi sp, sp, -0
		#('RETURN', 'NULL', 'NULL', 'n')
  ld a0, 16(sp)
		#('POP', 'NULL', 'NULL', 'env2')
  addi sp, sp, 0
		#('GOTO', 'NULL', 'NULL', 'factorial_end')
  j factorial_end
		#('GOTO', 'NULL', 'NULL', 'L5')
  j L5
		#('LABEL', 'NULL', 'NULL', 'L4:')
L4:
		#('PUSH', 'NULL', 'NULL', 'env3')
  addi sp, sp, -24
		#('OP-', 'n', '1', 'tmp15')
  ld t0, 40(sp)
  li t1, 1
  sub t0, t0, t1
  sd t0, 0(sp)
		#('PARAM', 0, 'NULL', 'tmp15')
  ld a0, 0(sp)
		#('CALL', 'tmp14', 1, 'factorial')
  jal factorial
  sd a0, 16(sp)
		#('OP*', 'n', 'tmp14', 'tmp16')
  ld t0, 40(sp)
  ld t1, 16(sp)
  mul t0, t0, t1
  sd t0, 8(sp)
		#('RETURN', 'NULL', 'NULL', 'tmp16')
  ld a0, 8(sp)
		#('POP', 'NULL', 'NULL', 'env3')
  addi sp, sp, 24
		#('GOTO', 'NULL', 'NULL', 'factorial_end')
  j factorial_end
		#('LABEL', 'NULL', 'NULL', 'L5:')
L5:
		#('LABEL', 'NULL', 'NULL', 'factorial_end:')
factorial_end:
		#('FUNPOP', 1, 'NULL', 'env1')
  ld ra, 24(sp)
  addi sp, sp, 32
  jr ra
		#('LABEL', 'NULL', 'NULL', 'fib:')
fib:
		#('FUNPUSH', 1, 'NULL', 'env4')
  addi sp, sp, -72
sd a0, 8(sp)
  sd ra, 64(sp)
		#('CMP<=', 'n', '1', 'tmp17')
  ld t0, 8(sp)
  li t1, 1
  slt t2, t1, t0
  xori t2, t2, 1
  sd t2, 40(sp)
		#('IF<=', 'n', '1', 'L6')
  ld t0, 8(sp)
  li t1, 1
  ble t0, t1, L6
		#('GOTO', 'NULL', 'NULL', 'L7')
  j L7
		#('LABEL', 'NULL', 'NULL', 'L6:')
L6:
		#('PUSH', 'NULL', 'NULL', 'env5')
  addi sp, sp, -0
		#('RETURN', 'NULL', 'NULL', 'n')
  ld a0, 8(sp)
		#('POP', 'NULL', 'NULL', 'env5')
  addi sp, sp, 0
		#('GOTO', 'NULL', 'NULL', 'fib_end')
  j fib_end
		#('LABEL', 'NULL', 'NULL', 'L7:')
L7:
		#('OP-', 'n', '1', 'tmp19')
  ld t0, 8(sp)
  li t1, 1
  sub t0, t0, t1
  sd t0, 24(sp)
		#('PARAM', 0, 'NULL', 'tmp19')
  ld a0, 24(sp)
		#('CALL', 'tmp18', 1, 'fib')
  jal fib
  sd a0, 56(sp)
		#('OP-', 'n', '2', 'tmp21')
  ld t0, 8(sp)
  li t1, 2
  sub t0, t0, t1
  sd t0, 0(sp)
		#('PARAM', 0, 'NULL', 'tmp21')
  ld a0, 0(sp)
		#('CALL', 'tmp20', 1, 'fib')
  jal fib
  sd a0, 48(sp)
		#('OP+', 'tmp18', 'tmp20', 'tmp22')
  ld t0, 56(sp)
  ld t1, 48(sp)
  add t0, t0, t1
  sd t0, 16(sp)
		#('RETURN', 'NULL', 'NULL', 'tmp22')
  ld a0, 16(sp)
		#('GOTO', 'NULL', 'NULL', 'fib_end')
  j fib_end
		#('LABEL', 'NULL', 'NULL', 'fib_end:')
fib_end:
		#('FUNPOP', 1, 'NULL', 'env4')
  ld ra, 64(sp)
  addi sp, sp, 72
  jr ra
