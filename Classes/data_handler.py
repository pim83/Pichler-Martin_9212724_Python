from dataclasses import asdict
from datetime import datetime
from typing import List
import json
from study import CourseOfStudy, Semester, Module, Assessment


def serialize_course(course: CourseOfStudy):
    return {
        "study_name": course.study_name,
        "student_name": course.student_name,
        "study_start_date": course.study_start_date.isoformat(),
        "module_duration": course.module_duration,
        "semesters": [
            {
                "semester_number": semester.semester_number,
                "modules": [
                    {
                        "module_ID": module.module_ID,
                        "module_name": module.module_name,
                        "module_ects": module.module_ects,
                        "assessment": {
                            "grade": module.assessment.grade,
                            "assessment_date": module.assessment.assessment_date.isoformat()
                        }
                    } for module in semester.modules
                ]
            } for semester in course.semesters
        ]
    }


def deserialize_course(data: dict) -> CourseOfStudy:
    return CourseOfStudy(
        study_name=data["study_name"],
        student_name=data["student_name"],
        study_start_date=datetime.fromisoformat(data["study_start_date"]),
        module_duration=data["module_duration"],
        semesters=[
            Semester(
                semester_number=sem["semester_number"],
                modules=[
                    Module(
                        module_ID=mod["module_ID"],
                        module_name=mod["module_name"],
                        module_ects=mod["module_ects"],
                        assessment=Assessment(
                            grade=mod["assessment"]["grade"],
                            assessment_date=datetime.fromisoformat(mod["assessment"]["assessment_date"])
                        )
                    ) for mod in sem["modules"]
                ]
            ) for sem in data["semesters"]
        ]
    )


def save_course_to_file(course: CourseOfStudy, filename: str):
    with open(filename, "w") as f:
        json.dump(serialize_course(course), f, indent=4)


def load_course_from_file(filename: str) -> CourseOfStudy:
    with open(filename) as f:
        data = json.load(f)
    return deserialize_course(data)


def create_empty_course():
    return CourseOfStudy(
        study_name="",
        student_name="",
        study_start_date=datetime.now(),
        module_duration=0,
        semesters=[
            Semester(
                semester_number=i + 1,
                modules=[
                    Module(
                        module_ID="",
                        module_name="",
                        module_ects=0,
                        assessment=Assessment(
                            grade=0.0,
                            assessment_date=datetime.now()
                        )
                    ) for _ in range(5)  # 5 leere Module pro Semester
                ]
            ) for i in range(8)  # 8 Semester
        ]
    )