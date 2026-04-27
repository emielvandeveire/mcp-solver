# Planning Problem

To ensure that a person capable of applying first-aid is always present in a school, a weekly permanence schedule is made. 

### Here’s what we know:
- Days (Monday to Friday) are split into a morning segment and an afternoon segment.
- In total, there are five people that can be assigned permanence: William, Julie, Alex, Emma, and Sophie.
- Each of these people has their own specific availabilities.

### General Rules:
A planning must be made according to the following rules:
1. For each segment, exactly one person must be assigned as the first-aid officer, and exactly one other person must be assigned as the back-up.
2. A person cannot be assigned both first-aid and back-up at the same time.
3. If a person is not available during a segment, they cannot be scheduled for either role.
4. Emma must be assigned first-aid on Wednesday afternoon.
5. William must be back-up on Monday morning.
6. Sophie may only be planned as back-up (never as first-aid officer).

### Task:
Model this scheduling problem using IDP-Z3 (FO(·)) to find a valid weekly schedule.

1. Vocabulary: Define types for days, segments, and persons, along with functions/predicates assigning persons to roles in specific segments.
2. Theory: Define the constraints governing the schedule.
3. Structure: Enumerate the days, segments, and the availability of the persons (create hypothetical availabilities if none are strictly given).
4. Reasoning Task: Use Model Expansion to generate a valid weekly first-aid and back-up schedule.
