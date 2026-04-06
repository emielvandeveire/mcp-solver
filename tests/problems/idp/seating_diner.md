We need to organize a small dinner for three guests and assign them to specific seats. The goal is to find a valid seating arrangement that respects personal conflicts and physical constraints.

### Here’s what we know:

- There are three guests: An, Bert, and Cas.
- There are three seats arranged in a single row, numbered 1, 2, and 3.

### General Rules:

- Unique Seating: Each guest must be assigned to exactly one seat.
- Single Occupancy: Each seat can be occupied by at most one guest.
- Social Constraint: An and Bert are having a disagreement and cannot sit next to each other. Seats are considered adjacent if their numbers differ by exactly 1.

### Task:

Model and solve this problem using IDP-Z3 (FO(·)) to determine a valid seating arrangement for all three guests.

1. Vocabulary: Define types for `Guest` and `Seat`, and a function or predicate to map guests to seats.
2. Theory: Define the constraints for unique seating and the adjacency rule for An and Bert.
3. Structure: Enumerate the guests and seat numbers.
4. Reasoning Task: Use Model Expansion to find one valid seating plan.

For the final output, list which seat each guest is assigned to and verify that An and Bert are not sitting next to each other, in adjacent seats.