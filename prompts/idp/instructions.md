# MCP Solver – IDP-Z3 / FO(·) Quick Start Guide

Welcome to the MCP Solver. This document provides detailed guidelines for building and solving knowledge bases using the IDP-Z3 reasoning engine and the FO(·) logic language.

## Overview

The MCP Solver integrates IDP-Z3 solving with the Model Context Protocol, allowing you to create, modify, and solve knowledge bases incrementally. The following tools are available:

- **clear_model**
- **add_item**
- **replace_item**
- **delete_item**
- **solve_model**

These tools let you construct your knowledge base item by item and solve it using IDP-Z3.

## What is IDP-Z3 / FO(·)?

IDP-Z3 is a reasoning engine for FO(·), a rich extension of classical First-Order Logic with useful features such as types, aggregates, (inductive) definitions, and more. It explicitly supports the Knowledge Base Paradigm, in which the same domain knowledge can be used for many different reasoning tasks.

As in normal FOL, a vocabulary in FO(·) consists of a set of symbols. Because FO(·) is a typed logic, this includes types, in addition to predicate and function symbols. For instance, in the example about car insurance below, we use types `Customer` and `Car`. The function `risk_factor` maps each `Car` to its associated risk factor (∈ ℝ), while the function `age` maps each `Customer` to their age (∈ ℤ). A number of constants (= 0-ary functions) represent the car's value, its type, and the insurance premium. Finally, a unary predicate `applicant` represents which of the customers is requesting the insurance.

A structure for a vocabulary provides an interpretation for some (not necessarily all) of the symbols in this vocabulary. A theory consists of a set of logical sentences. In the example below, we have two sentences: one states that every applicant must be an adult, and one defines the calculation of the insurance premium.

```idp
vocabulary V {
  type Customer := {Ann, Brit}
  type Car      := {Sedan, SUV, Truck}
  risk_factor: Car      -> Real
  age:         Customer -> Int
  car_value:            -> Real
  premium:              -> Real
  car_type:             -> Car
  applicant:   Customer -> Bool
}

structure S : V {
  age         := {Ann -> 16, Brit -> 32}.
  risk_factor := {Sedan -> 1.03, Truck -> 1.15}.
}

theory T : V {
  !p in Customer: applicant(p) => age(p) >= 18.
  premium() = (car_value() / 100) * risk_factor(car_type()).
}
```

We denote the value of a symbol σ in a structure S by σˢ and extend this notation to terms and formulas (e.g., age(Ann)ˢ = 16). A structure S such that φˢ = true for all φ ∈ T is called a (logical) model of T, written as S |= T.

Given such a KB, IDP-Z3 can perform different forms of reasoning to answer different questions. For instance, it can determine which customers are eligible for an insurance policy and explain why. Given the car type and car value, it can also calculate the insurance premium, or optimise the premium by looking for the car type with the lowest risk factor. Using these different reasoning tasks does not require any modifications to the KB itself, allowing for straightforward knowledge reuse.

FO(·) is expressive enough to model many problem domains. Furthermore, as First-Order Logic is the subject of many articles and textbooks, the training corpora of LLMs will also contain enough information to allow them to be fluent in this formalism.

## FO(·) KB Items and Structure

- **KB Item:** A complete block belonging to either the vocabulary, structure, or theory. Each item ends with a closing brace `}` or a period `.` depending on context.
- **No Output Statements:** Do not include output formatting in your model. The solver handles only the KB and the reasoning task.
- **Indices Start at 0:** Items are added one by one, starting with index 0.

## List Semantics for Model Operations

The model items behave like a standard programming list with these exact semantics:

- **add_item(index, content)**: Inserts the item at the specified position, shifting all items at that index and after to the right.
  - Example: If model has items [A, B, C] and you call add_item(1, X), result is [A, X, B, C]
  - Valid index range: 0 to length (inclusive)

- **delete_item(index)**: Removes the item at the specified index, shifting all subsequent items to the left.
  - Example: If model has items [A, B, C, D] and you call delete_item(1), result is [A, C, D]
  - Valid index range: 0 to length-1 (inclusive)

- **replace_item(index, content)**: Replaces the item at the specified index in-place. No shifting occurs.
  - Example: If model has items [A, B, C] and you call replace_item(1, X), result is [A, X, C]
  - Valid index range: 0 to length-1 (inclusive)

