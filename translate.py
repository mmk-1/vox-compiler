import sys
from project1_solutions.ast_tools import *
from project1_solutions.misc import *



tmp_var_id_count = -1
def generate_tmp_var():
    global tmp_var_id_count
    tmp_var_id_count += 1
    return f't{tmp_var_id_count}'

def translate(exp):
    if type(exp) == type(ABinary):
        # (OP, VARIABLE OR LITERAL, VARIABLE OR LITERAL)
        name = generate_tmp_var()

        firstarg_name, firstarg_code = translate(exp[1])
        secondarg_name, secondarg_code = translate(exp[2])

        firstarg_code.extend(secondarg_code) #calculate(evaluate) firstarg, THEN secondarg.
        #very important line, has important semantic implications!

        firstarg_code.append(f'{name} = {firstarg_name} {exp[0]} {secondarg_name}')
        #do the operation and assign it to tmp variable for this op_expression.

        code = firstarg_code
    elif type(exp) == type(Assign):
        # Assign(Id, Expr)
        name = exp[0]
        assigned_name, assigned_code = translate(exp[1])
        assigned_code.append(f'{name} = {assigned_name}')
        #calculate the value for the assigned and simply assign it to ID!

        code = assigned_code
    elif type(exp) == type(ALiteral):
        return (str(int(exp.value)), [])
    elif type(exp) == type(Program):
        stmts = exp[2]
        # res = None
        for stmt in stmts:
            translate(stmt)
        # print(res)
        return
    return (name, code)

if __name__ == "__main__":
    input_code = sys.argv[1]
    with open(input_code) as f:
        source = f.read()
    ast = generate_ast(source)
    translate(ast)
    

'''
Program(
        var_decls=[VarDecl(identifier=Identifier(name='a', lineno=1, index=4), initializer=None), VarDecl(identifier=Identifier(name='b', lineno=2, index=11), initializer=None), VarDecl(identifier=Identifier(name='c', lineno=3, index=18), initializer=None)], 
        fun_decls=[], 
        statements=[
            Assign(identifier=Identifier(name='a', lineno=5, index=22), expr=
                   ALiteral(value=3.0)), 
            Assign(identifier=Identifier(name='a', lineno=6, index=29), expr=
                   ABinary(op='+', left=ALiteral(value=5.0), right=
                           ABinary(op='*', left=ALiteral(value=3.0), right=
                                   ABinary(op='-', left=ALiteral(value=2.0), right=
                                           Variable(identifier=Identifier(name='a', lineno=6, index=40)))))), 
                                    Assign(identifier=Identifier(name='b', lineno=7, index=44), expr=Variable(identifier=Identifier(name='a', lineno=7, index=48)))])
'''
