# Final-project_Formal-Languages

# ST0270/SI2002 - Formal Languages and Compilers Project

## LL(1) and SLR(1) Parser Implementation

---

## Group Members

- Mariana Sanchez Araque
- Sebastian Cañon 
---

## System Requirements

### Operating System
- **OS**: Ubuntu 22.04.3 LTS / Windows 11 / macOS Ventura 13.4
- **Architecture**: x86_64

### Programming Language
- **Python**: Version 3.10.12 or higher
- **Required Libraries**: None (uses only Python standard library)

---

## Project Description

This project implements algorithms to compute **FIRST** and **FOLLOW** sets, and constructs both **LL(1)** (Top-Down) and **SLR(1)** (Bottom-Up) parsers for context-free grammars. The implementation follows the algorithms described in Aho et al., *Compilers: Principles, Techniques, and Tools* (2nd Edition), sections 4.4 and 4.6.

### Features

1. **FIRST Set Computation**: Computes FIRST sets for all nonterminals in the grammar
2. **FOLLOW Set Computation**: Computes FOLLOW sets for all nonterminals in the grammar
3. **LL(1) Parser**: Implements top-down predictive parsing using parsing tables
4. **SLR(1) Parser**: Implements bottom-up shift-reduce parsing using LR(0) items and SLR(1) parsing tables
5. **Grammar Classification**: Automatically determines if a grammar is LL(1), SLR(1), both, or neither

---

## Installation and Setup

### Prerequisites

Ensure Python 3.10 or higher is installed on your system:

```bash
python3 --version
```

### Download the Project

```bash
git clone [your-repository-url]
cd [project-directory]
```

No additional dependencies need to be installed.

---

## Usage Instructions

### Running the Program

Execute the program from the command line:

```bash
python3 parser.py
```

### Input Format

The program expects input in the following format:

1. **First line**: An integer `n` representing the number of production rules
2. **Next n lines**: Production rules in the format:
   ```
   <Nonterminal> -> <derivation1> <derivation2> ... <derivationN>
   ```

### Input Grammar Conventions

- The capital letter **`S`** is always the start symbol
- **Nonterminals** are represented by uppercase letters (A-Z)
- **Terminals** are any characters that are NOT uppercase letters
- The **empty string (ε)** is represented by the letter **`e`**
- All input strings must end with **`$`** (added automatically by the parser)
- The symbols **`e`** and **`$`** cannot be used as terminal symbols

### Example 1: SLR(1) Grammar

**Input:**
```
3
S -> S+T T
T -> T*F F
F -> (S) i
```

**Output:**
```
Grammar is SLR(1).
```

Then enter strings to parse (one per line, empty line to exit):
```
i+i
yes
(i)
yes
(i+i)*i)
no

```

### Example 2: LL(1) and SLR(1) Grammar

**Input:**
```
3
S -> AB
A -> aA d
B -> bBc e
```

**Output:**
```
Select a parser (T: for LL(1), B: for SLR(1), Q: quit):
```

**User selects:** `T`

Then enter strings to parse:
```
d
yes
adbc
yes
a
no

```

**Output:**
```
Select a parser (T: for LL(1), B: for SLR(1), Q: quit):
```

**User selects:** `Q` (program exits)

### Example 3: Neither LL(1) nor SLR(1)

**Input:**
```
2
S -> A
A -> A b
```

**Output:**
```
Grammar is neither LL(1) nor SLR(1).
```

Program exits immediately.

---

## Program Behavior

The program operates in four possible modes based on the grammar properties:

### Case 1: Grammar is both LL(1) and SLR(1)
- Prompts user to select a parser (T for LL(1), B for SLR(1), Q to quit)
- Parses input strings with the selected parser
- Returns to parser selection after each parsing session

### Case 2: Grammar is LL(1) only
- Prints "Grammar is LL(1)."
- Accepts strings to parse using LL(1)
- Exits on empty input line

### Case 3: Grammar is SLR(1) only
- Prints "Grammar is SLR(1)."
- Accepts strings to parse using SLR(1)
- Exits on empty input line

### Case 4: Grammar is neither LL(1) nor SLR(1)
- Prints "Grammar is neither LL(1) nor SLR(1)."
- Exits immediately

---
``

### Algorithm Implementation

#### FIRST Set Algorithm
- Iteratively computes FIRST sets for all nonterminals
- Handles epsilon productions correctly
- Properly propagates FIRST sets through production rules

#### FOLLOW Set Algorithm
- Computes FOLLOW sets based on FIRST sets
- Adds `$` to the start symbol's FOLLOW set
- Correctly handles epsilon productions in computing FOLLOW sets

#### LL(1) Parser
- Constructs predictive parsing table
- Detects conflicts (multiple entries in same table cell)
- Uses stack-based parsing algorithm
- Checks for LL(1) condition violations

#### SLR(1) Parser
- Creates augmented grammar with S' -> S
- Computes canonical collection of LR(0) items
- Constructs SLR(1) parsing table (ACTION and GOTO)
- Detects shift-reduce and reduce-reduce conflicts
- Implements shift-reduce parsing algorithm

---

## Testing

The program has been tested with multiple grammars including:

- Simple expression grammars (arithmetic operators)
- Grammars with epsilon productions
- Left-recursive grammars (for SLR(1))
- Ambiguous grammars
- Non-deterministic grammars

All test cases comply with the project specifications.

---

## Known Limitations

1. The program assumes well-formed input according to specifications
2. Nonterminals must be single uppercase letters
3. The start symbol must always be 'S'
4. No error recovery is implemented for malformed grammars

---

## Problems Encountered and Solutions

### Problem 1: Epsilon Production Handling
**Issue**: Initial implementation didn't correctly handle epsilon productions in FIRST and FOLLOW computations.

**Solution**: Added explicit checks for `len(prod) == 1 and prod[0] == 'e'` to properly identify epsilon productions and handle them separately in the algorithms.

### Problem 2: SLR(1) Closure Computation
**Issue**: The closure function wasn't correctly handling the augmented start symbol S' when building LR(0) items.

**Solution**: Modified `_closure()` to accept a set of all nonterminals (including S') as a parameter, ensuring proper closure computation for all items.

### Problem 3: Parser State Management
**Issue**: LL(1) parser wasn't correctly handling the end-of-input marker ($) in all cases.

**Solution**: Improved the termination condition in `parse_ll1()` to correctly verify that all input has been consumed when $ is matched.

### Problem 4: Input/Output Format
**Issue**: Original implementation included extra prompts and messages not specified in the project requirements.

**Solution**: Removed all unnecessary messages and prompts to match the exact specification format, ensuring clean input/output for automated testing.

---

## References

- Aho, Alfred V. et al. *Compilers: Principles, Techniques, and Tools* (2nd Edition). USA: Addison-Wesley Longman Publishing Co., Inc., 2006. ISBN: 0321486811.
- Course lectures and materials from ST0270/SI2002


