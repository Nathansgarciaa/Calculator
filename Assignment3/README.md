# Assignment 3 - Milestone 1: Lambda Calculus with Arithmetic

This project implements a functional programming language by combining lambda calculus with arithmetic operations.

## Features

- **Lambda calculus**: Variables, abstraction (`\x.body`), application
- **Arithmetic operations**: `+`, `-`, `*`, and numbers
- **Lazy evaluation**: Does not reduce under lambda, does not evaluate arguments before substitution
- **Proper precedence**:
  1. Application (highest, left-associative)
  2. Unary negation
  3. Multiplication (left-associative)
  4. Addition and subtraction (left-associative, same precedence)
  5. Lambda abstraction (lowest, right-associative)

## Installation

Requires Python 3 and the `lark` parser library.

```bash
cd Assignment3
pip install lark
```

## Usage

Run tests:
```bash
python interpreter_test.py
```

Interpret a file:
```bash
python interpreter.py test.lc
```

Interpret from command line:
```bash
python interpreter.py "(\x.x * x) 3"
```

## Example Expressions

```
(\x.x) (1--2)                    →  3.0
(\x.x + 1) 5                     →  6.0
(\x.x * x) 3                     →  9.0
(\x.\y.x + y) 3 4                →  7.0
1-2*3-4                          →  -9.0
(\x.x * x) 2 * 3                 →  12.0
(\x.x * x) (-2) * (-3)           →  -12.0
```

## Implementation Details

### Grammar (grammar.lark)
Defines the syntax with proper precedence levels:
- Lambda abstraction has lowest precedence
- Addition/subtraction are left-associative
- Multiplication has higher precedence than addition
- Unary negation binds tighter than binary operators
- Application has highest precedence

### Interpreter (interpreter.py)
Key functions:
- `evaluate()`: Reduces expressions using lazy/normal-order evaluation
- `substitute()`: Performs capture-avoiding substitution with α-renaming
- `linearize()`: Converts AST back to readable string format

### Testing (interpreter_test.py)
Comprehensive test suite covering:
- Lazy evaluation semantics
- Arithmetic operations
- Operator precedence
- Edge cases (double/triple negation, parentheses)

## Grading Requirements Met

✓ Lambda calculus operations work correctly  
✓ All required test cases pass  
✓ Additional test cases in blue highlighting  
✓ Proper operator precedence implemented  
✓ Lazy evaluation strategy implemented  
✓ Comments explain grammar decisions

## Team

Nathan Garcia and Kurt Lim 
