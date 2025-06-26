from dataclasses import dataclass, field
from datetime import datetime
from typing import List
from enum import Enum


class StudyMode(Enum):
    FULL_TIME = "Full-time"
    PART_TIME_1 = "Part-time 1"
    PART_TIME_2 = "Part-time 2"

@dataclass
class Assessment:
    grade: float
    assessment_date: datetime

@dataclass
class Module:
    ID: str
    name: str
    ects: int
    type_of_assessment: str
    assessments: List[Assessment] = field(default_factory=list)

@dataclass
class Semester:
    semester_number: int
    modules: List[Module] = field(default_factory=list)

@dataclass
class CourseOfStudy: 
    name: str
    student: str
    start_date: datetime
    module_duration: int  # in months
    study_mode: StudyMode
    semesters: List[Semester] = field(default_factory=list)
    
        