**Important**: All indices are 0-based. The first item is at index 0, the second at index 1, etc.

**Critical: Index stability on errors**

- Indices only change when an operation succeeds. If `add_item`, `replace_item`, or `delete_item` returns an error, the model is unchanged and item indices remain exactly the same.
- Specifically for `add_item`: do not advance your intended insertion index after a failed call. Try again with the same index once the cause of the error is fixed.

## Tool Input and Output Details

1. **clear_model**
   - **Input:** No arguments.
   - **Output:** Confirmation that the model has been cleared.

2. **add_item**
   - **Input:**
     - `index` (integer): Position to insert the new FO(·) block.
     - `content` (string): The complete FO(·) block to add.
   - **Output:** Confirmation and the current (truncated) model.
   - **Index behavior on error:** If the call fails (e.g., invalid index, malformed content), the model is not modified and no indices shift.

3. **replace_item**
   - **Input:**
     - `index` (integer): Index of the item to replace.
     - `content` (string): The new FO(·) block.
   - **Output:** Confirmation and the updated (truncated) model.

4. **delete_item**
   - **Input:**
     - `index` (integer): Index of the item to delete.
   - **Output:** Confirmation and the updated (truncated) model.

5. **solve_model**
   - **Input:**
     - `timeout` (number): Time in seconds allowed for solving (between 1 and 30 seconds).
     - `reasoning_task` (string): The reasoning task to perform (see section below).
   - **Output:**
     - A JSON object with:
       - **status:** `"SAT"`, `"UNSAT"`, or `"TIMEOUT"`.
       - **solution:** (If applicable) The solution object when the model is satisfiable.

## Reasoning Tasks

IDP-Z3 supports eight distinct forms of reasoning over a knowledge base. Select the task that matches the question being asked.

| Task | Formal Definition | When to use |
|---|---|---|
| **Model Expansion** | Generate n logical models of theory T (i.e., structures S such that S \|= T). The interpretation of some symbols may already be given; the reasoner completes the rest. | "Find a valid assignment / solution." |
| **Satisfiability** | Verify if at least one model S exists for a given theory T. | "Is this situation possible?" |
| **Optimization** | Find the model S of a given T in which a given term t reaches its minimal or maximal value. | "What is the minimum cost / maximum output?" |
| **Propagation** | Determine which atomic formulas are true or false in all models S of the given theory T. | "What can we conclude with certainty?" |
| **Explain** | Explain why a given atomic formula is true or false in all models of T, or if T has no models, explain the inconsistency. | "Why is X the case?" / "Why is there no solution?" |
| **Determine Range** | Determine the range of possible values for a given function term f given a theory T — the set of all values v such that there exists at least one model S of T in which f evaluates to v. | "What values can X have?" |
| **Relevance** | Determine which symbols σ are relevant, in the sense that there exists a model S of T such that S would no longer be a model if the value of σ in S were different. | "Which inputs actually affect the outcome?" |
| **Logical Entailment** | Verify whether a given statement φ is logically entailed by theory T. | "Does the knowledge base imply φ?" |

**Key principle:** The vocabulary and theory do not change between tasks. Only the reasoning task and any additional data in the structure change.

## Model Solving and Verification

- **Solution Verification:** After solving, verify that the returned solution satisfies all constraints in the theory. If the model is satisfiable (`SAT`), you will receive both the status and the solution; otherwise, only the status is provided.
- **UNSAT is valid:** If the theory is unsatisfiable given the structure, `UNSAT` is a correct and meaningful result. It means the constraints jointly have no solution.
- **Semantic check:** If the KB is UNSAT before any query-specific data is added, this likely indicates a mistake in the theory — not an inherent property of the domain.

## Model Modification Guidelines

- **Comments:** Combine comments with the block they describe. A comment alone is not a standalone item.
- **Combining similar parts:** Group related type declarations or related sentences in the same item.
- **Incremental Changes:** Use `replace_item` for small edits (e.g., changing a constant value or fixing a formula). This avoids rebuilding the entire model.
- **When to Clear:** Use `clear_model` only when the structure of the problem changes fundamentally and starting over is more efficient.

## Blueprint: Recommended FO(·) KB Structure

A typical IDP-Z3 knowledge base for MCP Solver should follow this four-item structure:

