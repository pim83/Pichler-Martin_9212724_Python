from datetime import datetime
from typing import List
from abc import ABC, abstractmethod


class Assessment(ABC):
    def __init__(self, grade: float, evaluation_date: datetime):
        self.grade = grade
        self.evaluation_date = evaluation_date
    
    def to_dict(self):
        return {
            "type": self.__class__.__name__,
            "grade": self.grade,
            "evaluation_date": self.evaluation_date.isoformat()
        }

    @abstractmethod
    def info(self):
        pass  


class WrittenExam(Assessment):
    def __init__(self, grade: float, evaluation_date: datetime, exam_duration: int):
        super().__init__(grade, evaluation_date)
        self.exam_duration = exam_duration

    def to_dict(self):
        data = super().to_dict()
        data["exam_duration"] = self.exam_duration
        return data

    def info(self):
        return (
            f"Note: {self.grade}, "
            f"Bewertet am: {self.evaluation_date}, "
            f"Dauer der Prüfung: {self.exam_duration}"
        )  


class Project(Assessment):
    def __init__(self, grade: float, evaluation_date: datetime, pages_required):
        super().__init__(grade, evaluation_date)
        self.pages_required = pages_required

    def to_dict(self):
        return {
            "type": "Project",
            "grade": self.grade,
            "evaluation_date": self.evaluation_date.isoformat(),
            "pages_required": self.pages_required
        }

    def info(self):
        return (
            f"Note: {self.grade}, "
            f"Bewertet am: {self.evaluation_date}, "
            f"Benötigte Seitenanzahl: {self.pages_required}"
        )


class Presentation(Assessment):
    def __init__(self, grade: float, evaluation_date: datetime, presentation_duration: int):
        super().__init__(grade, evaluation_date)
        self.presentation_duration = presentation_duration

    def to_dict(self):
        return {
            "type": "Presentation",
            "grade": self.grade,
            "evaluation_date": self.evaluation_date.isoformat(),
            "presentation_duration": self.presentation_duration
        }
    
    def info(self):
        return (
            f"Note: {self.grade}, "
            f"Bewertet am: {self.evaluation_date}, "
            f"Dauer der Präsentation: {self.presentation_duration}"
        )
    

class Module:
    def __init__(self, module_ID: str, module_name: str, module_ects: int, assessment: Assessment):
        self.module_ID = module_ID
        self.module_name = module_name
        self.module_ects = module_ects
        self.assessment = assessment


class Semester:
    def __init__(self, semester_number: int):
        self.semester_number = semester_number
        self.modules = []
    
    def add_module(self, module: Module):
        self.modules.append(module)


class CourseOfStudy:
    def __init__(self, study_name: str, study_start_date: datetime, semesters: List[Semester]):
        self.study_name = study_name
        self.study_start_date = study_start_date
        self.semesters = semesters