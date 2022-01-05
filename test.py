from tkinter import ttk
from connector import qdb, tk, tdb
from tkinter import messagebox as ms


class AddFrame(tk.Toplevel):
    """Окно добавления вопроса"""
    def __init__(self):
        super().__init__()
        self.db = qdb
        self.init_child()
        self.geometry('+900+500')
        self.widgets()
        self.width = "90"
        self.grab_set()
        self.focus_set()

    def init_child(self):
        self.title('Добавить вопрос')
        self.btn_ok = ttk.Button(self, text='Добавить')

    def widgets(self):
        self.label_sum = tk.Label(self, text='Баллы:')
        self.label_description = tk.Label(self, text='Вопрос:')
        self.btn_cancel = ttk.Button(self, text='Выход', command=self.destroy)
        self.entry_money = ttk.Entry(self)
        self.entry_description = ttk.Entry(self)
        self.label_description.grid(row=0, column=0, padx=20, pady=10)
        self.label_sum.grid(row=1, column=0, padx=20, pady=10)
        self.entry_description.grid(row=0, column=1, padx=20, pady=10)
        self.entry_money.grid(row=1, column=1, padx=20, pady=10)
        self.btn_cancel.grid(row=2, column=1, padx=30, pady=10)
        self.btn_ok.grid(row=2, column=0, padx=30, pady=10)
        self.btn_ok.bind('<Button-1>', self.safe_set)

    def safe_set(self, event):
        """метод безопасной передачи вопросов в бд"""
        descr = self.entry_description.get()
        pnts = self.entry_money.get()
        if descr == '' or pnts == '':
            ms.showerror('Error!', 'Все поля должны быть заполнены.')
        else:
            try:
                self.try_set(descr, pnts)
                self.destroy()
            except:
                ms.showerror('Error!', 'Баллы должны быть числом.')

    def try_set(self, descr, price):
        self.db.insert_data_db(descr, float(price))


class EditFrame(AddFrame):
    """Окно редактирования вопроса"""
    def __init__(self, sel_id):
        super().__init__()
        self.sel_id = sel_id
        self.default_data()

    def init_child(self):
        self.title('Редактирование вопроса')
        self.btn_ok = ttk.Button(self, text='Готово')

    def try_set(self, descr, price):
        self.db.edit_record_db(descr, float(price), self.sel_id)

    def default_data(self):
        """Подставление старых данных из бд"""
        self.db.default_data_db(self.sel_id)
        row = self.db.c.fetchone()
        self.entry_description.insert(0, row[1])
        self.entry_money.insert(0, row[2])


class DelFrame(tk.Toplevel):
    """Окно подтверждения удаления вопроса"""
    def __init__(self, sel_id):
        super().__init__()
        self.sel_id = sel_id
        self.btn_cancel = ttk.Button(self, text='Нет', command=self.destroy)
        self.label_description = tk.Label(self, text='Подтверждаете?')
        self.db = qdb
        self.init_child()

    def init_child(self):
        self.title('Удаление')
        self.geometry('+400+300')
        self.resizable(False, False)
        self.ok_button()
        self.label_description.grid(row=0, column=0, columnspan=2, padx=20, pady=10)
        self.btn_cancel.grid(row=1, column=1, padx=30, pady=10)
        self.btn_ok.grid(row=1, column=0, padx=30, pady=10)
        self.grab_set()
        self.focus_set()

    def ok_button(self):
        self.btn_ok = ttk.Button(self, text='Удалить')
        self.btn_ok.bind('<Button-1>', lambda event: [self.db.del_record_db(self.sel_id),
                                                      self.destroy()])


class AddToTestFrame(DelFrame):
    """Окно подтверждения добавления вопроса"""
    def __init__(self, sel_id):
        super().__init__(sel_id)
        self.title('Подтверждение')

    def ok_button(self):
        self.btn_ok = ttk.Button(self, text='Да')
        self.btn_ok.bind('<Button-1>', lambda event: [self.db.add_to_cart_db(self.sel_id),
                                                      self.destroy()])


