Types
=====
**NOTE THAT EVERYTHING HERE IS JUST A DESIGN AND WORK IN PROGRESS AND WILL CHANGE WHILE BEING IMPLEMENTED**

The language is statically typed, with type inference, however dyamic typing is allowed.

A variable has a type, which defines what can be put into it. For example, you can't put a ```String``` into an ```Integer```.
```
String a = "42"
Integer b = a  // This will crash / exception / whatever
```

#### Type Inference
This is where the compiler finds a type from the data put into a varible.
```
var a = 42 // a is now an Integer containing the number 42
var b = "Hello!" // b is now a String containing "Hello!"
a = b // this will not work as a and b are of different types
```

#### Casting
However, you **can** put an ```Integer``` into a ```Long```, as the language will be able to cast the ```Integer``` to a ```Long``` without any chance of failiure.
```
Integer a = 42
Long b = a 
```
It is possible to convert a ```Long``` into an ```Integer```, by forcing a cast. Forcing a cast will mean that there is a chance of failiure, which will throw an exception.
```
Long a = 42
Integer b = (Integer)a
```

#### Dynamic Typing
Dynamic typing is allowed with the ```Dynamic``` type. Everything can put put into a varible with a ```Dynamic``` type, but to get data out of a Dynamic variable it does not need to be cast, but it can throw an exception just like casting would!
```
Dynamic a = "Hello, World!" // a now contains a string
a = 42 // now it contains an Integer
Integer b = a // this will work.

Dynamic c = "This is a test"
Integer d = c // This will crash, as you can't convert normal text into an Integer!
```

#### Subtyping
_TODO_

#### The type of a Function
_TODO_
