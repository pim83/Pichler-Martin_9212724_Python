from dataclasses import dataclass, field
from datetime import datetime
from typing import List


@dataclass
class Assessment:
    grade: float
    assessment_date: datetime

@dataclass
class Module:
    module_ID: str
    module_name: str
    module_ects: int
    assessment: Assessment

@dataclass
class Semester:
    semester_number: int
    modules: List[Module] = field(default_factory=list)

@dataclass
class CourseOfStudy: 
    study_name: str
    student_name: str
    study_start_date: datetime
    module_duration: int  # in months
    semesters: List[Semester] = field(default_factory=list)
    
        
