from os import wait
import re
from ast_tools import *
from misc import *


label_id_count = -1
def generate_tmp_label():
    global label_id_count
    label_id_count += 1
    return f'L{label_id_count}'

tmp_var_id_count = -1
def generate_tmp_var():
    global tmp_var_id_count
    tmp_var_id_count += 1
    return f'tmp{tmp_var_id_count}'

env_cntr = -1
def generate_env():
    global env_cntr
    env_cntr += 1
    return f'env{env_cntr}'

NULL = 'NULL'

PLACEHOLDER = 'PLACEHOLDER'

risc_regs = [f'a{i}' for i in range(0,8)]

envs = dict()
function_places = set()
current_scope = 'global'
strings = set()

class Environment:
    def __init__(self, scope_name : str, parent : str):
        self.scope_name = scope_name
        self.parent = parent
        # self.var_decls = list()
        self.places = set()
        self.fun_params = dict()
        self.func_name = ''
        self.stack_size = 0
        self.string_table = set()
        self.vector_table = dict()

    def __repr__(self) -> str:
        return f'({self.scope_name}, {self.parent}, {self.places}, {self.fun_params}, {self.stack_size})'

def block_handler(src, instr_list, func_obj, is_func):
    global current_scope
    global envs
    
    new_env_name = generate_env()
    new_scope = Environment(new_env_name, current_scope)
    envs[new_env_name] = new_scope
    # new_scope.parent = current_scope
    current_scope = new_env_name

    if is_func:
        envs[current_scope].func_name = func_obj.identifier.name
        envs[current_scope].places.add(func_obj.identifier.name)
        params = func_obj.params
    
    if is_func == True:
        n = len(params)
        instr_list.append((f'FUNPUSH', n, NULL, current_scope))
    else:
        instr_list.append((f'PUSH', NULL, NULL, current_scope))

    for v in src.var_decls:
        if v.initializer != None:
            translate(v, instr_list)
        else:
            envs[current_scope].places.add(v.identifier.name)
    
    if is_func == True:
        i = 0
        for p in params:
            envs[current_scope].places.add(p.name)
            envs[current_scope].fun_params[p.name] = risc_regs[i]
            i += 1

    # stmts = list()
    for s in src.statements:
#        print(s)
        translate(s, instr_list)
        # print(instr_list)

    if is_func == True:
        n = len(params)
        instr_list.append((f'LABEL', NULL, NULL, envs[current_scope].func_name + '_end:'))
        instr_list.append((f'FUNPOP', n, NULL, current_scope))
    else:
        if instr_list[-1][0] == 'GOTO' and instr_list[-1][-1] != '':
            temp = instr_list.pop()
            instr_list.append((f'POP', NULL, NULL, current_scope))
            instr_list.append(temp)
        else:
            instr_list.append((f'POP', NULL, NULL, current_scope))
    current_scope = envs[current_scope].parent


def lbinary_handler(src, instr_list, t_list, f_list):
    op = src.op
    l = src.left
    r = src.right

    # code = NULL

    if type(l) == LBinary:
        lbinary_handler(l, instr_list, t_list, f_list)
    else:
        l = translate(l, instr_list)
        if type(l) == tuple and len(l) == 1:
            pass
        elif l[0].startswith('LPrimary'):
            instr_list.append(l)
        elif l[0].startswith('CMP'):
            instr_list.append(l)
            # if op == 'or':
            #     t_list.append()
            # else:
            #     f_list.append(r)
            

    if type(r) == LBinary:
        lbinary_handler(r, instr_list, t_list, f_list)
    else:
        r = translate(r, instr_list)
        if type(r) == tuple and len(r) == 1:
            pass
        elif r[0].startswith('LPrimary'):
            instr_list.append(r)
        elif r[0].startswith('CMP'):
            instr_list.append(r)
            # if op == 'or':
            #     t_list.append(r)
            # else:
            #     f_list.append(r)