1. **Vocabulary block:** All types, predicates, and function declarations.
2. **Structure block:** Known facts, constants, and partial interpretations.
3. **Theory block:** Logical sentences — implications, biconditionals, quantified formulas, definitions.
4. **Reasoning task call:** The specific task to execute (Model Expansion, Optimization, etc.).

**Example — Car Insurance:**

```idp
// Item 0: Vocabulary
vocabulary V {
  type Customer := {Ann, Brit}
  type Car := {Sedan, SUV, Truck}
  risk_factor: Car -> Real
  age: Customer -> Int
  car_value: -> Real
  premium: -> Real
  car_type: -> Car
  applicant: Customer -> Bool
}

// Item 1: Structure (known data)
structure S : V {
  age := {Ann -> 16, Brit -> 32}.
  risk_factor := {Sedan -> 1.03, SUV -> 1.10, Truck -> 1.15}.
}

// Item 2: Theory (constraints and definitions)
theory T : V {
  // Every applicant must be an adult.
  !p in Customer: applicant(p) => age(p) >= 18.
  // Insurance premium calculation.
  premium() = (car_value() / 100) * risk_factor(car_type()).
}

// Item 3: Reasoning task (e.g., Model Expansion)
// Ask: given car_value = 20000 and car_type = Sedan, what is the premium?
```

## FO(·) Syntax Reference

### Types
```idp
type Person := {Ann, Bob, Carol}   // Enumerated type
type Score := {1..10}              // Integer range type
```

### Predicates and Functions
```idp
eligible: Person -> Bool           // Unary predicate
friends: Person * Person -> Bool   // Binary predicate
age: Person -> Int                 // Function returning integer
risk: Person -> Real               // Function returning real
```

### Theory Sentences
```idp
// Universal quantification
!p in Person: eligible(p) => age(p) >= 18.

// Existential quantification
?p in Person: eligible(p).

// Biconditional (if and only if)
!p in Person: student(p) <=> enrolled(p).

// Negation
!p in Person: ~(boy(p) & girl(p)).

// Aggregates
!p in Person: total(p) = sum{ score(p, c) | c in Course }.

// Count
#{p in Person: eligible(p)} >= 1.

// Arithmetic
premium() = (car_value() / 100) * risk_factor(car_type()).
```

### Structure Assignments
```idp
structure S : V {
  age := {Ann -> 25, Bob -> 17}.
  car_type := Sedan.
  car_value := 20000.
}
```

## Grammar Quick Reference (FO(·) Constraints)

| Construct | FO(·) Syntax |
|---|---|
| Conjunction | `expr1 & expr2` |
| Disjunction (inclusive) | `expr1 \| expr2` |
| Negation | `~expr` |
| Implication | `expr1 => expr2` |
| Biconditional | `expr1 <=> expr2` |
| Exclusive or | `expr1 <=> ~expr2` |
| Universal quantification | `!x in Type: expr` |
| Existential quantification | `?x in Type: expr` |
| Count aggregate | `#{x in Type: expr}` |
| Sum aggregate | `sum{ f(x) \| x in Type: cond }` |
| Arithmetic comparisons | `<`, `>`, `=<`, `>=`, `=`, `~=` |
| Absolute value | `abs(expr)` |

**Note on Closed World Assumption (CWA):** IDP-Z3 always uses the CWA. All type extensions must be fully enumerated in the vocabulary. If open-world reasoning is needed, add an explicit `unknown` element to each relevant type.

## Best Practices

- **Separate knowledge from queries.** Put domain rules in the theory and specific case data in the structure. This allows you to reuse the theory for many different reasoning tasks without changes.
- **Use clear, descriptive names** for types, predicates, and functions.
- **Annotate each symbol** with its natural language meaning as a comment.
- **Think about implicit constraints.** For example: if someone studies a course they are a student; nobody can be both a boy and a girl; a fixed order requires that no two elements share the same position.
- **Prefer biconditionals over implications** when a property holds exactly when certain conditions are met.
- **Use exclusive or** (`<=> ~`) rather than inclusive or when "or" in natural language means "one or the other, not both."
- **Group related sentences** together in the theory block.
- **Test incrementally:** Add vocabulary and a small theory, solve, then expand.

## Common Pitfalls

