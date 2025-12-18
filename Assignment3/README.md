# Assignment 3: Functional Programming Language

A lambda calculus interpreter with arithmetic, conditionals, let bindings, and lists.

## Authors

Nathan Garcia and Kurt lim

## Features

**Milestone 1:** Lambda calculus + arithmetic (`+`, `-`, `*`)  
**Milestone 2:** Conditionals (`if`), comparisons (`==`, `<=`), let bindings (`let`, `letrec`)  
**Milestone 3:** Lists (`#`, `:`, `hd`, `tl`), sequencing (`;;`)

## Usage

```bash
python interpreter_test.py          # Run all tests
python interpreter.py test.lc       # Run example file
python interpreter.py "1 + 2"       # Evaluate expression
```

## Examples

```
(\x.x * x) 3                                         →  9.0
let x = 5 in if x == 5 then x+1 else x-1            →  6.0
hd (1:2:3:#)                                         →  1.0
letrec f = \n. if n==0 then 1 else n*f(n-1) in f 5  →  120.0
```