class DelFromTestFrame(DelFrame):
    """Окно подтверждения удаления вопроса"""
    def __init__(self, sel_id):
        super().__init__(sel_id)
        self.title('Удаление')

    def ok_button(self):
        self.btn_ok = ttk.Button(self, text='Готово')
        self.btn_ok.bind('<Button-1>', lambda event: [self.db.rm_from_cart_db(self.sel_id),
                                                      self.destroy()])


class CleanProgress(DelFrame):
    """Окно подтверждения очистки прогресса"""
    def __init__(self):
        super().__init__(0)
        self.title('Удаление')

    def ok_button(self):
        self.btn_ok = ttk.Button(self, text='Удалить всё')
        self.btn_ok.bind('<Button-1>', lambda event: [self.db.clean_cart_db(),
                                                      self.destroy()])


class AnamnesisFrame(tk.Toplevel):
    """Окно подтверждения прохождения теста"""
    def __init__(self, username):
        super().__init__()
        self.db = qdb
        self.odb = tdb
        self.init_child()
        self.username = username

        self.res_ids = ''
        self.total = 0

        self.questions_info()
        self.widgets()

        self.grab_set()
        self.focus_set()

    def questions_info(self):
        """Получение вопросов"""
        self.db.show_cart_db()
        rows = self.db.c.fetchall()
        names, ids = [], []
        for row in rows:
            ids.append(row[0])
            names.append(row[1])
            self.total += row[2]

    def init_child(self):
        self.title('Результат')
        self.geometry('+900+500')
        self.resizable(False, False)
        self.btn_ok = ttk.Button(self, text='Сохранить')

    def widgets(self):

            self.label_total_value = tk.Label(self, text=f'У Вас {self.total} баллов за тест.')
            if self.total > 100:
                self.label_total = tk.Label(self,
                                            text='Риск возникновения сахарного диабета более 80%',
                                            font=("", 14),
                                            bg="#e3f2fd")
                res_ids = 'Риск возникновения сахарного диабета более 80%'

            elif self.total > 50 and self.total < 100:
                self.label_total = tk.Label(self,
                                            text='Риск возникновения сахарного диабета более 50%',
                                            font=("", 14),
                                            bg="#e3f2fd")
                res_ids = 'Риск возникновения сахарного диабета более 50%'
            elif self.total > 20 and self.total < 50:
                self.label_total = tk.Label(self,
                                            text='Риск возникновения сахарного диабета более 20%',
                                            font=("", 14),
                                            bg="#e3f2fd")

                res_ids = 'Риск возникновения сахарного диабета более 20%'
            elif self.total < 20:
                self.label_total = tk.Label(self,
                                            text='Риск возникновения сахарного диабета менее 10%',
                                            font=("", 14),
                                            bg="#e3f2fd")
                res_ids = 'Риск возникновения сахарного диабета менее 10%'

            self.btn_cancel = ttk.Button(self, text='Назад', command=self.destroy)
            self.label_total.grid(row=0, column=0, padx=20, pady=10, columnspan=2)
            self.label_total_value.grid(row=1, column=0, padx=20, pady=10, columnspan=2)
            self.btn_cancel.grid(row=3, column=1, padx=30, pady=10)
            self.btn_ok.grid(row=3, column=0, padx=30, pady=10)
            self.btn_ok.bind('<Button-1>', self.safe_res)



    def safe_res(self, event):
        """Безопасная передача результата"""
        if self.label_total == '':
            ms.showerror('Error!', 'Результат не может быть пустым.')
        else:
            try:
                self.odb.create_order_db(self.username, self.res_ids, self.total)
                self.db.clean_cart_db()
                self.destroy()
            except:
                ms.showerror('Error!', 'Что-то не так...')


