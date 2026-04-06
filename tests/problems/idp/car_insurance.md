# Car Insurance: Premium & Eligibility

This problem models a decision support system for car insurance. It uses domain knowledge to determine if a customer is eligible for insurance and calculates the final premium based on risk factors.

### Here’s what we know:

- Customers: Ann (age 16) and Brit (age 32).
- Car Types: Sedan (risk factor 1.03) and Truck (risk factor 1.15).
- Current Case: 
  - The applicant is Ann.
  - The car value is 20,000.
  - The car type is a Sedan.

### General Rules (Theory):

1. Age Requirement: Every applicant must be an adult, meaning their age must be 18 or older.
2. Premium Calculation: The insurance premium is calculated as: `(car_value / 100) * risk_factor` of the car type.

### IDP-Z3 Task:

Model this problem as a Knowledge Base to perform insurance calculations and eligibility checks.

1. Vocabulary: 
   - Define types for `Customer` and `Car`.
   - Define functions for `age`, `risk_factor`, `car_value`, `car_type`, and `premium`.
   - Define a predicate `applicant`.
2. Structure: Provide the ages for Ann and Brit, the risk factors for the car types, and the specific data for the current case (car value and applicant).
3. Theory: Implement the age constraint and the premium formula.
4. Reasoning Task: 
   - Use Satisfiability to check if the current applicant (Ann) is eligible.
   - Use Model Expansion to calculate the premium if eligible.
   - Use Explain to show why a customer is or is not eligible.

Determine the eligibility and premium for the current case.