import tkinter as tk
from tkinter import ttk
from connector import udb
from tkinter import messagebox as ms
from navigator import Start


class EnterFrame:
    """Окно входа/регистрации"""
    def __init__(self, frame):
        self.frame = frame
        self.frame.title("МедТест")
        self.frame.geometry("+650+350")
        self.regfr = tk.Frame(self.frame)
        self.logfr = tk.Frame(self.frame)
        self.db = udb
        self.login_frame()
        self.frame.mainloop()

    def login_frame(self):
        """Виджеты логина"""
        head = tk.Label(self.logfr, text='Медицинский Тест', bg="#e3f2fd", width="25", font=('', 18), pady=10)
        head.grid(row=0, column=0, columnspan=2)
        label_username = tk.Label(self.logfr, text='Логин: ')
        label_username.grid(row=1, column=0, padx=20, pady=10)
        label_password = tk.Label(self.logfr, text='Пароль: ')
        label_password.grid(row=2, column=0, padx=20, pady=10)
        self.entry_username = ttk.Entry(self.logfr)
        self.entry_username.grid(row=1, column=1, padx=20, pady=10)
        self.entry_password = ttk.Entry(self.logfr, show='*')
        self.entry_password.grid(row=2, column=1, padx=20, pady=10)
        button_login = ttk.Button(self.logfr, text='Вход', width = '20',
                                  command=lambda: self.login(self.entry_username.get(), self.entry_password.get()))
        button_login.grid(row=3, column=0, padx=20, pady=10)
        button_register = ttk.Button(self.logfr, text='Регистрация', width = '20', command=self.log_to_reg)
        button_register.grid(row=3, column=1, padx=20, pady=10)

        self.logfr.pack()

    def login(self, username, password):
        self.db.find_user_db(username, password)
        if self.db.c.fetchall():
            self.logfr.pack_forget()
            Start(username)
        else:
            ms.showerror('Ошибка входа', "Неверный логин или пароль.")

    def log_to_reg(self):
        self.logfr.pack_forget()
        self.register_frame()

    def register_frame(self):
        """Виджеты регистрации"""
        head = tk.Label(self.regfr, text='Регистрация',bg="#e3f2fd", width="25", font=('', 18), padx=5, pady=10)
        head.grid(row=0, column=0, columnspan=2)
        lbl_unm = tk.Label(self.regfr, text='Логин: ')
        lbl_unm.grid(row=1, column=0, padx=20, pady=10)
        lbl_pwd = tk.Label(self.regfr, text='Пароль: ')
        lbl_pwd.grid(row=2, column=0, padx=20, pady=10)
        lbl_umode = tk.Label(self.regfr, text='Статус: ')
        lbl_umode.grid(row=3, column=0, padx=20, pady=10)
        self.entry_username = ttk.Entry(self.regfr)
        self.entry_username.grid(row=1, column=1, padx=20, pady=10)
        self.entry_password = ttk.Entry(self.regfr, show='*')
        self.entry_password.grid(row=2, column=1, padx=20, pady=10)
        self.cbox_umode = ttk.Combobox(self.regfr,
                                       state="readonly",
                                       width = '17',
                                       values=[u'Эксперт', u'Доктор', u'Пациент'])
        self.cbox_umode.grid(row=3, column=1, padx=20, pady=10)
        self.cbox_umode.current(2)
        button_register = ttk.Button(self.regfr, text='Войти', width = '20',
                                     command=lambda:
                                     self.register(self.entry_username.get(),
                                                   self.entry_password.get(),
                                                   self.cbox_umode.get()))
        button_register.grid(row=4, column=0, padx=20, pady=30)
        button_login = ttk.Button(self.regfr, text='Назад', width = '20', command=self.reg_to_log)
        button_login.grid(row=4, column=1, padx=20, pady=30)
        self.regfr.pack()

    def register(self, username, password, umode):
        self.db.find_username_db(username)
        if self.db.c.fetchall():
            ms.showerror('Повторный логин','Пользователь уже существует.')
        elif password == '':
            ms.showerror('Пустое поле','Введите пароль.')
        elif username == '':
            ms.showerror('Пустое поле','Введите логин.')
        else:
            self.db.create_user_db(username, password, umode)
            self.regfr.pack_forget()
            Start(username)

    def reg_to_log(self):
        self.regfr.pack_forget()
        self.login_frame()