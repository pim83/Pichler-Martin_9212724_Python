from datetime import date
from sys import modules
from student import Student
from dateutil.relativedelta import relativedelta
from data_handler import DataHandler


class StudyViewModel:
    def __init__(self, student: Student):
        self._student = student
        self.course_of_study = student.courses_of_study[0] 

    def get_study_name(self) -> str:
        return self.course_of_study.study_name

    def get_student_name(self) -> str:
        return self._student.student_name
    
    def update_student(self, name: str, matrikel: int):
        self._student.student_name = name
        self._student.matrikel_number = matrikel
        DataHandler.save_student(self._student, "student_9212724.json")

    def get_matrikel_number(self) -> int:
        return self._student.matrikel_number
   
    def get_semester(self, semester_number: int):
        for semester in self.course_of_study.semesters:
            if semester.semester_number == semester_number:
                return semester
        return None

    def get_modules_for_semester(self, semester_number: int):
        semester = self.get_semester(semester_number)
        return semester.modules if semester else []
    
    def get_all_modules(self):
        all_modules = []
        for semester in self.course_of_study.semesters:
            all_modules.extend(semester.modules)
        return all_modules
    
    def get_grade_average(self) -> float:
        modules = self.get_all_modules()
        grades = [m.assessment.grade for m in modules if m.assessment.grade not in (0, None)]
    
        if not grades:
            return 0.0
    
        average = sum(grades) / len(grades)
        return round(average, 2)
    
    def get_all_grades(self) -> list[float]:
        grades = []

        for semester in self.course_of_study.semesters:
            for module in semester.modules:
                grade = module.assessment.grade
                if grade not in (0, None):
                    grades.append(grade)
        return grades
    
    def get_study_progress(self) -> float:
        all_modules = []

        # collect all modules
        for semester in self.course_of_study.semesters:
            all_modules.extend(semester.modules)

        if not all_modules:
            return 0.0

        # completed modules
        completed = [
            m for m in all_modules
            if m.assessment.grade not in (0.0, None)
        ]

        progress = len(completed) / len(all_modules)
        return round(progress, 1)
    
    def get_module_progress_text(self) -> str:
        total_modules = 0
        completed_modules = 0

        for semester in self.course_of_study.semesters:
            for module in semester.modules:
                total_modules += 1
                if module.assessment.grade not in (0, None):
                    completed_modules += 1

        return f"{completed_modules}/{total_modules}"
    
    def get_estimated_end_date(self) -> date:
        open_modules = 0

        for semester in self.course_of_study.semesters:
            for module in semester.modules:
                if module.assessment.grade in (0, None):
                    open_modules += 1

        months_needed = open_modules * 2

        start_date = self.course_of_study.study_start_date
        end_date = start_date + relativedelta(months=months_needed)

        return end_date.strftime("%m/%Y")
    
    def get_ects_progress_string(self) -> str:
        completed_ects = 0

        for semester in self.course_of_study.semesters:
            for module in semester.modules:

                if module.assessment.grade not in (0, None):
                    completed_ects += module.module_ects

        return f"{completed_ects}/120"
    
    def get_thesis_start_date(self) -> date:
        earned_ects = sum(
            m.module_ects
            for semester in self.course_of_study.semesters
            for m in semester.modules
            if m.assessment.grade not in (0, None)
        )

        remaining_ects = max(0, 120 - earned_ects)
        months_needed = (remaining_ects / 5) * 2
        start_date = self.course_of_study.study_start_date

        thesis_start_date = start_date + relativedelta(months=int(months_needed))

        return thesis_start_date.strftime("%m/%Y")
    
    def update_module_grade(self, module_id: str, new_grade: float):
        for semester in self.course_of_study.semesters:
            for module in semester.modules:
                if module.module_ID == module_id:
                    module.assessment.grade = new_grade

                    DataHandler.save_course_of_study(self.course_of_study, "study_FS_BAAKI.json")
                    return