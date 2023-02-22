files are in project1_solutions/ -> may need to refactor

1. write a *.vox sample code
2. use translate.py to generate its IC
3. use generate_asm.py to generate is assembly code (*.c)
4. copy assembly to docker container
5. run compiler using:
`riscv64-unknown-linux-gnu-gcc -march=rv64gcv -static hello.c strveccpy.s -o hello`




using qemu:
`qemu-riscv64 -cpu rv64,v=true,zba=true,vlen=128,vext_spec=v1.0 hello`



9. Try running it on QEMU and remote debugging with gdb at the same time from port 1234:

qemu-riscv64 -g 1234 -cpu rv64,v=true,zba=true,vlen=128,vext_spec=v1.0 hello

From another terminal:
riscv64-unknown-linux-gnu-gdb hello
(gdb) target remote :1234
(gdb)break *strveccpy
(gdb)continue
(gdb)disas
(gdb)try inspecting some registers here: $sp, $a0, $a1, $v1 ...
(gdb)stepi, and other stuff...
(gdb)quit





# Docker cmds

`docker run -dit vox` -> run docker and keep it running

`docker exec -it <container name> bash` -> start terminal in container

`docker cp foo.txt container_id:/foo.txt` -> copy from local to container  .global main

  .text
  .align 2
main:
