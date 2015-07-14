Syntax Specification
====================
**NOTE THAT EVERYTHING HERE IS JUST A DESIGN AND WORK IN PROGRESS AND WILL CHANGE WHILE BEING IMPLEMENTED**

The syntax should be similar to C.

Three styles of comments are supported, such as ```/* */```, ```//``` and ```#```.
##### Examples of comments ####
```
/* This ia a
   multi-line
   comment
   /* nesting is a good idea, too */
*/

// This is a single line comment

# This is another single line comment
```

Functions are first class and the minimum needed for a function is ```() {}```, for example, if there was a function that took functions and ran them, a function could be simply passed without strange syntax.
##### Example of passing a function to another function #####
```
// Note that runFunction(Function toRun) {} is Syntactic Sugar for runFunction = (Function toRun) {}
runFunction(Function toRun) {
	toRun(42)
}

runFunction((Integer number) { IO.Standard.writeLine(number) })
```
Should output ```42``` onto the console

There will be many "helper" keywords that help show the language what you want to do with minimal mess, for example, the keyword ```entrypoint``` will be given a function to start with when the file is run. Note that ```entrypoint``` is Syntactic Sugar for placing a call to the function at the end of the file.
##### Example "Hello World" Program using ```entrypoint``` #####
```
entrypoint (){
	IO.Standard.writeLine("Hello World!")
}
```

##### Another example of using ```entrypoint``` #####

```
entrypoint main

main() {
	IO.Standard.writeLine("Hello again!")
}
```
Note that this is the same as
```
main() {
	IO.Standard.writeLine("Hello again!")
}

main()
```
