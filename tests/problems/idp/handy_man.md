This problem explores non-monotonic reasoning and exceptions in a taxonomic hierarchy. Model the problem using FO(·) for the IDP-Z3 reasoning engine, specifically focusing on the separation of vocabulary, theory, and structure.

### Here’s what we know:

A local handyman is an expert at hanging objects on walls. Sometimes he uses a nail, sometimes he uses glue, sometimes he uses a screw. Over the years, he has gathered the following knowledge:
- Nails support weights up to 25kg, screws support up to 40kg and glue supports only 15kg.
- Nails and screws require drilling holes in the wall, which cannot be done in tile walls.
- Glue is the easiest to use, a nail takes slightly more effort, and a screw is hardest to use.

### Task:

With this knowledge, he wants to answer questions such as:
1. Which method is easiest for hanging a 20kg weight on a brick wall?
2. There is a nail in my wall. How much weight will it support?
3. I want to hang a heavy object on my wooden wall, without knowing precisely how heavy it is. Which method will support the most weight?
4. Can we hang a 25kg object on a tile wall?
5. Where can I hang 20 kg?