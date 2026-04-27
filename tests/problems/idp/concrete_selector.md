# Concrete Selector

A construction consultancy company is specialised in finding the best type of concrete for a job. Selecting concrete is done on the basis of three parameters: strength, highest working temperature, and maximum viscosity.

### Here’s what we know:
- The company has a range of "standard mixes" for concrete (c1, c2, c3), for which the values of the three parameters are mostly known.
- These standard mixes can be further tweaked to meet specific needs (resulting in mixes like c1_1, c1_2, etc.).
- The known parameter values for the mixes are as follows:
  - c1: Strength 50, High_T 75, Max_Vis 30
  - c2: Strength 60, High_T 85, Max_Vis Unknown
  - c3: Strength 80, High_T Unknown, Max_Vis 25
  - c1_1: Strength 55, High_T 73, Max_Vis 30
  - c1_2: Strength 60, High_T 65, Max_Vis Unknown
  - c1_3: Strength 47, High_T Unknown, Max_Vis 20
  - c2_1: Strength Unknown, High_T 95, Max_Vis 12
  - c2_2: Strength 65, High_T 85, Max_Vis Unknown
  - c3_1: Strength Unknown, High_T Unknown, Max_Vis 18
  - c3_2: Strength 90, High_T Unknown, Max_Vis Unknown
  - c3_3: Strength 75, High_T 100, Max_Vis Unknown

### General Rules:
- If a parameter of a specific tweaked mix is unknown, assume the parameter value of the default mix on which it is based as an approximation.
- If that default value is also unknown, then do not apply any constraints that would exclude the mix based on that parameter.

### Task:
Model this problem using IDP-Z3 (FO(·)) to create a knowledge base capable of deciding which concrete mixes meet specific requirements.

1. Vocabulary: Define types for the standard mixes, the tweaked mixes, and their parameters.
2. Theory: Formulate the rules that determine the assumed values of strength, temperature, and viscosity for each mix based on the fall-back logic.
3. Structure: Provide the data for the specific mixes.
4. Reasoning Task: Use Model Expansion or Propagation to query the knowledge base and find all suitable mixes for varying constraints.
