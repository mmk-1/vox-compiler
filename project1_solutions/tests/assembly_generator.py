import re

class AssemblyGenerator:
    def __init__(self, relative_addr_table):
        self.relative_addr_table = relative_addr_table
        self.parent = ''
        self.current_scope = 'global'
        self.sp_extra_offset = 0
    
    def instr_to_asm(self, instr):
        if instr.startswith('L'):
            return instr.strip() +'\n'
        if instr.startswith('IF'):
            return self.IF_to_asm(instr)
        if instr.startswith('GOTO'):
            return self.GOTO_to_asm(instr)
        if instr.startswith('OP'):
            return self.OP_to_asm(instr);
        if instr[0] == 'CALL':
            return self.CALL_to_asm(instr)
        if instr[0] == 'PARAM':
            return self.PARAM_to_asm(instr)
        if instr.startswith('COPY'):
            return self.COPY_to_asm(instr)
        else:
            return f'ERROR! Unknown IL {instr}'

    def IF_to_asm(self,instr):
        op_mapping = {
            "==": "beq",
            "!=": "bne",
            "<": "blt",
            "<=": "ble",
            ">": "bgt",
            ">=": "bge"
        }

        match = re.search(r"IF (\w+|\d+) (>=|<=|>|<|==|!=) (\w+|\d+) GOTO (\w+)", instr)
        if match:
            left_op = match.group(1)
            op = match.group(2)
            right_op = match.group(3)
            label = match.group(4)
            print(left_op, op, right_op, label)
        else:
            raise Exception("No match found")
        
        if left_op.isdigit() and right_op.isdigit():
            pass
        elif left_op.isdigit() and not right_op.isdigit():
            pass
        elif not left_op.isdigit() and right_op.isdigit():
            left_from = self._value_addr(left_op)

            asm = [ f'  ld t0, {left_from}',
                    f'  li t1, {right_op}',
                    f'  {op_mapping[op]} t0, t1, {label}',]

            return '\n'.join(asm)+'\n'
        else:
            pass

    def GOTO_to_asm(self,il_instr):
        match = re.search(r"GOTO ([\w+][\d+])", il_instr)
        if match:
            label = match.group(1)
            # print(left_op, operator, b, label)
        else:
            raise Exception("No match found")
        asm = [ f'  j {label}' ]

        return '\n'.join(asm)+'\n'
        
    def PARAM_to_asm(self, il_instr):
        self.sp_extra_offset += 16
        asm = ['  addi sp, sp, -16']

        if type(il_instr[1]) == int:
            asm.extend(['  sd zero, (sp)',
                       f'  li t0, {il_instr[1]}',
                       f'  sd t0, 8(sp)'])
        else:
            type_addr = self._value_addr(il_instr[1])
            value_addr = self._value_addr(il_instr[1])
            asm.extend([f'  ld t0, {type_addr}',
                         '  sd t0, (sp)',
                        f'  ld t0, {value_addr}',
                        f'  sd t0, 8(sp)'])
        
        return '\n'.join(asm)+'\n'


    def CALL_to_asm(self, il_instr):
        asm = ['  mv a1, sp',
              f'  li a0, {il_instr[3]}',
              f'  call {il_instr[2]}',
              f'  addi sp, sp, {16*il_instr[3]}']
        
        self.sp_extra_offset -= 16*il_instr[3]
        
        if il_instr[1] is not None:
            type_addr = self._value_addr(il_instr[1])
            value_addr = self._value_addr(il_instr[1])
            asm.extend([f'  sd a0, {type_addr}',
                        f'  sd a1, {value_addr}'])
        
        return '\n'.join(asm)+'\n'

    def COPY_to_asm(self, instr):
        match = re.search(r"COPY ([\w+|\d+]),([\w+|\d+])", instr)
        if match:
            arg1 = match.group(1)
            arg2 = match.group(2)
        else:
            raise Exception("No match found")

        to_addr = self._value_addr(arg1)

        if arg2.isdigit():
            asm = [f'  sd zero, {to_addr}',
                   f'  li t0, {arg2}',
                   f'  sd t0, {to_addr}']
        else:
            from_addr = self._value_addr(arg1)

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

        match = re.search(r"OP (\w+) = (\w+|\d+) (\+|\*|-|/) (\w+|\d+)", instr)
        if match:
            result = match.group(1)
            left_op = match.group(2)
            op = match.group(3)
            right_op = match.group(4)
        else:
            raise Exception("No match found")

        if left_op.isdigit() and right_op.isdigit():
            # get left value 
            # get right value
            # add them up
            # store into t0
            store_to = self._value_addr(result)

            asm = [f'  li t0, {left_op}',
                   f'  li t1, {right_op}',
                   f'  {op_mapping[op]} t0, t1, t0',
                   f'  sd t0, {store_to}' ]
        elif left_op.isdigit() and not right_op.isdigit():
            store_to = self._value_addr(result)
            right_from = self._value_addr(right_op)

            asm = [f'  li t0, {left_op}',
                   f'  ld t1, {right_from}',
                   f'  {op_mapping[op]} t0, t1, t0',
                   f'  sd t0, {store_to}' ]
        elif right_op.isdigit() and not left_op.isdigit():
            store_to = self._value_addr(result)
            left_from = self._value_addr(left_op)

            asm = [f'  li t0, {right_op}',
                   f'  ld t1, {left_from}',
                   f'  {op_mapping[op]} t0, t1, t0',
                   f'  sd t0, {store_to}' ]
        else:
            left_from = self._value_addr(left_op)
            right_from = self._value_addr(right_op)
            store_to = self._value_addr(result)
            # Get value from memory operand left
            # Get value from memory operand right
            # add them up
            # store them into assgn
            asm = [f'  ld t0, {left_from}',
                   f'  ld t1, {right_from}',
                   f'  {op_mapping[op]} t0, t1, t0',
                   f'  sd t0, {store_to}' ]

        return '\n'.join(asm)+'\n'


    def _value_addr(self, place):
        return str(self.sp_extra_offset+self.relative_addr_table[place])+'(sp)'

