import sys
import translate_new
import asm_new

code, envs = translate_new.main(sys.argv[1])

relative_addr_tables = dict()


init_stack_size = -1

risc_regs = [f'a{i}' for i in range(0,8)]

for k,v in envs.items():
    # places = v.places
    # stack_size = len(places)*8+8
    stack_size = len(v.places)*8
    if k == 'global':
        # +8 cuz of ra
        init_stack_size = stack_size + 8
        v.stack_size = init_stack_size
    else:
        if v.func_name != '':
            v.stack_size = stack_size + 8
        else:
            v.stack_size = stack_size
    v.places = {place:str(addr) for (place, addr) in zip(v.places,range(0,stack_size,8))}
    # print(v.places)
    # for key, val in v.places.items():
        # if key in v.fun_params:
            # v.places[key] = risc_regs.pop(0)
    relative_addr_tables[k] = v

print("==============================================")
print("Inside generate_asm.py to generate assembly")
print(init_stack_size)
print(relative_addr_tables)
print()

def gen():
    global code, places

    text_section_prologue = f'''  .global main
      .text
      .align 2
    main:
      addi sp, sp, -{init_stack_size}
      sd ra, {init_stack_size-8}(sp)
    '''

    asm_file = open('code.s', 'w')
    asm_file.write(text_section_prologue)

    asm_generator = asm_new.AssemblyGenerator(relative_addr_tables, init_stack_size)

    # print(places)
    print("Instructions")
    for instr in code:
        # turn each instr to assembly
        print(instr)
        asm_file.write('\t\t#' + str(instr) +'\n')
        asm_file.write(asm_generator.instr_to_asm(instr))

    text_section_epilogue = ''
    asm_file.write(text_section_epilogue)
    asm_file.close()

if sys.argv[2] == '1':
    gen()
