import json
from datetime import datetime
from pathlib import Path
from student import Student
from study import CourseOfStudy, Semester, Module
from study import WrittenExam, Project, Presentation


class DataHandler:
    FOLDER = Path("data")

    @staticmethod
    def save_student(student: Student, filename: str):
        
        DataHandler.FOLDER.mkdir(exist_ok=True)
        file_path = DataHandler.FOLDER / filename

        data = {
            "student_name": student.student_name,
            "matrikel_number": student.matrikel_number
        }

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        print(f"Student gespeichert: {file_path}")

    @staticmethod
    def load_student(filename: str) -> Student:
        
        file_path = DataHandler.FOLDER / filename

        if not file_path.exists():
            raise FileNotFoundError(f"Student-Datei nicht gefunden: {file_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        student = Student(data["student_name"], data["matrikel_number"])
        return student
    

    @staticmethod
    def load_course_of_study(filename: str) -> CourseOfStudy:
        file_path = DataHandler.FOLDER / filename

        if not file_path.exists():
            raise FileNotFoundError(f"Datei nicht gefunden: {file_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        course = CourseOfStudy(
            study_name=data["study_name"],
            study_start_date=datetime.fromisoformat(data["study_start_date"]),
            semesters=[]
        )

        for semester_data in data["semesters"]:
            semester = Semester(semester_data["semester_number"])

            for module_data in semester_data["modules"]:
                assessment = DataHandler._create_assessment(
                    module_data["assessment"]
                )

                module = Module(
                    module_ID=module_data["module_ID"],
                    module_name=module_data["module_name"],
                    module_ects=module_data["module_ects"],
                    assessment=assessment
                )

                semester.add_module(module)

            course.semesters.append(semester)

        return course

    @staticmethod
    def save_course_of_study(course: CourseOfStudy, filename: str):
        DataHandler.FOLDER.mkdir(exist_ok=True)
        file_path = DataHandler.FOLDER / filename

        data = {
            "study_name": course.study_name,
            "study_start_date": course.study_start_date.isoformat(),
            "semesters": []
        }

        for semester in course.semesters:
            sem_data = {
                "semester_number": semester.semester_number,
                "modules": []
            }

            for module in semester.modules:
                sem_data["modules"].append({
                    "module_ID": module.module_ID,
                    "module_name": module.module_name,
                    "module_ects": module.module_ects,
                    "assessment": module.assessment.to_dict()
                })

            data["semesters"].append(sem_data)

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def _create_assessment(data: dict):
        assessment_type = data["type"]
        evaluation_date = datetime.fromisoformat(data["evaluation_date"])

        if assessment_type == "WrittenExam":
            return WrittenExam(
                grade=data["grade"],
                evaluation_date=evaluation_date,
                exam_duration=data["exam_duration"]
            )

        elif assessment_type == "Project":
            return Project(
                grade=data["grade"],
                evaluation_date=evaluation_date,
                pages_required=data["pages_required"]
            )

        elif assessment_type == "Presentation":
            return Presentation(
                grade=data["grade"],
                evaluation_date=evaluation_date,
                presentation_duration=data["presentation_duration"]
            )

        else:
            raise ValueError(f"Unbekannter Assessment-Typ: {assessment_type}")