# all_instr = list()
def translate(src, instr_list):
    global envs
    global current_scope
    #global all_instr
    if type(src) == VarDecl:
        id = src.identifier.name
        envs[current_scope].places.add(src.identifier.name)

        if type(src.initializer) == type([]):
            # Vector!
            tmp_var = generate_tmp_var()
            envs[current_scope].places.add(tmp_var)
            i = 0
            n = len(src.initializer)
            ll = reversed(src.initializer)
            vector_stmts = list()
            for expr in ll:
                temp = list()
                val = translate(expr, temp)
                # print(temp)
                instr_list.extend(temp)
                if len(val) == 1: # ALiteral or LLiteral
                    vector_stmts.append(('VECTOR', val[0], i, tmp_var))
                else:
                    vector_stmts.append(('VECTOR', val[-1], i, tmp_var))
                i += 1
            # if len(val) == 1: # ALiteral or LLiteral
            instr_list.extend(vector_stmts)
            code = ('ENDVECTOR', NULL, n, tmp_var)
            instr_list.append(code)
            code = ('COPY', tmp_var, NULL, id)
            instr_list.append(code)

            envs[current_scope].vector_table[id] = n
                
        elif type(src.initializer != None): 
            val = translate(src.initializer, instr_list)
            if len(val) == 1: # ALiteral or LLiteral
                code = ('COPY', val[0], NULL, id)
                instr_list.append(code)
            elif val[0] == 'STRING':
                code = ('COPY', val[-1], 'STRING', id)
                envs[current_scope].string_table.add(id)
                instr_list.append(code)
            elif type(val) == tuple and val[0].startswith('CMP'):
                # If comparision
                # Unlike ABinary Comparison doesn't add to instr_list directly
                # So we must handle here
                instr_list.append(val)
                code = ('COPY', val[-1], NULL, id)
                instr_list.append(code)
            else: 
                code = ('COPY', val[-1], NULL, id)
                instr_list.append(code)
        
    elif type(src) == Variable:
        # envs[current_scope].places.add(src.identifier.name)
        code = (src.identifier.name,)
    elif type(src) == LBinary:

        lbinary_handler(src, instr_list, [], [])
        code = NULL

    elif type(src) == ALiteral:
        code = (str(int(src.value)),)

    elif type(src) == SLiteral:
        id = generate_tmp_var()
        envs[current_scope].places.add(id)
        code = ("STRING", src.value, len(src.value), id)
        instr_list.append(code)
    elif type(src) == LPrimary:
        # For now just consider Variable
        code = ('LPrimary', translate(src.primary, instr_list)[0])

    elif type(src) == AUMinus:
        # - ()
        id = generate_tmp_var()
        envs[current_scope].places.add(id)
        r = translate(src.right, instr_list)
        # print()
        code = NULL
        if type(r) == ALiteral:
            code = ('UMinus', NULL, r, id)
        elif type(r) == tuple and r[0].startswith('OP'):
            code = ('UMinus', NULL, r[-1], id)
        elif type(r) == tuple:
            code = ('UMinus', NULL, r[0], id)
        instr_list.append(code)

    elif type(src) == LLiteral:
        if src.value == True:
            code = tuple(str(1))
        else:
            code = tuple(str(0))
    elif type(src) == LNot:
        # print(src.right)
        id = generate_tmp_var()
        envs[current_scope].places.add(id)
        r = translate(src.right, instr_list)
        code = NULL
        if r[0].startswith('LPrimary'):
            code = ('NOT', NULL, r[-1], id)
        elif r[0].startswith('CMP'):
            instr_list.append(r)
            code = ('NOT', NULL, r[-1], id)
        elif len(r) == 1:
            code = ('NOT', NULL, r[0], id)
        instr_list.append(code)
        # to save the trouble also store in mem!
        # This is only useful for if statements
        # It creates redundancy for normal expressions
        # instr_list.append(('COPY', id, NULL, id))

    elif type(src) == Assign:
        # ('COPY', value, id)
        id = src.identifier.name
        # envs[current_scope].places.add(src.identifier.name)
        val = translate(src.expr, instr_list)
        # print(val)
        # Do we need the NULL?
        # print(val)
        if len(val) == 1: # ALiteral or LLiteral
            code = ('COPY', val[0], NULL, id)
            instr_list.append(code)
        elif val[0] == 'STRING':
            # Get from heap 
            code = ('COPY', val[-1], 'STRING', id)
            envs[current_scope].string_table.add(id)
            instr_list.append(code)
        elif type(val) == tuple and val[0].startswith('CMP'):
            # If comparision
            # Unlike ABinary Comparison doesn't add to instr_list directly
            # So we must handle here
            instr_list.append(val)
            code = ('COPY', val[-1], NULL, id)
            instr_list.append(code)
        elif type(val) == tuple and val[0].startswith('CALL'):
            # val = (val[0], id, val[2], val[-1])
            code = ('COPY', val[1], NULL, id)
            # Remove and replace with new one
            instr_list.append(code)
        else: 
            code = ('COPY', val[-1], NULL, id)
            instr_list.append(code)
    elif type(src) == ABinary:
        # ('OP', left, right, result)
        l = translate(src.left, instr_list)
        r = translate(src.right, instr_list)

        op = src.op
        id = generate_tmp_var()
        envs[current_scope].places.add(id)
        
        if len(l) == 1 and len(r) == 1: # If literal or var

            if l[0] in envs[current_scope].vector_table.keys():
                n = envs[current_scope].vector_table[l[0]]
                code = (f'VECTOROP{op}', l[0], r[0], n, id)
            else:
                code = (f'OP{op}', l[0], r[0], id)
            instr_list.append(code)
        elif len(l) == 1 and len(r) > 1:
            if r[0].startswith('CALL'):
                code = (f'OP{op}', l[0], r[1], id)
            else:
                code = (f'OP{op}', l[0], r[-1], id)
            instr_list.append(code)
        elif len(l) > 1 and len(r) == 1:
            if r[0].startswith('CALL'):
                code = (f'OP{op}', l[1], r[0], id)
            else:
                code = (f'OP{op}', l[-1], r[0], id)
            instr_list.append(code)
        else: # If nexted ops
            if r[0].startswith('CALL'):
                code = (f'OP{op}', l[1], r[1], id)
            else:
                code = (f'OP{op}', l[-1], r[-1], id)
            instr_list.append(code)

    elif type(src) == Comparison:
        l = translate(src.left, instr_list)
        r = translate(src.right, instr_list)
        id = generate_tmp_var()
        envs[current_scope].places.add(id)
        op = src.op
        if type(l) == tuple and len(l) == 1:
            l = l[0]
        if type(r) == tuple and len(r) == 1:
            r = r[0]
        
        if len(l) > 1 and l[0].startswith('UMinus'):
            l = l[-1]
        if len(r) > 1 and r[0].startswith('UMinus'):
            r = r[-1]

        code = (f'CMP{op}', l, r, id)

    elif type(src) == IfElse:
        # Here we need to get all operations
        # Get the type of short-circuiting
        # if left is true for and -> go check right
        # if left is true for or -> jump over right
        cond_list = list()
        true_list = list()
        false_list = list()
        # If we use and/or (short-circuiting)
        if type(src.condition) == LBinary:
            lbinary_handler(src.condition, cond_list, true_list, false_list)
            print(cond_list)
            print(true_list)
            print(false_list)
            cond = tuple()
        else: # No short-circuiting
            cond_list = list()
            cond = translate(src.condition, cond_list)


        # print(cond)

        # print(cond)
        # if branch is either block or stmt
        if_branch = src.if_branch
        else_branch = src.else_branch

        if_stmts = list()
        if type(if_branch) == Block:
            block_handler(if_branch, if_stmts, [], False)
        else:
            translate(if_branch, if_stmts)
            # for stmt in if_branch.statements:
                # translate(stmt, if_stmts)

        label_true = generate_tmp_label()
        label_false = generate_tmp_label()

        if else_branch != None:
            label_after_else = generate_tmp_label()
        # Add all cond list instructions for safety
        # Like when temp value is changed but not stored in memory
        # for c in cond_list:
            # instr_list.append(c)
        if len(cond) > 0:
            if cond not in cond_list:
                cond_list.append(cond)
        temp = list()
        for cond in cond_list:
            if cond[0].startswith('CMP'):
                # print(cond)
                op = cond[0].split('CMP')[-1]
                temp.append(cond)
                code = (f'IF{op}', cond[1], cond[2], label_true)
                temp.append(code)
            elif cond[0].startswith('LPrimary'):
                code = (f'IF!=', cond[-1], str(0), label_true)
                temp.append(code)
            elif cond[0].startswith('NOT'):
                # Append Not instr itself to load from mem
                temp.append(cond)
                code = (f'IF!=', cond[-1], str(0), label_true)
                temp.append(code)
            elif cond[0].startswith('UMinus'):
                temp.append(cond)
                # code = (f'IF==', cond[-1], str(0), label_true)
                # temp.append(code)
            elif len(cond) == 1: # LLiteral True False
                code = (f'IF==', cond[0], str(1), label_true)
                temp.append(code)

        code = (f'GOTO', NULL, NULL, label_false)
        instr_list.extend(temp)
        instr_list.append(code)
        instr_list.append(('LABEL', NULL, NULL, label_true + ':'))
        instr_list.extend(if_stmts)
        if else_branch != None:
            instr_list.append((f'GOTO', NULL, NULL, label_after_else))
        instr_list.append(('LABEL', NULL, NULL, label_false + ':'))

        if else_branch != None and type(else_branch) == Block:
            else_stmts = list()
            block_handler(else_branch, else_stmts, [], False)
            instr_list.extend(else_stmts)
            instr_list.append(('LABEL', NULL, NULL, label_after_else + ':'))
        elif else_branch != None and type(else_branch) != Block:
            else_stmts = list()
            translate(else_branch, else_stmts)
            instr_list.extend(else_stmts)
            instr_list.append(('LABEL', NULL, NULL, label_after_else + ':'))


    elif type(src) == WhileLoop:
        # If CMP goto loop body
        # Go to end
        # Loop body
        # goto if
        cond = translate(src.condition, instr_list)

        stmts = list()
        if type(src.body) == Block:
            block_handler(src.body, stmts, [], False)
        else:
            translate(src.body, stmts)

        label_check = generate_tmp_label()
        label_true = generate_tmp_label()
        label_false = generate_tmp_label()
        instr_list.append(('LABEL', NULL, NULL, label_check + ':'))

        if cond[0].startswith('CMP'):
            op = cond[0].split('CMP')[-1]
            code = (f'IF{op}', cond[1], cond[2], label_true)
            instr_list.append(code)
        elif cond[0].startswith('LPrimary'):
            code = (f'IF!=', cond[1], str(0), label_true)
            instr_list.append(code)

        code = (f'GOTO', NULL, NULL, label_false)
        instr_list.append(code)
        instr_list.append(('LABEL', NULL, NULL, label_true + ':'))
        instr_list.extend(stmts)
        code = (f'GOTO', NULL, NULL, label_check)
        instr_list.append(code)
        instr_list.append(('LABEL', NULL, NULL, label_false + ':'))

    elif type(src) == Call:
        # Get args
        id = generate_tmp_var()
        envs[current_scope].places.add(id)

        n = len(src.arguments)
        callee = src.callee.name
        i = 0
        for arg in src.arguments:
            if type(arg) == ALiteral:
                id = generate_tmp_var()
                envs[current_scope].places.add(id)
                code = ('COPY', str(int(arg.value)), NULL, id)
                instr_list.append(code)
                instr_list.append(('PARAM', i, NULL, id))
            elif type(arg) == Variable:
                instr_list.append(('PARAM', i, NULL, arg.identifier.name))
            else:
                # ABinary 
                sub_instrs = list()
                tmp = translate(arg, sub_instrs)
                instr_list.extend(sub_instrs)
                instr_list.append(('PARAM', i, NULL, tmp[-1]))
            i += 1
        # CALL
        code = ('CALL', id, n, callee)
        instr_list.append(code)
    elif type(src) == FunDecl:
        id = src.identifier.name

        # is_fun_decl = True

        function_places.add(id)
        body = src.body
        body_instr = list()
        block_handler(body, body_instr, src, True)
        # print(body_instr)
        code = ('LABEL', NULL, NULL, id + ':')
        instr_list.append(code)
        # instr_list.append(('FUNPUSH', NULL, NULL, NULL))
        instr_list.extend(body_instr)
        # temp = instr_list[-1]
        # instr_list[-1] = instr_list[-2]
        # instr_list[-2] = temp
        # instr_list.append(('FUNPOP', NULL, NULL, NULL))
        # translate(body, [])

    elif type(src) == Print:
        val = translate(src.expr, instr_list)
        
        code = NULL
        if len(val) == 1: # Literal
            if val[0] in envs[current_scope].string_table:
                code = ('PRINT', NULL, 'STRING', val[0])
            elif val[0] in envs[current_scope].vector_table.keys():
                code = ('PRINT', NULL, 'VECTOR', val[0])
            else:
                code = ('PRINT', NULL, NULL, val[0])
        elif val[0] == 'STRING':
          # instr_list.append()
          code = ('PRINT', NULL, 'STRING', val[-1])
        elif val[0].startswith('VECTOROP'):
            code = ('PRINT', NULL, NULL, val[-1])
        elif val[0].startswith('OP'):
            code = ('PRINT', NULL, NULL, val[-1])
            # instr_list.append(val)

        instr_list.append(code)

    elif type(src) == Return:
        val = translate(src.expr, instr_list)
        
        code = NULL
        if len(val) == 1:
            code = ('RETURN', NULL, NULL, val[0])
        elif val[0].startswith('OP'):
            code = ('RETURN', NULL, NULL, val[-1])
            # instr_list.append(val)

        # Find parent function name
        func_name = ''
        temp_scope = current_scope
        while (temp_scope != 'global'):
            if envs[temp_scope].func_name != '':
                func_name = envs[temp_scope].func_name
                break
            temp_scope = envs[temp_scope].parent

        # Check if return is inside a block, then swap goto with stack
        # deallocation
        # if (instr_list)
        instr_list.append(code)
        instr_list.append((f'GOTO', NULL, NULL,  func_name + '_end'))
    elif type(src) == ForLoop:


        inits = list()
        conds = list()
        increments = list()
        if src.initializer != None:
            translate(src.initializer, inits)

        if src.condition != None:
           conds2 = translate(src.condition, conds)

        if src.increment != None:
            translate(src.increment, increments)

        # cond = translate(src.condition, instr_list)
        # print(conds2)
        if len(conds2) > 0:
            if conds2 not in conds:
                conds.append(conds2)

        stmts = list()
        if type(src.body) == Block:
            block_handler(src.body, stmts, [], False)
        else:
            translate(src.body, stmts)

        label_check = generate_tmp_label()
        label_true = generate_tmp_label()
        label_false = generate_tmp_label()

        instr_list.extend(inits)
        instr_list.append(('LABEL', NULL, NULL, label_check + ':'))


        for cond in conds:
            if cond[0].startswith('CMP'):
                op = cond[0].split('CMP')[-1]
                code = (f'IF{op}', cond[1], cond[2], label_true)
                instr_list.append(code)
            elif cond[0].startswith('LPrimary'):
                code = (f'IF!=', cond[1], str(0), label_true)
                instr_list.append(code)

        code = (f'GOTO', NULL, NULL, label_false)
        instr_list.append(code)
        instr_list.append(('LABEL', NULL, NULL, label_true + ':'))
        instr_list.extend(stmts)
        instr_list.extend(increments)
        code = (f'GOTO', NULL, NULL, label_check)
        instr_list.append(code)
        instr_list.append(('LABEL', NULL, NULL, label_false + ':'))


    return code




