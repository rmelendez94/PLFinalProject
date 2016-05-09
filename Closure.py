class student(object):
    def f(self):
        data = {
            'fname' : 'firstname',
            '$fname': lambda x : data.update({'fname': x}),
            'lname' : 'lastname',
            '$lname': lambda x : data.update({'lname': x}),
            'age'   : -1,
            '$age'  : lambda x : data.update({'age' : x}),
            'major' : 'undeclared',
            '$major': lambda x : data.update({'major': x}),
            'mt1'   : -1,
            '$mt1'  : lambda x : data.update({'mt1' : x}),
            'mt2'   : -1,
            '$mt2'  : lambda x : data.update({'mt2' : x}),
            'final' : -1,
            '$final': lambda x : data.update({'final: x'})
        }

        def cf(self, d):
            if d in data:
                return data[d]
            else:
                return None
        return cf
    run = f(1)

class econ_student(student):            # showcases polymorphism
    def f(self):
        data = {
            'major': 'Economics',
            '$major': lambda x : data.update({'major' : x})
        }
        def cf(self, d):
            if d in data:
                return data[d]
            else:
                return super(econ_student, self).run(d)
        return cf
    run = f(1)

class business_student(student):            # showcases polymorphism
    def f(self):
        data = {
            'major': 'Business',
            '$major': lambda x : data.update({'major' : x})
        }
        def cf(self, d):
            if d in data:
                return data[d]
            else:
                return super(business_student, self).run(d)
        return cf
    run = f(1)

students = []
s1 = student()
e1 = econ_student()
b1 = business_student()

def addStudent(major, fname, lname, age, mt1, mt2, final):
    new_student = []
    if major == "Undeclared":
        new_student.append(s1.run('major'))
        s1.run('$fname')(fname)
        new_student.append(s1.run('fname'))
        s1.run('$lname')(lname)
        new_student.append(s1.run('lname'))
        s1.run('$age')(age)
        new_student.append(s1.run('age'))
        s1.run('$mt1')(mt1)
        new_student.append(s1.run('mt1'))
        s1.run('$mt2')(mt2)
        new_student.append(s1.run('mt2'))
        s1.run('$final')(final)
        new_student.append(s1.run('final'))
    elif major == "Economics":
        new_student.append(e1.run('major'))
        e1.run('$fname')(fname)
        new_student.append(e1.run('fname'))
        e1.run('$lname')(lname)
        new_student.append(e1.run('lname'))
        e1.run('$age')(age)
        new_student.append(e1.run('age'))
        e1.run('$mt1')(mt1)
        new_student.append(e1.run('mt1'))
        e1.run('$mt2')(mt2)
        new_student.append(e1.run('mt2'))
        e1.run('$final')(final)
        new_student.append(e1.run('final'))
    elif major == "Business":
        new_student.append(b1.run('major'))
        b1.run('$fname')(fname)
        new_student.append(b1.run('fname'))
        b1.run('$lname')(lname)
        new_student.append(b1.run('lname'))
        b1.run('$age')(age)
        new_student.append(b1.run('age'))
        b1.run('$mt1')(mt1)
        new_student.append(b1.run('mt1'))
        b1.run('$mt2')(mt2)
        new_student.append(b1.run('mt2'))
        b1.run('$final')(final)
        new_student.append(b1.run('final'))
    students.append(new_student)

def returnAllStudents():
    return students


'''
class substance(object):
    def f(self):
        data = {
            'name': 'Rita',
            '$name': lambda x: data.update({'name': x}),
            'age': 67,
            '$age': lambda x: data.update({'age': x})
        }
        def cf(self, d):
            if d in data:
                return data[d]
            else:
                return None
        return cf
    run = f(1)

s1 = substance()
print
print s1.run('name')
s1.run('$name')('Phil')
print s1.run('name')
print s1.run('age')
s1.run('$age')('66')
print s1.run('age')
print s1.run('dob')
# print s1.data

class animal(substance):
    #def run(self, a): return super(animal, self).run(a)
    def f(self):
        data = {
            'name': 'Animal',
            '$name': lambda x: data.update({'name': x})
        }
        def cf(self, d):
            if d in data:
                return data[d]
            else:
                return super(animal, self).run(d)
        return cf
    run = f(1)

a1 = animal()
print
print "Now printing for a1"
print a1.run('name')
print a1.run('age')
print a1.run('dob')
'''