# Student-Course Management System Implementation

from collections import defaultdict

class Course:
    all_courses = []

    def __init__(self, code, name, instructor, credits, limit):
        self.code = code
        self.name = name
        self.instructor = instructor
        self.credits = credits
        self.limit = limit
        self.enrolled_students = []  
        self.grades = {}  
        self.waitlist = []
        Course.all_courses.append(self)

    def __str__(self):
        return f"{self.code} - {self.name} ({self.instructor}) [{self.credits} credits]"

    def get_available_spots(self):
        return self.limit - len(self.enrolled_students)

    def get_enrollment_count(self):
        return len(self.enrolled_students)

    def is_full(self):
        return len(self.enrolled_students) >= self.limit

    def enroll_student(self, student):
        if student.student_id in self.enrolled_students:
            return "Already enrolled"
        if self.is_full():
            self.waitlist.append(student.student_id)
            return "Added to waitlist"
        self.enrolled_students.append(student.student_id)
        return "Enrolled"

    def add_grade(self, student_id, grade):
        self.grades[student_id] = grade

    def get_course_statistics(self):
        if not self.grades:
            return {"average": None, "min": None, "max": None, "count": 0}
        grades = list(self.grades.values())
        return {
            "average": sum(grades) / len(grades),
            "min": min(grades),
            "max": max(grades),
            "count": len(grades)
        }

    @classmethod
    def get_total_enrollments(cls):
        return sum(len(course.enrolled_students) for course in cls.all_courses)

class Student:
    all_students = []

    def __init__(self, student_id, name, email, program):
        self.student_id = student_id
        self.name = name
        self.email = email
        self.program = program
        self.courses = {}  
        self.grades = {} 
        Student.all_students.append(self)

    def __str__(self):
        return f"{self.student_id} - {self.name} ({self.program})"

    def enroll_in_course(self, course):
        result = course.enroll_student(self)
        if result == "Enrolled":
            self.courses[course.code] = course
        return result

    def add_grade(self, course_code, grade):
        if course_code in self.courses:
            self.grades[course_code] = grade
            self.courses[course_code].add_grade(self.student_id, grade)

    def calculate_gpa(self):
        if not self.grades:
            return 0.0
        return sum(self.grades.values()) / len(self.grades)

    def get_transcript(self):
        return {code: self.grades[code] for code in self.grades}

    @classmethod
    def get_total_students(cls):
        return len(cls.all_students)

    @classmethod
    def get_average_gpa(cls):
        gpas = [student.calculate_gpa() for student in cls.all_students if student.grades]
        if not gpas:
            return 0.0
        return sum(gpas) / len(gpas)

    @classmethod
    def get_top_students(cls, n):
        students_with_gpa = [(student, student.calculate_gpa()) for student in cls.all_students if student.grades]
        students_with_gpa.sort(key=lambda x: x[1], reverse=True)
        return [(s.student_id, s.name, gpa) for s, gpa in students_with_gpa[:n]]

math_course = Course("MATH101", "Calculus I", "Dr. Smith", 3, 30)
physics_course = Course("PHYS101", "Physics I", "Dr. Johnson", 4, 25)
cs_course = Course("CS101", "Programming Basics", "Prof. Brown", 3, 20)

print(f"Course: {math_course}")
print(f"Available spots in Math: {math_course.get_available_spots()}")

student1 = Student("S001", "Alice Wilson", "alice@university.edu", "Computer Science")
student2 = Student("S002", "Bob Davis", "bob@university.edu", "Mathematics")
student3 = Student("S003", "Carol Lee", "carol@university.edu", "Physics")

print(f"Student: {student1}")
print(f"Total students: {Student.get_total_students()}")

enrollment1 = student1.enroll_in_course(math_course)
enrollment2 = student1.enroll_in_course(cs_course)
enrollment3 = student2.enroll_in_course(math_course)

print(f"Alice's enrollment in Math: {enrollment1}")
print(f"Math course enrollment count: {math_course.get_enrollment_count()}")

student1.add_grade("MATH101", 85.5)
student1.add_grade("CS101", 92.0)
student2.add_grade("MATH101", 78.3)

print(f"Alice's GPA: {student1.calculate_gpa()}")
print(f"Alice's transcript: {student1.get_transcript()}")

math_course.add_grade("S001", 85.5)
math_course.add_grade("S002", 78.3)

course_stats = math_course.get_course_statistics()
print(f"Math course statistics: {course_stats}")

total_enrollments = Course.get_total_enrollments()
print(f"Total enrollments across all courses: {total_enrollments}")

average_gpa = Student.get_average_gpa()
print(f"University average GPA: {average_gpa}")

top_students = Student.get_top_students(2)
print(f"Top 2 students: {top_students}")

for i in range(25):
    temp_student = Student(f"S100{i}", f"Student {i}", f"student{i}@uni.edu", "General")
    result = temp_student.enroll_in_course(math_course)

print(f"Course full status: {math_course.is_full()}")
print(f"Waitlist size: {len(math_course.waitlist) if hasattr(math_course, 'waitlist') else 0}")
