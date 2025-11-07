# Calculator Specification

## Overview

This calculator implements a context-free grammar-based expression evaluator using the Lark parsing library. It supports arithmetic operations with proper operator precedence and associativity rules.

## Supported Operations

### 1. Basic Arithmetic
- **Addition**: `+` (left-associative, lowest precedence)
- **Subtraction**: `-` (left-associative, lowest precedence)  
- **Multiplication**: `*` (left-associative, medium precedence)

### 2. Advanced Operations
- **Exponentiation**: `^` (right-associative, highest precedence)
- **Unary Minus**: `-` (prefix operator, medium precedence)
- **Logarithms**: `log <value> base <base>` (medium-high precedence)

### 3. Grouping
- **Parentheses**: `()` for explicit precedence control

## Grammar Definition

The calculator uses a precedence-climbing grammar with the following structure:

```
?start: exp

// Addition and Subtraction (lowest precedence)
?exp: exp "+" exp1            -> plus
    | exp "-" exp1            -> minus
    | exp1

// Multiplication (medium-low precedence)  
?exp1: exp1 "*" exp2          -> times
     | exp2

// Unary minus (medium precedence)
?exp2: "-" exp2               -> neg
     | exp3

// Logarithms (medium-high precedence)
?exp3: "log" exp4 "base" exp4 -> log_base
     | exp4

// Exponents (right-associative, highest precedence)
?exp4: exp5 "^" exp4          -> power
     | exp5

// Parentheses and Numbers (highest precedence)
?exp5: NUMBER                 -> num
     | "(" exp ")"
```

## Operator Precedence (highest to lowest)

1. **Parentheses** `()` - Highest precedence
2. **Exponentiation** `^` - Right-associative
3. **Logarithms** `log ... base ...`
4. **Unary Minus** `-` (prefix)
5. **Multiplication** `*`
6. **Addition/Subtraction** `+`, `-` - Lowest precedence

## Associativity Rules

- **Left-associative**: `+`, `-`, `*`
  - Example: `a - b - c` = `(a - b) - c`
- **Right-associative**: `^`
  - Example: `2^3^2` = `2^(3^2)` = `2^9` = 512`

## Input Format

- **Numbers**: Decimal numbers (integers and floats)
- **Operators**: Standard mathematical symbols
- **Logarithms**: `log <value> base <base>`
- **Whitespace**: Ignored between tokens

## Usage Examples

### Basic Arithmetic
```bash
python calculator_cfg.py "2 + 3"          # Output: 5
python calculator_cfg.py "10 - 4"         # Output: 6
python calculator_cfg.py "5 * 6"          # Output: 30
```

### Operator Precedence
```bash
python calculator_cfg.py "1+2*3"          # Output: 7 (not 9)
python calculator_cfg.py "2^3+1"          # Output: 9
python calculator_cfg.py "2^3*2"          # Output: 16
```

### Parentheses
```bash
python calculator_cfg.py "2-(4+2)"        # Output: -4
python calculator_cfg.py "(3+2)*2"        # Output: 10
python calculator_cfg.py "(1+2)*3"        # Output: 9
```

### Unary Minus
```bash
python calculator_cfg.py "--1"            # Output: 1
python calculator_cfg.py "-3^2"           # Output: -9 (-(3^2))
python calculator_cfg.py "-(3+2)"         # Output: -5
```

### Right Associativity
```bash
python calculator_cfg.py "2^3^2"          # Output: 512 (2^(3^2))
```

### Logarithms
```bash
python calculator_cfg.py "log 8 base 2"   # Output: 3
python calculator_cfg.py "log 100 base 10" # Output: 2
python calculator_cfg.py "log 8 base 2 + 1" # Output: 4
```

### Complex Expressions
```bash
python calculator_cfg.py "1+2*3+4*5+6"    # Output: 33
python calculator_cfg.py "(2+3)^2"        # Output: 25
```

## Implementation Details

### Architecture
1. **Parser**: Lark LALR parser generates Concrete Syntax Tree (CST)
2. **Transformer**: Converts CST to Abstract Syntax Tree (AST)
3. **Evaluator**: Recursively evaluates AST to produce numerical result

### AST Node Types
- `('plus', left, right)` - Addition
- `('minus', left, right)` - Subtraction  
- `('times', left, right)` - Multiplication
- `('power', left, right)` - Exponentiation
- `('neg', operand)` - Unary minus
- `('log_base', value, base)` - Logarithm
- `('num', value)` - Number literal

### Output Formatting
- Integer results are displayed without decimal points
- Floating-point results preserve decimal precision
- Uses Python's `math.log()` for logarithm calculations

## Error Handling

The calculator handles:
- **Syntax errors**: Invalid expressions (handled by Lark parser)
- **Mathematical errors**: Division by zero in logarithms
- **Type errors**: Invalid operand types

## Dependencies

- **Python 3.x**
- **Lark parsing library**: `pip install lark`

## Files

- `calculator_cfg.py` - Main calculator implementation
- `grammar.lark` - Grammar definition file
- `specs.md` - This specification document

## Mathematical Properties

### Logarithm Implementation
- Uses change of base formula: `log_a(x) = ln(x) / ln(a)`
- Supports any positive base and value
- Returns floating-point results

### Precision
- Floating-point arithmetic follows Python's `float` precision
- Results may have small rounding errors for complex expressions

## Testing

The calculator has been tested with various expressions to ensure:
- Correct operator precedence
- Proper associativity
- Accurate mathematical calculations
- Robust error handling

For comprehensive test cases, see the test examples above or run the calculator with different expressions to verify behavior.