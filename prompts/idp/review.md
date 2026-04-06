# IDP-Z3 / FO(·) Solution Review Template

Your task is to review an IDP-Z3 / FO(·) knowledge base and its solution for structural correctness, adherence to the problem statement, and best practices.

## Problem Statement

${PROBLEM}

## Knowledge Base Implementation

${MODEL}

## Solution Results

${SOLUTION}

## Review Guidelines

⚠️ **IMPORTANT**: Do NOT try to verify that every logical sentence is mathematically correct in full generality. However, DO verify that the solution satisfies the hard constraints and requirements stated in the problem, and that the structure of the knowledge base is sound.

Focus on these checks:

1. **Structural Correctness**
   - Is the KB divided into the three required blocks: `vocabulary`, `structure`, and `theory`?
   - Does every type in the theory appear in the vocabulary?
   - Are all predicates and functions declared with the correct arity and return type?
   - Do all theory sentences end with a period `.`?
   - Do all blocks close with `}`?
   - Are all variables quantified over a declared type (no untyped or ungrounded variables)?
   - Is the reasoning task appropriate for the question being asked?

2. **Vocabulary Soundness**
   - Are all types fully enumerated (IDP-Z3 uses Closed World Assumption — all elements must be listed)?
   - Are predicates correctly typed as `Type -> Bool`?
   - Are functions correctly typed with their return type (`-> Int`, `-> Real`, `-> Type`)?
   - Are constants declared as zero-arity functions (`-> Type`)?

3. **Hard Constraint Satisfaction**
   - Based on the solution, check whether all theory sentences are satisfied.
   - For example: if the problem says "every applicant must be an adult", verify that no eligible person in the solution has age < 18.
   - Focus on constraints you can verify directly from the problem statement and the returned solution values.
   - If a sentence involves complex aggregates or arithmetic, check the result value rather than the full derivation.

4. **Knowledge / Data Separation**
   - Is domain knowledge (rules, definitions, constraints) in the **theory** block?
   - Is case-specific data (known values, given facts) in the **structure** block?
   - Mixing them is a red flag — it prevents knowledge reuse and can introduce unexpected UNSAT.

5. **Reasoning Task Verification**
   - Is the reasoning task used (Model Expansion, Optimization, Propagation, etc.) the right one for the question?
   - For **Optimization**: does the solution report the minimised or maximised value, and does it match the problem's objective?
   - For **Propagation**: do the reported certainties follow from the theory alone?
   - For **Satisfiability**: is the yes/no answer consistent with the constraints?
   - For **Logical Entailment**: is the entailed formula consistent with the theory?

6. **For Unsatisfiable Solutions**
   - **IMPORTANT**: You do NOT need to explain WHY the problem is unsatisfiable.
   - Verify that all theory sentences are justified by the problem statement.
   - If all sentences are justified, mark the result as correct — UNSAT is a valid and meaningful answer.
   - If UNSAT appears unexpected, check whether case data was accidentally placed in the theory instead of the structure, or whether two sentences contradict each other.
   - Trust the solver's determination of unsatisfiability.

7. **Implicit Constraints**
   - Are implicit constraints captured? Examples:
     - Nobody can belong to two mutually exclusive categories (e.g., boy and girl).
     - If someone studies a course, they are a student.
     - A fixed ordering requires that no two elements share the same position.
     - Exclusive "or" in natural language should be encoded as a biconditional with negation (`<=> ~`), not inclusive disjunction.

8. **Basic Sanity Checks**
   - Are all atoms in the solution properly grounded (no free variables)?
   - Are there any obvious contradictions or missing assignments in the solution?
   - Does the solution include values for all symbols the problem asks about?

9. **Optimality Verification**
   - If the solution claims to be optimal (e.g., minimum premium, maximum score), verify this makes sense given the problem constraints.
   - Check that the reported optimal value matches the assignments in the solution.

10. **DO NOT Check**
    - ❌ Whether every logical sentence is globally correct in all possible interpretations (trust the encoding for non-obvious cases)
    - ❌ Whether the solver found the globally optimal solution (trust the solver)
    - ❌ Complex aggregate derivations step by step
    - ❌ Whether soft preferences match your intuition

## Output Format

After your detailed analysis, provide your verdict using simple XML tags.

**Your answer MUST follow this structure:**
1. First provide a detailed explanation of your reasoning.
2. Analyse each major constraint or sentence from the theory.
3. Check vocabulary and structure soundness.
4. Verify the reasoning task is appropriate.
5. End with a clear conclusion statement: "The solution is correct." or "The solution is incorrect."
6. Finally, add exactly ONE of these verdict tags on a new line:

```
<verdict>correct</verdict>
<verdict>incorrect</verdict>
<verdict>unknown</verdict>
```

For example:

```
[Your detailed analysis here]

After checking all constraints, vocabulary declarations, and the reasoning task, I can confirm that each sentence is satisfied by the provided solution values and the KB structure is sound.

The solution is correct.

<verdict>correct</verdict>
```

The verdict must be EXACTLY one of: "correct", "incorrect", or "unknown" — nothing else.

**Before finalising your response, always check that:**
1. Your explanation ends with a clear conclusion statement.
2. The verdict tag matches your conclusion exactly.
3. If your explanation concludes "The solution is correct", use `<verdict>correct</verdict>`.
4. If your explanation concludes "The solution is incorrect", use `<verdict>incorrect</verdict>`.
5. If you cannot determine correctness or establish incorrectness, use `<verdict>unknown</verdict>`.

## Data

### Problem Statement

$PROBLEM

### IDP-Z3 / FO(·) Knowledge Base

$MODEL

### Solution

$SOLUTION
