# MCP Solver – IDP-Z3 / FO(·) Quick Start Guide

Welcome to the MCP Solver. This document provides detailed guidelines for building and solving knowledge bases using the IDP-Z3 reasoning engine and the FO(·) logic language.

## Overview

The MCP Solver integrates IDP-Z3 solving with the Model Context Protocol, allowing you to create, modify, and solve knowledge bases incrementally. The following tools are available:

- **clear_model**
- **add_item**
- **replace_item**
- **delete_item**
- **solve_model**
- **check_syntax**

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


## Blueprint: Recommended FO(·) KB Structure

A typical IDP-Z3 knowledge base for MCP Solver should follow this four-item structure:

1. **Vocabulary block:** All types, predicates, and function declarations.
2. **Structure block:** Known facts, constants, and partial interpretations.
3. **Theory block:** Logical sentences — implications, biconditionals, quantified formulas, definitions.
4. **Reasoning task call:** The specific task to execute (Model Expansion, Optimization, etc.).


## FO(·) Syntax Reference

### Types
```idp
type Person := {Ann, Bob, Carol}   // Enumerated type (nullary constructors)
type Score  := {1..10}             // Integer range type
```
> **Critical rule:** Every identifier used in a structure or theory must belong to an enumerated type declared in the vocabulary. You cannot reference `Tweety` in a structure unless `Tweety` appears inside `type Entity := {Tweety, ...}` in the vocabulary. Forgetting this is the single most common cause of "Symbol not in vocabulary" errors.

### Predicates and Functions
```idp
eligible: Person -> Bool           // Unary predicate (returns Bool)
friends:  Person * Person -> Bool  // Binary predicate
age:      Person -> Int            // Function returning integer
risk:     Person -> Real           // Function returning real
premium:           -> Real         // Nullary function (constant), called as premium()
```

> **Note:** Predicates return `Bool`. Functions return a typed value. Do not mix them. A nullary function `f` must always be called as `f()`, never as `f`.

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

// Aggregates (sum over multiset)
!p in Person: total(p) = sum{{ score(p, c) | c in Course }}.

// Count
#{p in Person: eligible(p)} >= 1.

// Arithmetic
premium() = (car_value() / 100) * risk_factor(car_type()).
```

### Structure Assignments
```idp
structure S : V {
  age      := {Ann -> 25, Bob -> 17}.
  car_type := Sedan.
  car_value := 20000.
}
```

## Grammar Quick Reference (FO(·) Constraints)

| Construct | FO(·) Syntax | Notes |
|---|---|---|
| Conjunction | `expr1 & expr2` | |
| Disjunction | `expr1 \| expr2` | Use `\|`, not `\/` |
| Negation | `~expr` | |
| Implication | `expr1 => expr2` | |
| Biconditional | `expr1 <=> expr2` | |
| Exclusive or | `expr1 <=> ~expr2` | |
| Universal quantification | `!x in Type: expr` | |
| Existential quantification | `?x in Type: expr` | |
| Unique existential | `#{x in Type: expr} = 1` | **Do not use `?!`; it is not valid syntax** |
| Count aggregate | `#{x in Type: expr}` | |
| Sum aggregate (multiset) | `sum{{ f(x) \| x in Type: cond }}` | Double braces `{{ }}` for multisets |
| Arithmetic comparisons | `<`, `>`, `=<`, `>=`, `=`, `~=` | Note: less-than-or-equal is `=<`, not `<=` |
| Absolute value | `abs(expr)` | Built-in for Int and Real |

**Note on Closed World Assumption (CWA):** IDP-Z3 always uses the CWA. All type extensions must be fully enumerated in the vocabulary. If open-world reasoning is needed, add an explicit `unknown` element to each relevant type.

## Critical Syntax Rules (Read Before Writing Any Theory)

These are the mistakes most commonly made. Violating any of these will produce a syntax or runtime error.

### 1. All domain elements must be declared in the vocabulary

Every name used in a structure or theory (e.g. `Tweety`, `Ann`, `Sedan`) must be an element of an enumerated type in the vocabulary block. Declaring them only in the structure is not sufficient.

```idp
// WRONG — Tweety is not declared anywhere
vocabulary V {
  type Entity          // open, no elements
  bird: Entity -> Bool
}
structure S : V {
  bird := {Tweety}.    // ERROR: Tweety not in vocabulary
}

// CORRECT
vocabulary V {
  type Entity := {Tweety, Opus, Woody, Polly}
  bird: Entity -> Bool
}
structure S : V {
  bird := {Tweety, Opus, Woody}.
}
```

### 2. Use `|` for disjunction, not `\/`

The ASCII disjunction operator is `|`. The operator `\/` is not valid and will cause a parse error.

```idp
// WRONG
!x in Person: p(x) \/ q(x).

// CORRECT
!x in Person: p(x) | q(x).
```

### 3. Unique existential quantification: use a cardinality constraint, not `?!`

