# Vox compiler
- This compiler is for RISC-V architecture. Dockerfile provides the environment with necessary toolchains and simulators to run programs.
- Alternatively you can install the dependencies locally -> [link](#Install RISC-V locally)

## Running
To run:  
1- `bash run <.vox file>`  
2- `riscv64-unknown-linux-gnu-gcc -march=rv64gcv -static c_helper.c v_helper.s code.s -o main`
  - code.s is the assembly file generated  

## Issues:
- Vector operations do not work. You can only initialize and print vectors.
- Short circuting (`and` & `or` operations) doesn't work properly.

## Other notes:
- There are some tests available in `tests/` dir.
- Functions work (with recursion) and its tested in `tests/funcs.vox`

## Install RISC-V locally
1. Dependencies:

`sudo apt install device-tree-compiler git wget tar build-essential libglib2.0-dev libfdt-dev libpixman-1-dev zlib1g-dev ninja-build python3 autoconf automake autotools-dev curl python3 libmpc-dev libmpfr-dev libgmp-dev gawk build-essential bison flex texinfo gperf libtool patchutils bc zlib1g-dev libexpat-dev`

2. Environment Variables:
Add these to ~/.bashrc:

`export RISCV="/opt/riscv/"`
`export PATH="${PATH}:${RISCV}bin/:${RISCV}riscv64-unknown-linux-gnu/bin/"`

2. Spike Simulator:

`git clone https://github.com/riscv-software-src/riscv-isa-sim`
`mkdir riscv-isa-sim/build`
`cd riscv-isa-sim/build`
`../configure --prefix=$RISCV`
`make`
`[sudo] make install`

3. GNU Toolchain for riscv programs configured for linux kernels - takes a very long time!:

`git clone https://github.com/riscv-collab/riscv-gnu-toolchain`
`mkdir riscv-gnu-toolchain/build`
`cd riscv-gnu-toolchain/build`
`../configure --prefix=$RISCV`
`make linux`

4. Proxy Linux Kernel:

`git clone https://github.com/riscv-software-src/riscv-pk`
`mkdir riscv-pk/build`
`cd riscv-pk/build`
`../configure --prefix=$RISCV --host=riscv64-unknown-linux-gnu`
`make`
`[sudo] make install`

5. QEMU (emulator for riscv64 user-level programs for linux):

`wget https://download.qemu.org/qemu-7.2.0-rc4.tar.xz`
`tar -xf qemu-7.2.0-rc4.tar.xz`
`mkdir qemu-7.2.0-rc4/build`
`cd mkdir qemu-7.2.0-rc4/build`
`../configure --target-list=riscv64-linux-user`
`make`
`[sudo] make install`


