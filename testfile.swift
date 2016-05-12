
let variable1 = (exec 'from java.lang import Math; toReturn = Math.max(23, 34)') //Here they match
let variable2 = 35

var variable3 = (exec 'from java.lang import Math; toReturn = Math.max(23, 34)') //Here they dont
var variable4 = 99

if variable1 == variable2 { //Uses Variables 1-4 above
print ("We have a match") //Print if the numbers match, case 1 above
} else {
print ("Nope") //Print if they do not match, case 2 above
}

var list1 = (exec 'import Stream; toReturn = Stream.stream1()') //This will use java streams to get list [C1, C2]

print (list1) //Print the streamed list, should output [C1, C2] (possibly change to string)

//We now need list comprehension incorporated, Use python in an exec?
