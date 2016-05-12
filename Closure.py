import csv

def createStudentsList():
    with open('Students.csv', 'rb') as csvfile:
        studentreader = csv.reader(csvfile, delimiter=',')
        for row in studentreader:
            addStudent(row)
    csvfile.close()

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
            '$final': lambda x : data.update({'final' : x})
        }

        def returnListFormat(self):
            return [self.run('major'),self.run('fname'), self.run('lname'),self.run('age'),self.run('mt1'),self.run('mt2'), self.run('final')]

        def cf(self, d):
            if d in data:
                return data[d]
            elif d == 'returnListFormat':
                return returnListFormat(self)
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
s1 = student
e1 = econ_student
b1 = business_student

def addStudent(rowdata):
    (major, fname, lname, age, mt1, mt2, final) = rowdata
    if major == "Undeclared":
        new_student = s1()
    elif major == "Economics":
        new_student = e1()
    elif major == "Business":
        new_student = b1()
    else:
        # row has error in data
        return
    new_student.run('$fname')(fname)
    new_student.run('$lname')(lname)
    new_student.run('$age')(age)
    new_student.run('$mt1')(mt1)
    new_student.run('$mt2')(mt2)
    new_student.run('$final')(final)
    students.append(new_student.run('returnListFormat'))
    return

def returnAllStudents():
    return students

def returnAllBusinessStudents():
    return [i for i in students if i[0] == 'Business']