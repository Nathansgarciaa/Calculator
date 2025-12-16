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


if __name__ == "__main__":
    test_lazy_evaluation()
    test_arithmetic()
    test_precedence()
    test_additional_cases()
    
    print("\n" + "="*60)
    print("ALL TESTS PASSED! ✓")
    print("="*60 + "\n")
