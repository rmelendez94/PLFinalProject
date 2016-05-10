
let variable1 = (exec 'from java.lang import Math; toReturn = Math.max(23, 34)') //Here they match
let variable2 = 35

var variable3 = (exec 'from java.lang import Math; toReturn = Math.max(23, 34)') //Here they dont
var variable4 = 99

if variable1 == variable2 { //Uses Variables 1-4 above
print "We have a match"
} else {
print "Nope"
}

var list1 = (exec 'from java.util import stream; toReturn = List<String> myList -> { Arrays.asList("a1", "a2", "b1", "c2", "c1"); myList.stream().filter(s -> s.startsWith("c")).map(String::toUpperCase).sorted(); }') //We can possibly make this an exec of a stream operation that results in a shorter list of students who meet a certain criteria
