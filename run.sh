#!/usr/bin/env bash

python3 asmr.py ${1} 1
riscv64-unknown-linux-gnu-gcc -march=rv64gcv -static c_helper.c v_helper.s code.s -o main
