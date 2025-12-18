from interpreter import interpret, substitute, evaluate, LambdaCalculusTransformer, parser, linearize
from lark import Lark, Transformer

# ANSI color codes
BLUE = '\033[94m'
MAGENTA = '\033[95m'
RESET = '\033[0m'

# Helper function to convert concrete syntax to AST
def ast(source_code):
    return LambdaCalculusTransformer().transform(parser.parse(source_code))

def test_lazy_evaluation():
    """Test that the interpreter follows lazy evaluation (does not reduce under lambda)"""
    print("\n" + "="*60)
    print("TEST LAZY EVALUATION")
    print("="*60)
    
    # Test 1: Don't reduce under lambda
    assert interpret(r"\x.(\y.y)x") == r"(\x.((\y.y) x))"
    print(f"{MAGENTA}\\x.(\\y.y)x{RESET}  -->  (\\x.((\\y.y) x))")
    
    # Test 2: Don't evaluate arguments before substitution
    assert interpret(r"(\x.a x) ((\x.x)b)") == r"(a ((\x.x) b))"
    print(f"{MAGENTA}(\\x.a x) ((\\x.x)b){RESET}  -->  (a ((\\x.x) b))")
    
    print("\nLazy evaluation: All tests passed!\n")


def test_arithmetic():
    """Test basic arithmetic operations"""
    print("\n" + "="*60)
    print("TEST ARITHMETIC OPERATIONS")
    print("="*60)
    
    # Test subtraction with double negative
    result = interpret(r"(\x.x) (1--2)")
    assert result == "3.0", f"Expected 3.0, got {result}"
    print(f"{BLUE}(\\x.x) (1--2){RESET}  -->  3.0")
    
    # Test subtraction with triple negative
    result = interpret(r"(\x.x) (1---2)")
    assert result == "-1.0", f"Expected -1.0, got {result}"
    print(f"{BLUE}(\\x.x) (1---2){RESET}  -->  -1.0")
    
    # Test lambda with addition
    result = interpret(r"(\x.x + 1) 5")
    assert result == "6.0", f"Expected 6.0, got {result}"
    print(f"{BLUE}(\\x.x + 1) 5{RESET}  -->  6.0")
    
    # Test lambda with multiplication
    result = interpret(r"(\x.x * x) 3")
    assert result == "9.0", f"Expected 9.0, got {result}"
    print(f"{BLUE}(\\x.x * x) 3{RESET}  -->  9.0")
    
    # Test multi-argument lambda
    result = interpret(r"(\x.\y.x + y) 3 4")
    assert result == "7.0", f"Expected 7.0, got {result}"
    print(f"{BLUE}(\\x.\\y.x + y) 3 4{RESET}  -->  7.0")
    
    print("\nArithmetic operations: All tests passed!\n")


def test_precedence():
    """Test operator precedence"""
    print("\n" + "="*60)
    print("TEST OPERATOR PRECEDENCE")
    print("="*60)
    
    # Test: * has higher precedence than -
    result = interpret(r"1-2*3-4")
    assert result == "-9.0", f"Expected -9.0, got {result}"
    print(f"{BLUE}1-2*3-4{RESET}  -->  -9.0  (evaluates as 1-(2*3)-4)")
    
    # Test: application has higher precedence than *
    result = interpret(r"(\x.x * x) 2 * 3")
    assert result == "12.0", f"Expected 12.0, got {result}"
    print(f"{BLUE}(\\x.x * x) 2 * 3{RESET}  -->  12.0  (evaluates as ((\\x.x*x) 2) * 3)")
    
    # Test: parenthesized negative numbers
    result = interpret(r"(\x.x * x) (-2) * (-3)")
    assert result == "-12.0", f"Expected -12.0, got {result}"
    print(f"{BLUE}(\\x.x * x) (-2) * (-3){RESET}  -->  -12.0")
    
    # Test: explicit parentheses
    result = interpret(r"((\x.x * x) (-2)) * (-3)")
    assert result == "-12.0", f"Expected -12.0, got {result}"
    print(f"{BLUE}((\\x.x * x) (-2)) * (-3){RESET}  -->  -12.0")
    
    # Test: triple negation
    result = interpret(r"(\x.x) (---2)")
    assert result == "-2.0", f"Expected -2.0, got {result}"
    print(f"{BLUE}(\\x.x) (---2){RESET}  -->  -2.0")
    
    print("\nOperator precedence: All tests passed!\n")