class ChangeStatusFrame(tk.Toplevel):
    """Окно смены статуса диагноза"""
    def __init__(self, sel_id):
        super().__init__()
        self.sel_id = sel_id
        self.db = tdb

        self.default_data()
        self.diagnosis()
        self.title('Result Status')
        self.widgets()
        self.geometry('+300+500')
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()

    def diagnosis(self):
        self.label_uid = tk.Label(self, text=f'Пациент: {self.client_id}')
        self.cbox_state = ttk.Combobox(self, state="readonly", values=[u'Принять', u'Отклонить'])
        self.label_state = tk.Label(self, text='Статус диагноза:')
        self.label_rate = tk.Label(self, text=f'{self.total} баллов за тест', font=("", 16))
        if self.total > 100:
            self.label_total = tk.Label(self,
                                        text=f'Критический риск диабета у {self.client_id} - более 80%. '
                                             f'\nРекомендуется лечение в стационаре.',
                                        font=("", 12),
                                        bg="#e3f2fd")

        elif self.total > 50 and self.total < 100:
            self.label_total = tk.Label(self,
                                        text=f'Риск диабета у {self.client_id} более 50%. '
                                             f'\nРекомендуется лечение антибиотиками.',
                                        font=("", 12),
                                        bg="#e3f2fd")
        elif self.total > 20 and self.total < 50:
            self.label_total = tk.Label(self,
                                        text=f'Риск диабета у {self.client_id} более 20%. '
                                             f'\nРекомендуется строгая диета.',
                                        font=("", 12),
                                        bg="#e3f2fd")
        elif self.total < 20:
            self.label_total = tk.Label(self,
                                        text=f'Минимальный риск диабета у {self.client_id} - менее 10%. '
                                             f'\nРекомендуется умеренная диета.',
                                        font=("", 12),
                                        bg="#e3f2fd")

        self.btn_cancel = ttk.Button(self, text='Cancel', command=self.destroy)
        self.btn_ok = ttk.Button(self, text='Update')

    def default_data(self):
        """Получение информации о результате из бд"""
        self.db.default_data_db(self.sel_id)
        row = self.db.c.fetchone()
        self.client_id = row[1]
        self.goods = row[2]
        self.total = row[3]
        self.state = row[4]


    def widgets(self):
        self.cbox_state.current(0)
        self.label_uid.grid(row=0, column=0, padx=20, pady=10, columnspan=2)
        self.label_rate.grid(row=1, column=0, padx=20, pady=10, columnspan=2)
        self.label_total.grid(row=2, column=0, padx=20, pady=10, columnspan=2)
        self.cbox_state.grid(row=3, column=0, padx=20, pady=10, columnspan=2)
        self.btn_ok.grid(row=4, column=0, padx=20, pady=10)
        self.btn_cancel.grid(row=4, column=1, padx=20, pady=10)
        self.btn_ok.bind('<Button-1>', lambda event: [self.db.update_order_state_db(self.sel_id, self.cbox_state.get()),
                                                      self.destroy()])


class RmFrame(DelFrame):
    """Окно подтверждения удаления"""
    def __init__(self, sel_id):
        super().__init__(sel_id)
        self.db = tdb
        self.title('Удаление')

    def ok_button(self):
        self.btn_ok = ttk.Button(self, text='Готово')
        self.btn_ok.bind('<Button-1>', lambda event: [self.db.delete_order_db(self.sel_id),
                                                      self.destroy()])


class ShowAnswersFrame(tk.Toplevel):
    """Окно просмотра ответов"""
    def __init__(self, uid):
        super().__init__()
        self.uid = uid
        self.db = tdb
        self.tree = ttk.Treeview(self, columns=('№', 'Баллы', 'Состояние'), height=15, show='headings',
                                 selectmode="browse")   # Дерево отображения заказов юзера
        self.scroll = tk.Scrollbar(self, command=self.tree.yview)
        self.init_child()
        self.title("Мои ответы")
        self.geometry('225x150+300+300')
        self.grab_set()
        self.focus_set()

    def init_child(self):
        self.get_data_by_user()

        self.tree.column('№', width=75, anchor=tk.CENTER)
        self.tree.column('Баллы', width=77, anchor=tk.CENTER)
        self.tree.column('Состояние', width=50, anchor=tk.CENTER)

        self.tree.heading('№', text='№')
        self.tree.heading('Баллы', text='Баллы')
        self.tree.heading('Состояние', text='Состояние')
        self.tree.pack(side=tk.LEFT)
        self.scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=self.scroll.set)

    def get_data_by_user(self):
        """Передача данных об ответах из бд в дерево отображения"""
        self.db.get_orders_by_username_db(self.uid)
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]