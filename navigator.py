from interface import PatientFrame, ExpertFrame, DoctorFrame
from connector import root_frame, udb


class Start:
    """Класс вызова визуальных интерфейсов по ролям"""
    def __init__(self, username):
        self.db = udb
        self.username = username
        self.set_usermode()
        self.start_test()

    def start_test(self):
        if self.usermode == 'Эксперт':
            root_frame.title(f"MedTest: {self.username}")
            app = ExpertFrame(root_frame)
            app.pack()

        elif self.usermode == 'Пациент':
            root_frame.title(f"MedTest: Patient {self.username}")
            app = PatientFrame(root_frame, self.username)
            app.pack()

        elif self.usermode == 'Доктор':
            root_frame.title(f"MedTest: Doctor {self.username}")
            app = DoctorFrame(root_frame)
            app.pack()

    def set_usermode(self):
        """Получение юзермода по юзернейму из дб"""
        self.db.find_usermode_db(self.username)
        self.usermode = self.db.c.fetchone()[0]
