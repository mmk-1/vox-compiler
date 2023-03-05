import re

NULL = 'NULL'
class AssemblyGenerator:
    def __init__(self, relative_addr_table, init_stack_size):
        self.relative_addr_table = relative_addr_table
        self.parent = ''
        self.current_scope = 'global'
        self.sp_extra_offset = 0
        self.set_label_cnt = -1
        # self.is_func = False
        # self.arg_cnt = 0
        self.init_stack_size = init_stack_size

        self.risc_regs = [f'a{x}' for x in range(0,8)]
    
    def instr_to_asm(self, instr : tuple):
        if instr[0] == 'EPILOGUE':
            asm = [f'  ld ra, {self.init_stack_size-8}(sp)',
                   f'  addi sp, sp, {self.init_stack_size}',
                   f'  mv a0, zero',
                   f'  ret']
            return '\n'.join(asm)+'\n'
        elif instr[0] == 'LABEL':
            return instr[-1].strip() +'\n'
        elif re.match(r'IF(>|>=|==|<|<=|!=|_)', instr[0]):
            return self.IF_to_asm(instr)
        elif re.match(r'CMP(>|>=|==|<|<=|!=)', instr[0]):
            return self.CMP_to_asm(instr)
        elif instr[0] == 'NOT':
            return self.NOT_to_asm(instr)
        elif instr[0] == 'PUSH':
            return self.PUSH_to_asm(instr)
        elif instr[0] == 'POP':
            return self.POP_to_asm(instr)
        elif instr[0] == 'UMinus':
            return self.UMinus_to_asm(instr)
        elif instr[0] == 'GOTO':
            return self.GOTO_to_asm(instr)
        elif re.match(r'OP(\+|\*|-|/)', instr[0]):
            return self.OP_to_asm(instr);
        elif instr[0] == 'CALL':
            return self.CALL_to_asm(instr)
        elif instr[0] == 'PARAM':
            return self.PARAM_to_asm(instr)
        elif instr[0] == 'COPY':
            return self.COPY_to_asm(instr)
        elif instr[0] == 'PRINT':
            return self.PRINT_to_asm(instr)
        elif instr[0] == 'RETURN':
            return self.RETURN_to_asm(instr)
        elif instr[0] == 'FUNPUSH':
            return self.FUNPUSH_to_asm(instr)
        elif instr[0] == 'FUNPOP':
            return self.FUNPOP_to_asm(instr)
        elif instr[0] == 'STRING':
            return self.STRING_to_asm(instr)
        elif instr[0] == 'VECTOR':
            return self.VECTOR_to_asm(instr)
        elif instr[0] == 'ENDVECTOR':
            return self.ENDVECTOR_to_asm(instr)
        elif re.match(r'VECTOROP(\+|\*|-|/)', instr[0]):
            return self.VECTOROP_to_asm(instr)
        else:
            # print("ADASDASD" + str(instr))
            return f'ERROR! Unknown IL {instr}'

    def string_to_ascii(self, string):
        return [ord(c) for c in string]
    
    def VECTOROP_to_asm(self, instr):
        op_mapping = {
            '+': 'add',
            '-':'sub',
            '/':'div',
            '*':'mul'
        }

        op = instr[0].split('VECTOROP')[-1]
        left = instr[1]
        right = instr[2]

        v1 = self._value_addr(left)
        v2 = self._value_addr(right)

        n = instr[-2]
        result = instr[-1]
        result = self._value_addr(result)
        
        # a0 -> v1
        # a1 -> v2
        # a2 -> result
        # a3 -> size
        asm = [f'  ld a0, 8+{v1}',
               f'  ld a1, 8+{v2}',
               f'  ld a2, 8+{result}',
               f'  li a3, {n}']

        asm.extend([
               f'  addi sp, sp, -32',
               f'  sd a0, 0(sp)',
               f'  call __v_add__',
               f'  ld a0, 0(sp)',
               f'  addi sp, sp, 32'])

        return '\n'.join(asm)+'\n'


    def VECTOR_to_asm(self, instr):
        value = instr[1]
        i = instr[2]
        to = instr[3]
        to = self._value_addr(to)
        if value.isdigit():
            asm = [f'  addi sp, sp, -8',
                   f'  sd zero, (sp)',
                   f'  li t0, {value}',
                   f'  sd t0, (sp)']
        else:
            value = self._value_addr(value)
            # Multiply by offset
            value = int(value.split('(sp)')[0]) + ((i + 1) * 8)
            value = f'{value}(sp)'
            asm = [f'  addi sp, sp, -8',
                   f'  sd zero, (sp)',
                   f'  ld t0, {value}',
                   f'  sd t0, (sp)']
        return '\n'.join(asm)+'\n'

    def ENDVECTOR_to_asm(self, instr):
        n = instr[2]
        to = instr[-1]
        to = self._value_addr(to)
        asm = [
            f'  mv a1, sp',
            f'  li a0, {n}',
            f'  call __init_string__',
            f'  addi sp, sp, {n * 8}',
            f'  sd a0, {to}']
        return '\n'.join(asm)+'\n'

    def STRING_to_asm(self, instr):
        char_list = self.string_to_ascii(instr[1])
        char_list.reverse()
        n = instr[2]
        to = instr[3]
        to = self._value_addr(to)

        asm = list()
        for c in char_list:
            asm.extend([f'  addi sp, sp, -8',
                   f'  sd zero, (sp)',
                   f'  li t0, {c}',
                   f'  sd t0, (sp)'])
        asm.extend([
            f'  mv a1, sp',
            f'  li a0, {n}',
            f'  call __init_string__',
            f'  addi sp, sp, {n * 8}',
            f'  sd a0, {to}'])
            

        return '\n'.join(asm)+'\n'

    def RETURN_to_asm(self, instr):
        load = instr[-1]
        if load.isdigit():
            asm = [f'  li a0, {load}']
        else:
            load = self._value_addr(load)
            asm = [f'  ld a0, {load}']

        return '\n'.join(asm)+'\n'

    def PRINT_to_asm(self, instr):
        addr = instr[-1]
        
        if instr[2].startswith('STRING'):
            addr = self._value_addr(addr)
            asm = [f'  ld a0, {addr}',
                   f'  addi sp, sp, -8',
                   f'  sd a0, 0(sp)',
                   f'  call __string_print__',
                   f'  ld a0, 0(sp)',
                   f'  addi sp, sp, 8'] # shrink stack by 8 (only one argument to pass)
        elif instr[2] == 'VECTOR':
            addr = self._value_addr(addr)
            asm = [f'  ld a0, {addr}',
                   f'  addi sp, sp, -8',
                   f'  sd a0, 0(sp)',
                   f'  call __vector_print__',
                   f'  ld a0, 0(sp)',
                   f'  addi sp, sp, 8'] # shrink stack by 8 (only one argument to pass)

        elif addr.isdigit():
            asm = [f'  li a0, {addr}',
                   f'  addi sp, sp, -8',
                   f'  sd a0, 0(sp)',
                   f'  call __print_helper__',
                   f'  ld a0, 0(sp)',
                   f'  addi sp, sp, 8'] # shrink stack by 8 (only one argument to pass)
        else:
            from_mem = self._value_addr(addr)
            asm = [f'  ld a0, {from_mem}',
                   f'  addi sp, sp, -8',
                   f'  sd a0, 0(sp)',
                   f'  call __print_helper__',
                   f'  ld a0, 0(sp)',
                   f'  addi sp, sp, 8'] # shrink stack by 8 (only one argument to pass)
        return '\n'.join(asm)+'\n'

    def NOT_to_asm(self, instr):
        fromm = instr[-2]
        to = instr[-1]
        to = self._value_addr(to)
        if not fromm.isdigit():
            fromm = self._value_addr(fromm)
            asm = [ f'  ld t0, {fromm}',
                    f'  xori t1, t0, 1',
                    f'  sd t1, {to}']
        else:
            asm = [ f'  li t0, {fromm}',
                    f'  xori t1, t0, 1',
                    f'  sd t1, {to}']

        return '\n'.join(asm)+'\n'

    def UMinus_to_asm(self,instr):
        fromm = instr[-2]
        to = instr[-1]
        to = self._value_addr(to)
        if not fromm.isdigit():
            fromm = self._value_addr(fromm)
            asm = [ f'  ld t0, {fromm}',
                    f'  neg t1, t0',
                    f'  sd t1, {to}']
        else:
            asm = [ f'  li t0, {fromm}',
                    f'  neg t1, t0',
                    f'  sd t1, {to}']

        return '\n'.join(asm)+'\n'

    def FUNPUSH_to_asm(self, instr):
        # Calculate how much to allocate for stack
        new_env = instr[-1]

        n = 8 * len(self.relative_addr_table[new_env].places) 
        # We will save 3 callee saved registers
        self.current_scope = new_env
        # n = 3 * 8 + n
        # For ra
        n += 8
        self.sp_extra_offset += n

        len_params = len(self.relative_addr_table[new_env].fun_params)
        
        asm = [f'  addi sp, sp, -{n}']
        i = 0
        copy = self.relative_addr_table[new_env].fun_params.copy()
        # while (len_params != 0):
            # param = copy.pop()
            # reg = self.risc_regs[i]
            # get_addr = self._value_addr(param)
            # asm.append(f'sd {reg}, {get_addr}')
            # len_params -= 1
            # i += 1
               # f'  sd s0, {n - 8}(sp)',
               # f'  sd s1, {n - 16}(sp)',
               # f'  mv s0, a0',
               # f'  mv s1, a1'
        for param, register in copy.items():
            get_addr = self._value_addr(param)
            asm.append(f'sd {register}, {get_addr}')
        
        asm.append(f'  sd ra, {n - 8}(sp)')
        return '\n'.join(asm)+'\n'

    def PUSH_to_asm(self, instr):
        # Calculate how much to allocate for stack
        new_env = instr[-1]
        n = 8 * len(self.relative_addr_table[new_env].places)
        # self.parent = self.current_scope
        self.current_scope = new_env
        self.sp_extra_offset += n
        asm = [f'  addi sp, sp, -{n}'] # Allocate

        return '\n'.join(asm)+'\n'

    def POP_to_asm(self, instr):
        new_env = instr[-1]
        n = 8 * len(self.relative_addr_table[new_env].places)

        asm = [f'  addi sp, sp, {n}'] # Deallocate

        self.current_scope = self.relative_addr_table[new_env].parent
        self.sp_extra_offset -= n

        return '\n'.join(asm)+'\n'

    def FUNPOP_to_asm(self, instr):
        new_env = instr[-1]
        n = 8 * len(self.relative_addr_table[new_env].places)
        # n = 3 * 8 + n
        n += 8
        # param_len = len(self.relative_addr_table[new_env].fun_params)
        asm = [#f'  mv a0, s0',
               #f'  mv a1, s1',
               # f'  ld s0, {n - 8}(sp)',
               # f'  ld s1, {n - 16}(sp)',
               f'  ld ra, {n - 8}(sp)',
               f'  addi sp, sp, {n}',
               f'  jr ra']
        # self.arg_cnt = 0

        self.current_scope = self.relative_addr_table[new_env].parent
        self.sp_extra_offset -= n

        return '\n'.join(asm)+'\n'
        

    def CMP_to_asm(self,instr):
        # for == ???
        # for != ???

        op = instr[0].split('CMP')[-1]
        left_op = instr[1]
        right_op = instr[2]
        res = instr[-1]
        res = self._value_addr(res)

        if left_op.isdigit() and right_op.isdigit():
            asm = [ f'  li t0, {left_op}',
                    f'  li t1, {right_op}']
            tmp = self.set_operations(op)
            asm.extend(tmp)

        elif left_op.isdigit() and not right_op.isdigit():
            right_from = self._value_addr(right_op)
            asm = [ f'  li t0, {left_op}',
                    f'  ld t1, {right_from}']
            tmp = self.set_operations(op)
            asm.extend(tmp)

        elif not left_op.isdigit() and right_op.isdigit():
            left_from = self._value_addr(left_op)
            asm = [ f'  ld t0, {left_from}',
                    f'  li t1, {right_op}']
            tmp = self.set_operations(op)
            asm.extend(tmp)

        else:
            right_from = self._value_addr(right_op)
            left_from = self._value_addr(left_op)
            asm = [ f'  ld t0, {left_from}',
                    f'  ld t1, {right_from}']
            tmp = self.set_operations(op)
            asm.extend(tmp)

        # Why? Because we want to save temp
        asm.append(f'  sd t2, {res}')
        return '\n'.join(asm)+'\n'

    def IF_to_asm(self,instr):
        op_mapping = {
            "==": "beq",
            "!=": "bne",
            "<": "blt",
            "<=": "ble",
            ">": "bgt",
            ">=": "bge"
        }

        op = instr[0].split('IF')[-1]
        left_op = instr[1]
        right_op = instr[2]
        goto_label = instr[-1]

        if left_op.isdigit() and right_op.isdigit():
            asm = [ f'  li t0, {left_op}',
                    f'  li t1, {right_op}',
                    f'  {op_mapping[op]} t0, t1, {goto_label}',]
            return '\n'.join(asm)+'\n'

        elif left_op.isdigit() and not right_op.isdigit():
            right_from = self._value_addr(right_op)
            if right_from in self.risc_regs:
                asm = [ f'  li t0, {left_op}',
                        f'  mv t1, {right_from}',
                        f'  {op_mapping[op]} t0, t1, {goto_label}',]
            else:
                asm = [ f'  li t0, {left_op}',
                        f'  ld t1, {right_from}',
                        f'  {op_mapping[op]} t0, t1, {goto_label}',]
            return '\n'.join(asm)+'\n'

        elif not left_op.isdigit() and right_op.isdigit():
            left_from = self._value_addr(left_op)
            
            if left_from in self.risc_regs:
                asm = [ f'  mv t0, {left_from}',
                        f'  li t1, {right_op}',
                        f'  {op_mapping[op]} t0, t1, {goto_label}',]
            else:
                asm = [ f'  ld t0, {left_from}',
                        f'  li t1, {right_op}',
                        f'  {op_mapping[op]} t0, t1, {goto_label}',]
            return '\n'.join(asm)+'\n'

        else:
            right_from = self._value_addr(right_op)
            left_from = self._value_addr(left_op)

            if left_from in self.risc_regs and right_from in self.risc_regs:
                asm = [ f'  mv t0, {left_from}',
                        f'  mv t1, {right_from}',
                        f'  {op_mapping[op]} t0, t1, {goto_label}',]
            elif left_from in self.risc_regs and right_from not in self.risc_regs:
                asm = [ f'  mv t0, {left_from}',
                        f'  ld t1, {right_from}',
                        f'  {op_mapping[op]} t0, t1, {goto_label}',]
            elif left_from not in self.risc_regs and right_from in self.risc_regs:
                asm = [ f'  ld t0, {left_from}',
                        f'  mv t1, {right_from}',
                        f'  {op_mapping[op]} t0, t1, {goto_label}',]
            else:
                asm = [ f'  ld t0, {left_from}',
                        f'  ld t1, {right_from}',
                        f'  {op_mapping[op]} t0, t1, {goto_label}',]
            return '\n'.join(asm)+'\n'

    def GOTO_to_asm(self,il_instr):
        label = il_instr[-1]
        
        asm = [ f'  j {label}' ]

        return '\n'.join(asm)+'\n'
        
    def PARAM_to_asm(self, instr):
        # self.sp_extra_offset +=
        # self.sp_extra_offset += 16
        # asm = ['  addi sp, sp, -16']

        # if type(il_instr[1]) == int:
        #     asm.extend(['  sd zero, (sp)',
        #                f'  li t0, {il_instr[1]}',
        #                f'  sd t0, 8(sp)'])
        # else:
        #     type_addr = self._value_addr(il_instr[1])
        #     value_addr = self._value_addr(il_instr[1])
        #     asm.extend([f'  ld t0, {type_addr}',
        #                  '  sd t0, (sp)',
        #                 f'  ld t0, {value_addr}',
        #                 f'  sd t0, 8(sp)'])

        var = instr[-1]
        i = instr[1]
        if var.isdigit():
            asm = [f'  li a{i}, {var}']
        else:
            var = self._value_addr(var)
            asm = [f'  ld a{i}, {var}']
        # self.arg_cnt += 1
        return '\n'.join(asm)+'\n'


    def CALL_to_asm(self, instr):
        # asm = ['  mv a1, sp',
        #       f'  li a0, {il_instr[3]}',
        #       f'  call {il_instr[2]}',
        #       f'  addi sp, sp, {16*il_instr[3]}']
        # 
        # self.sp_extra_offset -= 16*il_instr[3]
        # 
        # if il_instr[1] is not None:
        #     type_addr = self._value_addr(il_instr[1])
        #     value_addr = self._value_addr(il_instr[1])
        #     asm.extend([f'  sd a0, {type_addr}',
        #                 f'  sd a1, {value_addr}'])
        func_label = instr[-1]
        to = instr[1]
        to = self._value_addr(to)
        asm = [f'  jal {func_label}',
               f'  sd a0, {to}']
        
        return '\n'.join(asm)+'\n'

    def COPY_to_asm(self, instr):
        arg1 = instr[-1] 
        arg2 = instr[1]

        is_string = True if instr[2] == 'STRING' else False

        # risc_regs = [f'a{x}' for x in range(0,8)]

        to_addr = self._value_addr(arg1)

        if is_string:
            arg2 = self._value_addr(arg2)
            asm = [f'  sd zero, {to_addr}',
                   f'  ld t0, {arg2}',
                   f'  sd t0, {to_addr}']
        elif arg2.isdigit():
            asm = [f'  sd zero, {to_addr}',
                   f'  li t0, {arg2}',
                   f'  sd t0, {to_addr}']
        # elif arg2 == '_RET_':
            ## store function result
            # asm = [f'  sd a0, {to_addr}']
        else:
            from_addr = self._value_addr(arg2)

            asm = [f'  ld t0, {from_addr}',
                   f'  sd t0, {to_addr}']

        
        return '\n'.join(asm)+'\n'

    def OP_to_asm(self, instr):
        # Right now it just adds but add * / - too!
        op_mapping = {
            '+': 'add',
            '-':'sub',
            '/':'div',
            '*':'mul'
        }
        # op = ''

        op = instr[0].split('OP')[-1]
        left_op = instr[1]
        right_op = instr[2]
        result = instr[-1]


        if left_op.isdigit() and right_op.isdigit():
            # get left value 
            # get right value
            # add them up
            # store into t0
            store_to = self._value_addr(result)

            asm = [f'  li t0, {left_op}',
                   f'  li t1, {right_op}',
                   f'  {op_mapping[op]} t0, t0, t1',
                   f'  sd t0, {store_to}' ]
        elif left_op.isdigit() and not right_op.isdigit():
            store_to = self._value_addr(result)
            right_from = self._value_addr(right_op)

            if right_from in self.risc_regs:
                asm = [f'  li t0, {left_op}',
                       f'  mv t1, {right_from}',
                       f'  {op_mapping[op]} t0, t0, t1',
                       f'  sd t0, {store_to}' ]
            else:
                asm = [f'  li t0, {left_op}',
                       f'  ld t1, {right_from}',
                       f'  {op_mapping[op]} t0, t0, t1',
                       f'  sd t0, {store_to}' ]
        elif right_op.isdigit() and not left_op.isdigit():
            store_to = self._value_addr(result)
            left_from = self._value_addr(left_op)

            if left_from in self.risc_regs:
                asm = [f'  mv t0, {left_from}',
                       f'  li t1, {right_op}',
                       f'  {op_mapping[op]} t0, t0, t1',
                       f'  sd t0, {store_to}' ]
            else:
                asm = [f'  ld t0, {left_from}',
                       f'  li t1, {right_op}',
                       f'  {op_mapping[op]} t0, t0, t1',
                       f'  sd t0, {store_to}' ]
        else:
            left_from = self._value_addr(left_op)
            right_from = self._value_addr(right_op)
            store_to = self._value_addr(result)


            if left_from in self.risc_regs and right_from in self.risc_regs:
                asm = [f'  mv t0, {left_from}',
                       f'  mv t1, {right_from}',
                       f'  {op_mapping[op]} t0, t0, t1',
                       f'  sd t0, {store_to}' ]
            elif left_from in self.risc_regs and right_from not in self.risc_regs:
                asm = [f'  mv t0, {left_from}',
                       f'  ld t1, {right_from}',
                       f'  {op_mapping[op]} t0, t0, t1',
                       f'  sd t0, {store_to}' ]
            elif left_from not in self.risc_regs and right_from in self.risc_regs:
                asm = [f'  ld t0, {left_from}',
                       f'  mv t1, {right_from}',
                       f'  {op_mapping[op]} t0, t0, t1',
                       f'  sd t0, {store_to}' ]
            else:
                asm = [f'  ld t0, {left_from}',
                       f'  ld t1, {right_from}',
                       f'  {op_mapping[op]} t0, t0, t1',
                       f'  sd t0, {store_to}' ]

        return '\n'.join(asm)+'\n'

    def set_operations(self, op):
        # For < -> slt
        # For > -> Flip the operands
        # For >= -> slt then xori (negate)
        # For <= -> flip slt then xori

        if op == '<':
            asm = [f'  slt t2, t0, t1',]

        elif op == '>':
            # Flipped
            asm = [f'  slt t2, t1, t0',]
        elif op == '<=':
            asm = [f'  slt t2, t1, t0',
                   f'  xori t2, t2, 1']
        elif op == '>=':
            asm = [f'  slt t2, t0, t1',
                   f'  xori t2, t2, 1']
        elif op == '==':
            goto = self.gen_set_labels()
            asm = [f'  beq t0, t1, {goto}',
                   f'  li t2, 0',
                   f'{goto}:',
                   f'  li t2, 1']
        elif op == '!=':
            goto = self.gen_set_labels()
            asm = [f'  bne t0, t1, {goto}',
                   f'  li t2, 1',
                   f'{goto}:',
                   f'  li t2, 0']

        return asm

    def gen_set_labels(self):
        self.set_label_cnt += 1
        return f'true{self.set_label_cnt}'

    def _value_addr(self, place):
        if place in self.relative_addr_table[self.current_scope].places:
            return str(self.relative_addr_table[self.current_scope].places[place])+'(sp)'
        else:
            # Not in current scope, go back to root to find
            parent = self.relative_addr_table[self.current_scope].parent
            offset = self.relative_addr_table[self.current_scope].stack_size
            while parent != '':
                if place in self.relative_addr_table[parent].places:
                    return str(offset+int(self.relative_addr_table[parent].places[place]))+'(sp)'
                parent = self.relative_addr_table[parent].parent
                offset += self.relative_addr_table[parent].stack_size

            raise Exception('Cannot find variable in parent environments ' + place)