def test_additional_cases():
    """Additional test cases in BLUE"""
    print("\n" + "="*60)
    print("ADDITIONAL TEST CASES")
    print("="*60)
    
    # Test simple addition
    result = interpret(r"2 + 3")
    assert result == "5.0", f"Expected 5.0, got {result}"
    print(f"{BLUE}2 + 3{RESET}  -->  5.0")
    
    # Test simple multiplication
    result = interpret(r"4 * 5")
    assert result == "20.0", f"Expected 20.0, got {result}"
    print(f"{BLUE}4 * 5{RESET}  -->  20.0")
    
    # Test simple subtraction
    result = interpret(r"10 - 3")
    assert result == "7.0", f"Expected 7.0, got {result}"
    print(f"{BLUE}10 - 3{RESET}  -->  7.0")
    
    # Test negation
    result = interpret(r"-5")
    assert result == "-5.0", f"Expected -5.0, got {result}"
    print(f"{BLUE}-5{RESET}  -->  -5.0")
    
    # Test complex expression
    result = interpret(r"2 + 3 * 4")
    assert result == "14.0", f"Expected 14.0, got {result}"
    print(f"{BLUE}2 + 3 * 4{RESET}  -->  14.0  (evaluates as 2 + (3*4))")
    
    # Test lambda with complex body
    result = interpret(r"(\x.x + x) 5")
    assert result == "10.0", f"Expected 10.0, got {result}"
    print(f"{BLUE}(\\x.x + x) 5{RESET}  -->  10.0")
    
    # Test nested lambdas with arithmetic
    result = interpret(r"(\x.\y.x * y) 3 5")
    assert result == "15.0", f"Expected 15.0, got {result}"
    print(f"{BLUE}(\\x.\\y.x * y) 3 5{RESET}  -->  15.0")
    
    # Test associativity of subtraction (left-to-right)
    result = interpret(r"10 - 3 - 2")
    assert result == "5.0", f"Expected 5.0, got {result}"
    print(f"{BLUE}10 - 3 - 2{RESET}  -->  5.0  (evaluates as (10-3)-2)")
    
    # Test mixed operations
    result = interpret(r"2 * 3 + 4 * 5")
    assert result == "26.0", f"Expected 26.0, got {result}"
    print(f"{BLUE}2 * 3 + 4 * 5{RESET}  -->  26.0  (evaluates as (2*3)+(4*5))")
    
    # Test double negation
    result = interpret(r"--5")
    assert result == "5.0", f"Expected 5.0, got {result}"
    print(f"{BLUE}--5{RESET}  -->  5.0")
    
    print("\nAdditional test cases: All tests passed!\n")


def test_milestone2():
    """Test Milestone 2 features: conditionals, let, letrec"""
    print("\n" + "="*60)
    print("MILESTONE 2: CONDITIONALS, LET, LETREC")
    print("="*60)
    
    # Conditionals
    assert interpret("if 0 then 2 else 1") == "1.0"
    print(f"{BLUE}if 0 then 2 else 1{RESET}  -->  1.0")
    
    assert interpret("if 1 then 2 else 2") == "2.0"
    print(f"{BLUE}if 1 then 2 else 2{RESET}  -->  2.0")
    
    assert interpret("if 0 then 2 else if 1 then 3 else 4") == "3.0"
    print(f"{BLUE}if 0 then 2 else if 1 then 3 else 4{RESET}  -->  3.0")
    
    assert interpret("if 0 then 2 else if 0 then 3 else 4") == "4.0"
    print(f"{BLUE}if 0 then 2 else if 0 then 3 else 4{RESET}  -->  4.0")
    
    # Equality and comparison
    assert interpret("if 0 == 0 then 5 else 6") == "5.0"
    print(f"{BLUE}if 0 == 0 then 5 else 6{RESET}  -->  5.0")
    
    assert interpret("if 0 <= 1 then 6 else 7") == "6.0"
    print(f"{BLUE}if 0 <= 1 then 6 else 7{RESET}  -->  6.0")
    
    assert interpret("if 1 <= 0 then 6 else 7") == "7.0"
    print(f"{BLUE}if 1 <= 0 then 6 else 7{RESET}  -->  7.0")
    
    # Let bindings
    assert interpret("let x = 1 in if x == 1 then 8 else 9") == "8.0"
    print(f"{BLUE}let x = 1 in if x == 1 then 8 else 9{RESET}  -->  8.0")
    
    assert interpret("let x = 0 in if x == 1 then 8 else 9") == "9.0"
    print(f"{BLUE}let x = 0 in if x == 1 then 8 else 9{RESET}  -->  9.0")
    
    assert interpret(r"let f = \x.x in f 10") == "10.0"
    print(f"{BLUE}let f = \\x.x in f 10{RESET}  -->  10.0")
    
    assert interpret(r"let f = \x.x+1 in f 10") == "11.0"
    print(f"{BLUE}let f = \\x.x+1 in f 10{RESET}  -->  11.0")
    
    assert interpret(r"let f = \x.x*6 in let g = \x.x+1 in f (g 1)") == "12.0"
    print(f"{BLUE}let f = \\x.x*6 in let g = \\x.x+1 in f (g 1){RESET}  -->  12.0")
    
    assert interpret(r"let f = \x.x*6 in let g = \x.x+1 in g (f 2)") == "13.0"
    print(f"{BLUE}let f = \\x.x*6 in let g = \\x.x+1 in g (f 2){RESET}  -->  13.0")
    
    assert interpret(r"let f = \x.x*6 in let f = \x.x+1 in f (f 2) + 10") == "14.0"
    print(f"{BLUE}let f = \\x.x*6 in let f = \\x.x+1 in f (f 2) + 10{RESET}  -->  14.0")
    
    # Letrec - recursive functions
    assert interpret(r"letrec f = \n. if n==0 then 1 else n*f(n-1) in f 4") == "24.0"
    print(f"{BLUE}letrec f = \\n. if n==0 then 1 else n*f(n-1) in f 4{RESET}  -->  24.0  (factorial)")
    
    assert interpret(r"letrec f = \n. if n==0 then 0 else 1 + 2*(n-1) + f(n-1) in f 6") == "36.0"
    print(f"{BLUE}letrec f = \\n. if n==0 then 0 else 1 + 2*(n-1) + f(n-1) in f 6{RESET}  -->  36.0")
    
    print("\nMilestone 2: All tests passed!\n")


