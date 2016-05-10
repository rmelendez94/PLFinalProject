//: Playground - noun: a place where people can play

import UIKit

//Manually create a list here of the student data. 

let variable1 = (exec 'from java.lang import Math; toReturn = Math.max(23, 34)') //Here they match
let variable2 = 35

var variable3 = (exec 'from java.lang import Math; toReturn = Math.max(23, 34)') //Here they dont
var variable4 = 99

if variable1 == variable2 //Uses Variables 1-4 above
print "We have a match"
else
print "Nope"

print //student list before streaming
var list1 = (exec 'from java.util import stream; toReturn = (Do some streming of the list here)[Will we run into trouble in our parser?]') //We can possibly make this an exec of a stream operation that results in a shorter list of students who meet a certain criteria

print // student list after streaming