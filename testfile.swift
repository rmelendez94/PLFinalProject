
let variable1 = (exec 'from java.lang import Math; toReturn = Math.max(23, 34)') + 1 //Here they match
let variable2 = 35

var variable3 = (exec 'from java.lang import Math; toReturn = Math.max(23, 34)') + 1 //Here they do NOT match
var variable4 = 99

if variable1 == variable2 { print("We have a match") } else { print("Nope") }

var list1 = (exec 'import Stream; toReturn = Stream.stream1(Stream.createEmpList())') //Demonstrate with java file stream 1

var list2 = (exec 'import Stream; toReturn = Stream.stream2(Stream.createEmpList())') //Demonstrate with java file stream 2

print (list1) //Print the result of java stream1

print (list2) //Print the result of java stream2


//We now need list comprehension incorporated, Use python in an exec?