def main(input_code) -> tuple:
    global envs
    print("==============================================")
    print("Inside translate.py to make TAC")
    print()
    # input_code = sys.argv[1]
    with open(input_code) as f:
        source = f.read()
    ast = process(source)
    multiple_vars = multiple_var_declarations(ast)
    undecl_vars = undeclared_vars(ast)
    print("AST:")
    print(ast)
    print()
    #print("TAC)
    if len(multiple_vars) > 0:
        raise Exception("Multiple Variable Declarations!!")
    if len(undecl_vars) > 0:
        raise Exception("Usage of Undeclared Variables!!")

    if type(ast) == Program:
        all_funcs = list()
        stmts = ast.statements
        fun_decls = ast.fun_decls
        var_decls = ast.var_decls

        global_env = Environment(current_scope, '')
        
        envs[current_scope] = global_env

        # stmts res
        res = list()

        for v in var_decls:
            # Pass only those which have an initializer
            if v.initializer != None:
                temp = list()
                translate(v, temp)
                res.extend(temp)
            else:
                envs[current_scope].places.add(v.identifier.name)

        for stmt in stmts:
            temp = list()
            translate(stmt, temp)
            print(temp)
            res.extend(temp)
        res.append(('EPILOGUE',))

        for f in fun_decls:
            # Pass only those which have an initializer
            temp = list()
            translate(f, temp)
            res.extend(temp)
        # print(res)
        # for r in res:
        #     print(r)
        # for r in res:
          # code.extend(list(filter(lambda x: x, r[1])))
        with open(f'{input_code.split(".")[0]}.ic', 'w') as out:
            for r in res:
                #print(r)
                # out.write('\n'.join(filter(lambda x: x, r[1])))
                out.write(str(r))
                out.write('\n')
        return (res, envs)
    return ([], envs)
    