def test_milestone3():
    """Test Milestone 3 features: sequencing and lists"""
    print("\n" + "="*60)
    print("MILESTONE 3: SEQUENCING AND LISTS")
    print("="*60)
    
    # Basic tests
    assert interpret("1") == "1.0"
    print(f"{BLUE}1{RESET}  -->  1.0")
    
    # Sequencing
    assert interpret("1 ;; 2") == "1.0 ;; 2.0"
    print(f"{BLUE}1 ;; 2{RESET}  -->  1.0 ;; 2.0")
    
    assert interpret("1 ;; 2 ;; 3") == "1.0 ;; 2.0 ;; 3.0"
    print(f"{BLUE}1 ;; 2 ;; 3{RESET}  -->  1.0 ;; 2.0 ;; 3.0")
    
    # Empty list
    assert interpret("#") == "#"
    print(f"{BLUE}#{RESET}  -->  #")
    
    # List construction
    assert interpret("1:2:3:#") == "(1.0 : (2.0 : (3.0 : #)))"
    print(f"{BLUE}1:2:3:#{RESET}  -->  (1.0 : (2.0 : (3.0 : #)))")
    
    # List operations with lambda
    assert interpret(r"(\x.x) #") == "#"
    print(f"{BLUE}(\\x.x) #{RESET}  -->  #")
    
    # List equality
    assert interpret("1:2 == 1:2") == "1.0"
    print(f"{BLUE}1:2 == 1:2{RESET}  -->  1.0")
    
    assert interpret("1:2 == 1:3") == "0.0"
    print(f"{BLUE}1:2 == 1:3{RESET}  -->  0.0")
    
    # Head and tail
    assert interpret("hd (1:2:#)") == "1.0"
    print(f"{BLUE}hd (1:2:#{RESET})  -->  1.0")
    
    assert interpret("hd 1:2:#") == "1.0"
    print(f"{BLUE}hd 1:2:#{RESET}  -->  1.0")
    
    assert interpret("tl (1:2:#)") == "(2.0 : #)"
    print(f"{BLUE}tl (1:2:#{RESET})  -->  (2.0 : #)")
    
    assert interpret("tl 1:2:#") == "(2.0 : #)"
    print(f"{BLUE}tl 1:2:#{RESET}  -->  (2.0 : #)")
    
    # Map function
    result = interpret(r"letrec map = \f. \xs. if xs==# then # else (f (hd xs)) : (map f (tl xs)) in (map (\x.x+1) (1:2:3:#))")
    assert result == "(2.0 : (3.0 : (4.0 : #)))"
    print(f"{BLUE}letrec map = ... in map (\\x.x+1) (1:2:3:#{RESET})  -->  (2.0 : (3.0 : (4.0 : #)))")
    
    print("\nMilestone 3: All tests passed!\n")


if __name__ == "__main__":
    test_lazy_evaluation()
    test_arithmetic()
    test_precedence()
    test_additional_cases()
    test_milestone2()
    test_milestone3()
    
    print("\n" + "="*60)
    print("ALL TESTS PASSED! ✓")
    print("="*60 + "\n")
