# Vacation Days

The number of vacation days an employee receives depends on their age and years of service.

### Here’s what we know:
- Every employee receives a base of at least 22 days.

### General Rules:
Additional days are provided according to the following criteria:
1. Only employees younger than 18 or at least 60 years old, or employees with at least 30 years of service will receive 5 extra days.
2. Employees with at least 30 years of service and also employees of age 60 or more, receive 3 extra days, on top of possible additional days already given.
3. If an employee has at least 15 but less than 30 years of service, 2 extra days are given. These 2 days are also provided for employees of age 45 or more.
4. Exception: These 2 extra days cannot be combined with the 5 extra days.

### Task:
Model the calculation of vacation days using IDP-Z3 (FO(·)).

1. Vocabulary: Define types for employees, and functions assigning them an age, years of service, and total vacation days.
2. Theory: Model the default rules and exceptions for computing the extra days and the total number of vacation days.
3. Reasoning Task: Use the knowledge base to calculate the total vacation days for various hypothetical employees.
