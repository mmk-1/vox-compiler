To run:  
1- `bash run <.vox file>`  
2- `riscv64-unknown-linux-gnu-gcc -march=rv64gcv -static c_helper.c v_helper.s code.s -o main`
  - code.s is the assembly file generated  


Issues:
- Vector operations do not work. You can only initialize and print vectors.
- Short circuting (`and` & `or` operations) doesn't work properly.

Notes:
- There are some tests available in `tests/` dir.
- Functions work (with recursion) and its tested in `tests/funcs.vox`
