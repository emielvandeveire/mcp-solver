This problem explores non-monotonic reasoning and exceptions in a taxonomic hierarchy. Model the problem using FO(·) for the IDP-Z3 reasoning engine, specifically focusing on the separation of vocabulary, theory, and structure.

### Here’s what we know:

- Tweety is a bird and is yellow.
- Opus is a bird and is a penguin.
- Woody is a bird and is a woodpecker.
- Penguins and woodpeckers are both types of birds.
- Later, we find out that Woody is injured due to a broken wing.
- There is also an airplane named Polly, and Polly can fly.

### General Rules

- By default, birds can fly.
- Penguins cannot fly (this is an exception).
- Injured birds cannot fly (another exception).
- Anything that can fly is considered mobile.
- All birds have feathers.

### Task:

Model this domain as a reusable Knowledge Base to answer questions about the capabilities of these entities.

1. Vocabulary: Define a type for `Entity` and predicates for `bird`, `penguin`, `woodpecker`, `airplane`, `injured`, `flies`, `mobile`, and `has_feathers`.
2. Theory: Define the general rules. Use negation-as-failure or explicit exceptions to model the default "birds fly" rule. 
3. Structure: Provide the specific facts for Tweety, Opus, Woody, and Polly.
4. Reasoning Task: 
   - Use Propagation to determine for each entity: Can it fly? Is it mobile? Does it have feathers?
   - Use Explain to determine the reasoning type (fact, default, or exception) for each conclusion.

Verify the results for each entity, specifically checking if the exceptions for Opus (penguin) and Woody (injured) are correctly handled by the theory.