IDP-Z3 does not support the `?!` operator. Express "exactly one" using the count aggregate or the generalised existential shorthand.

```idp
// WRONG — ?! is not valid syntax
!g in Guest: ?!s in Seat: seated(g) = s.

// CORRECT — option A: cardinality constraint
!g in Guest: #{s in Seat: seated(g) = s} = 1.

// CORRECT — option B: generalised existential (shorthand)
!g in Guest: ?=1 s in Seat: seated(g) = s.
```

### 4. Functions are total by default; use `seated(g) = s` not `seated(g, s)`

In FO(·), a function `f: A -> B` maps every element of A to exactly one element of B. Access its value as `f(a) = b`. Do not confuse functions with predicates.

```idp
// WRONG — seated is a function, not a predicate
seated(An, 1).

// CORRECT
seated(An) = 1.
```

### 5. Every theory sentence must end with a period `.`

```idp
// WRONG
!p in Person: eligible(p) => age(p) >= 18

// CORRECT
!p in Person: eligible(p) => age(p) >= 18.
```

### 6. Less-than-or-equal is `=<`, not `<=`

```idp
// WRONG
age(p) <= 18.

// CORRECT
age(p) =< 18.
```

### 7. Nullary functions must be called with `()`

```idp
// WRONG — premium is a nullary function
premium = 100.

// CORRECT
premium() = 100.
```

### 8. Adjacency: use `abs()` rather than arithmetic on enumerated type elements

When checking whether two values differ by 1, use `abs(s1 - s2) = 1`. Arithmetic like `s - 1` on an enumerated integer type works, but ensure the type is declared as a numeric range (`{1..3}`), not as named constructors.

```idp
// Robust adjacency check for seats declared as {1..3}
!s1, s2 in Seat: abs(s1 - s2) = 1 => ~(seated(An) = s1 & seated(Bert) = s2).
```

### 9. Declare ALL symbols: EVERY predicate or function you use in the `theory` MUST be explicitly declared in the `vocabulary` first. Do not invent new predicates in the theory.

### 10. Finding Extremes (Min/Max): DO NOT invent syntax like `min{...} ordered by` or `wrt`. To define an optimal choice in FO(·), use standard First-Order Logic.
   - Example to find the best option: 
     `!x in Type: best(x) <=> valid(x) & ~(?y in Type: valid(y) & cost(y) < cost(x)).`

### 11. No ASP/Prolog Wildcards: DO NOT use the underscore (_) as a wildcard variable. FO(·) does not support this. You MUST explicitly quantify every variable. (e.g., Use '!w in WallType: capacity(Nail, w) = 25.' instead of 'capacity(Nail, _) = 25.')

## Model Solving and Verification

- **Solution Verification:** After solving, verify that the returned solution satisfies all constraints in the theory. If the model is satisfiable (`SAT`), you will receive both the status and the solution; otherwise, only the status is provided.
- **UNSAT is valid:** If the theory is unsatisfiable given the structure, `UNSAT` is a correct and meaningful result. It means the constraints jointly have no solution.
- **Semantic check:** If the KB is UNSAT before any query-specific data is added, this likely indicates a mistake in the theory, not an inherent property of the domain.

## Model Modification Guidelines

- **Comments:** Combine comments with the block they describe. A comment alone is not a standalone item.
- **Combining similar parts:** Group related type declarations or related sentences in the same item.
- **Incremental Changes:** Use `replace_item` for small edits (e.g., changing a constant value or fixing a formula). This avoids rebuilding the entire model.
- **When to Clear:** Use `clear_model` only when the structure of the problem changes fundamentally and starting over is more efficient.

## Minimal Working Example

Suppose you want to determine which customers are eligible for car insurance and what their premium would be:

