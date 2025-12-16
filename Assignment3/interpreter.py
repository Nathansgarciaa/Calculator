import sys
import os
from lark import Lark, Transformer

# --- Parsing ---

# convert concrete syntax to CST
parser = Lark(open("grammar.lark").read(), parser='lalr')


# convert CST to AST
class LambdaCalculusTransformer(Transformer):
    def start(self, args):
        # unwrap the single child of 'start'
        return args[0]

    def lam(self, args):
        # args = [LAMBDA_token, name, body]
        _, name, body = args
        return ('lam', str(name), body)

    def app(self, args):
        return ('app', *args)

    def var(self, args):
        token, = args
        return ('var', str(token))

    def num(self, args):
        token, = args
        return ('num', float(token))

    def plus(self, args):
        return ('plus', *args)

    def minus(self, args):
        return ('minus', *args)

    def times(self, args):
        return ('times', *args)

    def neg(self, args):
        return ('neg', args[0])

    def NAME(self, token):
        return str(token)


# --- Name generator for fresh variables (used in capture-avoiding substitution) ---

class NameGenerator:
    def __init__(self):
        self.counter = 0

    def generate(self):
        self.counter += 1
        # user-defined names start with lower case (see the grammar), thus 'Var' is fresh
        return 'Var' + str(self.counter)


name_generator = NameGenerator()


# --- Capture-avoiding substitution ---
# substitute(tree, name, replacement) = tree[replacement/name]

def substitute(tree, name, replacement):
    tag = tree[0]

    if tag == 'var':
        if tree[1] == name:
            # n [r/n] --> r
            return replacement
        else:
            # x [r/n] --> x
            return tree

    elif tag == 'lam':
        bound = tree[1]
        body = tree[2]
        if bound == name:
            # \n.e [r/n] --> \n.e
            return tree
        else:
            # Always alpha-rename the bound variable to a fresh name
            fresh_name = name_generator.generate()
            renamed_body = substitute(body, bound, ('var', fresh_name))
            # Now substitute in the renamed body
            return ('lam', fresh_name, substitute(renamed_body, name, replacement))
            # \x.e [r/n] --> (\fresh.(e[fresh/x])) [r/n]

    elif tag == 'app':
        return (
            'app',
            substitute(tree[1], name, replacement),
            substitute(tree[2], name, replacement),
        )

    elif tag == 'num':
        # numbers don't contain variables
        return tree

    elif tag == 'plus':
        return (
            'plus',
            substitute(tree[1], name, replacement),
            substitute(tree[2], name, replacement),
        )

    elif tag == 'minus':
        return (
            'minus',
            substitute(tree[1], name, replacement),
            substitute(tree[2], name, replacement),
        )

    elif tag == 'times':
        return (
            'times',
            substitute(tree[1], name, replacement),
            substitute(tree[2], name, replacement),
        )

    elif tag == 'neg':
        return ('neg', substitute(tree[1], name, replacement))

    else:
        raise Exception('Unknown tree', tree)


# --- Evaluation to beta-normal form (lazy/normal-order) ---

def evaluate(tree):
    tag = tree[0]

    if tag == 'var':
        return tree

    if tag == 'num':
        return tree

    if tag == 'lam':
        # DO NOT reduce under lambda (lazy evaluation)
        return tree

    if tag == 'app':
        func = evaluate(tree[1])   # normal-order: evaluate function first

        if func[0] == 'lam':
            # beta-reduction
            name = func[1]
            body = func[2]
            # IMPORTANT: DO NOT evaluate argument before substitution (lazy)
            return evaluate(substitute(body, name, tree[2]))

        # If function is NOT a lambda, we have a stuck application
        # In lazy evaluation, we don't evaluate the argument
        return ('app', func, tree[2])

    if tag == 'plus':
        left = evaluate(tree[1])
        right = evaluate(tree[2])
        if left[0] == 'num' and right[0] == 'num':
            return ('num', left[1] + right[1])
        return ('plus', left, right)

    if tag == 'minus':
        left = evaluate(tree[1])
        right = evaluate(tree[2])
        if left[0] == 'num' and right[0] == 'num':
            return ('num', left[1] - right[1])
        return ('minus', left, right)

    if tag == 'times':
        left = evaluate(tree[1])
        right = evaluate(tree[2])
        if left[0] == 'num' and right[0] == 'num':
            return ('num', left[1] * right[1])
        return ('times', left, right)

    if tag == 'neg':
        operand = evaluate(tree[1])
        if operand[0] == 'num':
            return ('num', -operand[1])
        return ('neg', operand)

    raise Exception('Unknown node', tree)


# --- Linearization (AST -> concrete syntax string) ---

def linearize(ast):
    tag = ast[0]

    if tag == 'var':
        return ast[1]

    elif tag == 'num':
        return str(ast[1])

    elif tag == 'lam':
        # (\x.e)
        return "(" + "\\" + ast[1] + "." + linearize(ast[2]) + ")"

    elif tag == 'app':
        # (e1 e2)
        return "(" + linearize(ast[1]) + " " + linearize(ast[2]) + ")"

    elif tag == 'plus':
        return "(" + linearize(ast[1]) + " + " + linearize(ast[2]) + ")"

    elif tag == 'minus':
        return "(" + linearize(ast[1]) + " - " + linearize(ast[2]) + ")"

    elif tag == 'times':
        return "(" + linearize(ast[1]) + " * " + linearize(ast[2]) + ")"

    elif tag == 'neg':
        return "(-" + linearize(ast[1]) + ")"

    else:
        return str(ast)


# --- Top-level interpret function ---

def interpret(source_code):
    cst = parser.parse(source_code)
    ast = LambdaCalculusTransformer().transform(cst)
    result_ast = evaluate(ast)
    result = linearize(result_ast)
    return result


# --- Main: command-line only, no interactive input, plain output only ---

def main():
    if len(sys.argv) != 2:
        # No extra output allowed for tests; just exit with error code.
        sys.exit(1)

    input_arg = sys.argv[1]

    if os.path.isfile(input_arg):
        # If the input is a valid file path, read from the file
        with open(input_arg, 'r') as f:
            expression = f.read()
    else:
        # Otherwise, treat the input as a direct expression
        expression = input_arg

    result = interpret(expression)
    # IMPORTANT: print ONLY the evaluated expression, nothing else.
    print(result)


if __name__ == "__main__":
    main()
