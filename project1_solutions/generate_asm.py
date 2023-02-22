import sys
import translate
import assembly_generator

# def strip_br_extension(strr):
#     return strr if not strr.endswith(".br") else strr[:-3]
# 
# def il_instr_to_str(il_instr):
#     return il_instr[0]+" "+", ".join([str(elem) for elem in il_instr[1:] if elem is not None])


# Get TAC
code, places = translate.main(sys.argv[1])
# New
# code, places = translate_new.main(sys.argv[1])

stack_size = len(places)*8+8
relative_addr_table = {place:addr for (place, addr) in zip(places,range(0,stack_size-8,8))}

def gen():
    print("==============================================")
    print("Inside generate_asm.py to generate assembly")
    print(stack_size)
    print(relative_addr_table)
    print()

    text_section_prologue = f'''  .global main
      .text
      .align 2
    main:
      addi sp, sp, -{stack_size}
      sd ra, {stack_size-8}(sp)
    '''

    asm_file = open('code.s', 'w')
    asm_file.write(text_section_prologue)

    asm_generator = assembly_generator.AssemblyGenerator(relative_addr_table)

    print("Instructions")
    for instr in code:
        # turn each instr to assembly
        print(instr)
        asm_file.write('\t\t#' + instr+'\n')
        asm_file.write(asm_generator.instr_to_asm(instr))

    text_section_epilogue = f'''        # Epilogue
      ld ra, {stack_size-8}(sp)
      addi sp, sp, {stack_size}
      mv a0, zero
      ret
    '''
    asm_file.write(text_section_epilogue)
    asm_file.close()

if sys.argv[2] == '1':
    gen()
