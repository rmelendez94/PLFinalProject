
let variable1 = (exec 'from java.lang import Math; toReturn = Math.max(23, 34)') //Here they match
let variable2 = 35

var variable3 = (exec 'from java.lang import Math; toReturn = Math.max(23, 34)') //Here they dont
var variable4 = 99

if variable1 == variable2 { //Uses Variables 1-4 above
print ("We have a match") //Print if the numbers match, case 1 above
} else {
print ("Nope") //Print if they do not match, case 2 above
}

var list1 = (exec 'from java.util import stream; List<String> myList = Arrays.asList("a1", "a2", "b1", "c2", "c1"); List<String> myNewList = myList.stream().filter(s -> s.startsWith("c")).map (String::toUpperCase).sorted().collect(Collectors.toList());; toReturn = myNewList }') //This will use java streams to get list [C1, C2]

print (list1) //Print the streamed list, should output [C1, C2]



