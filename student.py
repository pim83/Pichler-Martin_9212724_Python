from study import CourseOfStudy
from typing import List


class Student:
    def __init__(self, student_name: str, matrikel_number: int):
        self.student_name = student_name
        self.matrikel_number = matrikel_number
        self.courses_of_study: List[CourseOfStudy] = []
    
    def add_course_of_study(self, course_of_study: CourseOfStudy):
        self.courses_of_study.append(course_of_study)