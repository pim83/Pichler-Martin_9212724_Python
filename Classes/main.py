from view_main import MainWindow
from data_handler import save_course_to_file, load_course_from_file, create_empty_course
from study import CourseOfStudy
import os


# data file must be in the project directory
file_path = "studium.json"


def initialize_data(path: str) -> CourseOfStudy:
    
    # Check if the file exists, if not create an empty course and save it
    if not os.path.exists(path):
        data = create_empty_course()
        save_course_to_file(data, path)
    else:
        data = load_course_from_file(path)

    return data


def on_closing():
    app.close_all_plots()
    app.destroy() 


if __name__ == "__main__":

    # Initialize data
    study_data = initialize_data(file_path)

    # start the UI
    app = MainWindow(study_data)
    app.protocol("WM_DELETE_WINDOW", on_closing)
    app.mainloop()