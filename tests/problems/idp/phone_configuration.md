# Phone Configuration

A producer of phones builds custom, personalized phones for their customers. To make this design process more straightforward, they employ a modular design where phones consist of multiple components, which can require or exclude others.

### Here’s what we know:
- The possible components include a call module, a screen, a GPS module, and media modules (camera and MP3 player).
- The screen must be one of three types: basic, colour, or high resolution.

### General Rules:
- All phones must include the call module.
- All phones must contain exactly one screen type.
- The phone may optionally contain a GPS module, but only if the screen is not basic.
- The phone can support two types of media: a camera and an MP3 player (possibly at the same time).
- There are no special requirements for the MP3 player.
- The camera may only be selected if the screen supports a high resolution.

### Task:
Model this configuration problem using IDP-Z3 (FO(·)) to verify valid phone designs.

1. Vocabulary: Define types and predicates for the components and screen types.
2. Theory: Write the constraints that enforce the valid combinations of modules as outlined in the general rules.
3. Reasoning Task: Use Model Expansion to find valid configurations.