- **Missing type enumeration:** IDP-Z3 requires all type extensions to be fully listed. Omitting elements leads to incorrect or unexpected results.
- **Confusing predicates and functions:** Predicates return `Bool`; functions return a typed value. Do not mix them.
- **Using open-world reasoning implicitly:** IDP-Z3 is CWA only. If something is not stated, it is assumed false. Add an `unknown` element if OWA is needed.
- **Putting query data in the theory:** Specific case data (e.g., "Ann is 25") belongs in the structure, not in the theory. Mixing them prevents knowledge reuse.
- **Forgetting periods** at the end of theory sentences.
- **Untyped or ungrounded variables:** Every variable must be quantified over a declared type.
- **Redundant or contradictory sentences:** An inconsistent theory is always UNSAT regardless of the structure. Run a satisfiability check on the theory alone (without case data) to detect this early.
- **Choosing the wrong reasoning task:** Model Expansion finds solutions; Propagation finds certainties; Optimization finds extrema. Make sure the task matches the question.

## Minimal Working Example

Suppose you want to determine which customers are eligible for car insurance and what their premium would be:

```idp
// Item 0: Vocabulary
vocabulary V {
  type Customer := {Ann, Brit}
  type Car := {Sedan, SUV, Truck}
  age: Customer -> Int
  risk_factor: Car -> Real
  car_value: -> Real
  car_type: -> Car
  premium: -> Real
  applicant: Customer -> Bool
  eligible: Customer -> Bool
}

// Item 1: Structure
structure S : V {
  age := {Ann -> 25, Brit -> 17}.
  risk_factor := {Sedan -> 1.03, SUV -> 1.10, Truck -> 1.15}.
  car_value := 20000.
  car_type := Sedan.
  applicant := {Ann -> true, Brit -> true}.
}

// Item 2: Theory
theory T : V {
  // Eligibility: applicant must be an adult.
  !p in Customer: eligible(p) <=> (applicant(p) & age(p) >= 18).
  // Premium calculation.
  premium() = (car_value() / 100) * risk_factor(car_type()).
}

// Item 3: Solve with Model Expansion
// Result: eligible = {Ann}, premium = 206.0
```

## Advanced Patterns

### Fixed Ordering Constraints
Use this when the problem introduces a strict ordering (e.g., rank people by consumption):
```idp
// No two elements share the same position in the order.
!p1 in Person: !p2 in Person: position(p1) = position(p2) => p1 = p2.
```

### Simulating Open World Assumption
Add an `unknown` element to each type where OWA is needed:
```idp
type Person := {Ann, Bob, unknown}
```
This allows the reasoner to treat `unknown` as a stand-in for any unspecified individual.

### Aggregates with Conditions
```idp
// Total consumption is the sum of drink consumptions the person is dependent on.
!p in Person: total(p) = sum{ drink_consumption(p, d) | d in Drink: dependent(p, d) }.
```

### Multi-step Reasoning
For complex nested questions, break them into sequential reasoning tasks:
1. Run **Propagation** to determine what is certain given the domain.
2. Run **Model Expansion** with those certainties added to the structure.
3. Run **Optimization** if an extremum is needed.

### Satisfiability as a Sanity Check
Before adding query-specific data to the structure, verify the theory alone is satisfiable:
- If SAT: the domain rules are consistent.
- If UNSAT: there is a contradiction in the theory that must be fixed before proceeding.

## Self-Refinement Workflow

When the solver returns an error or UNSAT unexpectedly:

1. **Syntax error:** Check that all sentences end with `.`, all blocks close with `}`, and all variables are quantified over declared types.
2. **Semantic error (unexpected UNSAT):** Temporarily remove constraints one by one to find the conflicting sentence. IDP-Z3 can generate a minimal unsatisfiable subset to assist.
3. **Wrong reasoning task:** Re-read the question and check the task table above to confirm you are using the correct form of reasoning.
4. **Data in wrong block:** Confirm that domain rules are in the theory and case-specific facts are in the structure.

## Final Notes

- **Review return information** after each tool call.
- **Maintain a consistent structure:** vocabulary, structure, theory, task.
- **Verify solutions** after solving to ensure all theory sentences are satisfied.
- **Reuse your KB:** Once the vocabulary and theory are built, answer multiple questions by changing only the structure or the reasoning task.

Happy modeling with MCP Solver and IDP-Z3 / FO(·)!