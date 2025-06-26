from view_main import MainWindow
from data_handler import save_course_to_file, load_course_from_file, create_empty_course
from study import CourseOfStudy, Semester, Module, Assessment
from datetime import datetime
import os


if __name__ == "__main__":
    file_path = "studium.json"

    # Check if the file exists, if not create an empty course and save it
    if not os.path.exists(file_path):
        course = create_empty_course()
        save_course_to_file(course, file_path)
    else:
        course = load_course_from_file(file_path)

    # start the UI
    app = MainWindow()
    app.mainloop()
