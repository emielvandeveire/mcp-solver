# Map Colouring (Neighboring Countries)

A classic constraint satisfaction problem involves coloring a map such that no two adjacent regions share the same color. We want to color a map of a few European countries using a limited set of colors.

### Here’s what we know:
- The countries to be colored are: Belgium (BE), Netherlands (NL), France (FR), Luxembourg (LU), and Germany (DE).
- The available colors are: Red, Green, Blue, and Yellow.
- We know the following borders between these countries:
  - Belgium borders the Netherlands, France, Germany, and Luxembourg.
  - The Netherlands borders Belgium and Germany.
  - France borders Belgium, Luxembourg, and Germany.
  - Luxembourg borders France, Germany, and Belgium.
  - Germany borders France, the Netherlands, Belgium, and Luxembourg.
- Note: The bordering relationship is symmetric.

### General Rules:
- Every country must be assigned exactly one color.
- If two countries share a border (i.e., they are neighbors), they cannot be assigned the same color.

### Task:
Model this problem using IDP-Z3 (FO(·)) to find a valid coloring for the map.

1. Vocabulary: Define types for the countries and colors, a relation (predicate) for the borders, and a function mapping each country to its assigned color.
2. Theory: Define the map coloring constraint (neighboring countries must have different colors).
3. Structure: Enumerate the countries, the colors, and all the specific borders between the countries as given in the knowledge base.
4. Reasoning Task: Use Model Expansion to find a valid color assignment for all the countries.
