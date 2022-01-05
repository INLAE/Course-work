import tkinter as tk
from db import QuestionsDB, UsersDB, TestDB
"""Подключение к таблицам бд"""
qdb = QuestionsDB()
udb = UsersDB()
tdb = TestDB()

root_frame = tk.Tk()    # Базовый пустой фрейм
root_frame.resizable(False, False)

