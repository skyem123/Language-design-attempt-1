# Plan

A rough plan for making this programming language would be (hopefully) (**I'm currently doing step 1, by the way**):
1. Do a detailed specification, including code examples and what should happen.
	* Needs a specification of the standard library.
	* Need to decide what this will run on / compile to.
2. Work on the first implementation of the interpreter in another language, implementing a limited subset of the specification
3. Make sure that implementation works as expected, and fix any issues in the specification encountered while writing the interpreter
4. Make the interpreter into a compiler, and fix any issues in the specification that are encountered.
5. Add more features from the specification into the interpreter and compiler until the specification is fully implemented, fixing issues in the specification along the way
6. Make the language self-hosting by porting the compiler and interpreter into the language, again fixing issues in the compiler and interpreter and specification along the way (this probably won't be a fun task...)
7. Try to optimize the compiler and interpreter.
