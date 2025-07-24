from collections import defaultdict

class GradeManager:
    def __init__(self):
        """
        Initialize the grade manager with appropriate defaultdict structures
        Use defaultdict to avoid key existence checks
        """
        self.grades = defaultdict(lambda: defaultdict(list))

    def add_grade(self, student_name, subject, grade):
        """
        Add a grade for a student in a specific subject
        Args:
            student_name (str): Name of the student
            subject (str): Subject name
            grade (float): Grade value (0-100)
        """
        self.grades[student_name][subject].append(grade)

    def get_student_average(self, student_name):
        """
        Calculate average grade for a student across all subjects
        Args:
            student_name (str): Name of the student
        Returns:
            float: Average grade or 0 if student not found
        """
        subjects = self.grades.get(student_name, {})
        all_grades = []
        for grades in subjects.values():
            all_grades.extend(grades)
        if not all_grades:
            return 0
        return sum(all_grades) / len(all_grades)

    def get_subject_statistics(self, subject):
        """
        Get statistics for a specific subject across all students
        Args:
            subject (str): Subject name
        Returns:
            dict: Contains 'average', 'highest', 'lowest', 'student_count'
        """
        subject_grades = []
        for student in self.grades:
            subject_grades.extend(self.grades[student][subject])
        if not subject_grades:
            return {'average': 0, 'highest': 0, 'lowest': 0, 'student_count': 0}
        return {
            'average': sum(subject_grades) / len(subject_grades),
            'highest': max(subject_grades),
            'lowest': min(subject_grades),
            'student_count': len([student for student in self.grades if self.grades[student][subject]])
        }

    def get_top_students(self, n=3):
        """
        Get top N students based on their overall average
        Args:
            n (int): Number of top students to return
        Returns:
            list: List of tuples (student_name, average_grade)
        """
        averages = []
        for student in self.grades:
            avg = self.get_student_average(student)
            averages.append((student, avg))
        averages.sort(key=lambda x: x[1], reverse=True)
        return averages[:n]

    def get_failing_students(self, passing_grade=60):
        """
        Get students who are failing (average below passing grade)
        Args:
            passing_grade (float): Minimum grade to pass
        Returns:
            list: List of tuples (student_name, average_grade)
        """
        failing = []
        for student in self.grades:
            avg = self.get_student_average(student)
            if avg < passing_grade:
                failing.append((student, avg))
        return failing

manager = GradeManager()

grades_data = [
    ("Alice", "Math", 85), ("Alice", "Science", 92), ("Alice", "English", 78),
    ("Bob", "Math", 75), ("Bob", "Science", 68), ("Bob", "English", 82),
    ("Charlie", "Math", 95), ("Charlie", "Science", 88), ("Charlie", "History", 91),
    ("Diana", "Math", 55), ("Diana", "Science", 62), ("Diana", "English", 70),
    ("Eve", "Math", 88), ("Eve", "Science", 94), ("Eve", "English", 86), ("Eve", "History", 89)
]

for student, subject, grade in grades_data:
    manager.add_grade(student, subject, grade)

print("Alice's average:", manager.get_student_average("Alice"))
print("Math statistics:", manager.get_subject_statistics("Math"))
print("Top 3 students:", manager.get_top_students(3))
print("Failing students:", manager.get_failing_students(75))
