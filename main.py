from service.data_handler import DataHandler
from view.view_main import MainWindow
from service.study_viewmodel import StudyViewModel


if __name__ == "__main__":

    # initialize data
    student = DataHandler.load_student("student_9212724.json")
    course_of_study = DataHandler.load_course_of_study("study_FS_BAAKI.json")
    student.add_course_of_study(course_of_study)
    study_viewmodel = StudyViewModel(student)

    # start the UI
    app = MainWindow(study_viewmodel)
    app.mainloop()

