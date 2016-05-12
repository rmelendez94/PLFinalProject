
let variable1 = (exec 'from java.lang import Math; toReturn = Math.max(23, 34)') + 1
let variable2 = 35

var variable3 = (exec 'from java.lang import Math; toReturn = Math.max(23, 34)') + 1
var variable4 = 99

if variable1 == variable2 { print("We have a match") } else { print("Nope") }
if variable4 < 40 { print("\(variable4) is less than 40" )} else { print("\(variable4) is not less than 40")}


//Demonstrate with java file stream 1
var list1 = (exec 'import Stream; toReturn = Stream.stream1(Stream.createEmpList())')

//Demonstrate with java file stream 2
var list2 = (exec 'import Stream; toReturn = Stream.stream2(Stream.createEmpList())')

var list3 = listcomp(list1)

print (list3)

if list2 == list3 { print("The output of the java stream and the output of the python list comprehension are the same.") } else { print("The outputs are different.")}
print ("The output from the java stream: \(list2)")
print ("The output form the python list comprehension: \(list3)")