```idp
// Item 0: Vocabulary
vocabulary V {
  type Customer := {Ann, Brit}
  type Car      := {Sedan, SUV, Truck}
  age:         Customer -> Int
  risk_factor: Car      -> Real
  car_value:            -> Real
  car_type:             -> Car
  premium:              -> Real
  applicant:   Customer -> Bool
  eligible:    Customer -> Bool
}

// Item 1: Structure
structure S : V {
  age         := {Ann -> 25, Brit -> 17}.
  risk_factor := {Sedan -> 1.03, SUV -> 1.10, Truck -> 1.15}.
  car_value   := 20000.
  car_type    := Sedan.
  applicant   := {Ann -> true, Brit -> true}.
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

### Fixed Ordering / Injective Assignment

When assigning positions or ranks, enforce that no two elements share the same value:

```idp
// No two guests share the same seat
!g1, g2 in Guest: seated(g1) = seated(g2) => g1 = g2.
```

### Simulating Open World Assumption
Add an `unknown` element to each type where OWA is needed:
```idp
type Person := {Ann, Bob, unknown}
```
This allows the reasoner to treat `unknown` as a stand-in for any unspecified individual.

### Aggregates with Conditions
```idp
// Total is the sum of consumptions the person is dependent on.
!p in Person: total(p) = sum{{ drink_consumption(p, d) | d in Drink: dependent(p, d) }}.
```
Note the double braces `{{ }}` for multiset aggregates (`sum`, `min`, `max`). Single braces `{ }` are for set aggregates.

### Multi-step Reasoning
For complex nested questions, break them into sequential reasoning tasks:
1. Run **Propagation** to determine what is certain given the domain.
2. Run **Model Expansion** with those certainties added to the structure.
3. Run **Optimization** if an extremum is needed.

### Satisfiability as a Sanity Check
Before adding query-specific data to the structure, verify the theory alone is satisfiable:
- If SAT: the domain rules are consistent.
- If UNSAT: there is a contradiction in the theory that must be fixed before proceeding.

## Best Practices

- **Separate knowledge from queries.** Put domain rules in the theory and specific case data in the structure. This allows you to reuse the theory for many different reasoning tasks without changes.
- **Use clear, descriptive names** for types, predicates, and functions.
- **Annotate each symbol** with its natural language meaning as a comment.
- **Think about implicit constraints.** For example: if someone studies a course they are a student; nobody can be both a boy and a girl; a fixed order requires that no two elements share the same position.
- **Prefer biconditionals over implications** when a property holds exactly when certain conditions are met.
- **Use exclusive or** (`<=> ~`) rather than inclusive or when "or" in natural language means "one or the other, not both."
- **Group related sentences** together in the theory block.
- **Test incrementally:** Add vocabulary and a small theory, solve, then expand.
- **CRITICAL WORKFLOW RULE:** before you EVER call solve_model, you MUST call the check_syntax tool first to validate your logic. If check_syntax returns an error, use replace_item to fix the error before trying to solve.

### Modeling Best Practices for IDP-Z3
1. **Use Integers for Ordering and Rankings:** Do NOT create custom Enumerations (e.g., `type Effort = {Easy, Medium, Hard}`) and complex boolean predicates (like `easier(e1, e2)`) to rank items. Instead, map these properties directly to Integers. 
   *Example:* Use `difficulty: Method -> Int` and assign `{Nail -> 2, Glue -> 1, Screw -> 3}` in the structure. This allows Z3 to easily optimize or compare values using standard math operators (`<`, `>`, `=`).
2. **Quantifiers:** Never write inline type declarations like `predicate(x: Type) <=>` in the theory block without a universal quantifier (`!`). Always use `! x in Type: predicate(x) <=> ...` or use definition blocks `{ predicate(x) <- ... }`.

## Common Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Domain elements not enumerated in vocabulary | "Symbol not in vocabulary: X" | Add all names to the type declaration in the vocabulary: `type T := {X, Y, Z}` |
| Using `?!` for unique existential | Parse error at `?!` | Use `#{x in T: ...} = 1` or `?=1 x in T: ...` |
| Using `\/` for disjunction | Parse error at `\/` | Use `\|` |
| Using `<=` for less-than-or-equal | Parse error or wrong semantics | Use `=<` |
| Forgetting `.` at end of theory sentence | Parse error | Add `.` after every sentence |
| Calling a nullary function without `()` | Runtime or parse error | Always write `f()` |
| Mixing functions and predicates | Type error | Functions use `=`; predicates are applied directly |
| Query data in theory instead of structure | Theory is UNSAT for other inputs | Move specific facts (values, instances) to the structure |
| Using `sum{ }` (single braces) for multiset sum | Wrong or missing results | Use `sum{{ }}` (double braces) for multiset aggregates |
| Quantifying over `Int` or `Real` without bounds | Performance issues or timeout | Always quantify over a finite enumerated type or bounded range |

## Self-Refinement Workflow

When the solver returns an error or UNSAT unexpectedly:

1. **Syntax error:** Check that all sentences end with `.`, all blocks close with `}`, you use `|` (not `\/`) for disjunction, and no `?!` appears anywhere.
2. **"Symbol not in vocabulary":** Check that every name used in the structure or theory is declared inside a `type T := {...}` enumeration in the vocabulary.
3. **Unexpected UNSAT:** Temporarily remove theory sentences one by one to find the conflicting constraint. Run a satisfiability check on the theory alone (without case data) to isolate the issue.
4. **Wrong reasoning task:** Re-read the question and check the Reasoning Tasks table to confirm you are using the correct form of reasoning.
5. **Data in wrong block:** Confirm that domain rules are in the theory and case-specific facts are in the structure.

## Final Notes

- **Review return information** after each tool call.
- **Maintain a consistent structure:** vocabulary -> structure -> theory -> task.
- **Verify solutions** after solving to ensure all theory sentences are satisfied.
- **Reuse your KB:** Once the vocabulary and theory are built, answer multiple questions by changing only the structure or the reasoning task.

Happy modeling with MCP Solver and IDP-Z3 / FO(·)!