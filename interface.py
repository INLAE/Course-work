from buttons import *


class MainFrame(tk.Frame):
    """Дефолтное окно интерфейса"""
    def __init__(self, root_frame):
        super().__init__(root_frame)
        self.root_frame = root_frame
        self.root_frame.bind("<FocusIn>", self.handle_focus_user)
        self.tree = ttk.Treeview(self)  #дерево отображения записей из бд
        self.db = qdb
        self.toolbar = tk.Frame(bg="#e3f2fd", bd=2)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

    def handle_focus_user(self, event):
        """Обновление отображаемых данных при попадании фрейма в фокус"""
        if event.widget == self.root_frame:
            self.view_data()

    def view_data(self):
        """"Метод передачи данных из бд sql в дерево отображения"""
        self.db.view_data_db()
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def get_user_id(self):
        """Получение id выбранной записи"""
        selected = self.tree.focus()
        return self.tree.item(selected, 'values')[0]


class ExpertFrame(MainFrame):
    """Юзеринтерфейс ЭКСПЕРТА"""
    def __init__(self, root_frame):
        super().__init__(root_frame)
        self.tree = ttk.Treeview(self, columns=('№', 'Question', 'costs'),
                                 height=25, show='headings', selectmode="browse")
        self.scroll = tk.Scrollbar(self, command=self.tree.yview)
        self.init_user()

    def init_user(self):
        self.view_data()
        update_button = UpdateButton(self)
        add_button = AddButton(self)
        edit_button = EditQuestButton(self)
        del_button = DelButton(self)

        self.tree.column('№', width=30, anchor=tk.CENTER)
        self.tree.column('Question', width=365, anchor=tk.CENTER)
        self.tree.column('costs', width=150, anchor=tk.CENTER)

        self.tree.heading('№', text='№')
        self.tree.heading('Question', text='Question')
        self.tree.heading('costs', text='Points')

        self.tree.pack(side=tk.LEFT)
        self.scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=self.scroll.set)


class PatientFrame(MainFrame):
    """Юзеринтерфейс ПАЦИЕНТА"""
    def __init__(self, root_frame, username):
        super().__init__(root_frame)
        self.session_username = username
        self.tree = ttk.Treeview(self, columns=('№', 'Вопрос', 'Баллы', 'Состояние'),
                                 height=15, show='headings', selectmode="browse")
        self.scroll = tk.Scrollbar(self, command=self.tree.yview)
        self.init_user()

    def init_user(self):
        self.view_data()
        cart_button = ShowSymptomsButton(self)
        del_cart_button = DelSymptomsButton(self)
        add_to_cart_button = YesAnswerButton(self)
        rm_from_cart_button = NoAnswerButton(self)
        order_button = ResultButton(self)
        show_orders = ShowAnswersButton(self)
        update_button = UpdateButton(self)

        self.tree.column('№', width=50, anchor=tk.CENTER)
        self.tree.column('Вопрос', width=500, anchor=tk.CENTER)
        self.tree.column('Баллы', width=75, anchor=tk.CENTER)
        self.tree.column('Состояние', width=75, anchor=tk.CENTER)

        self.tree.heading('№', text='№')
        self.tree.heading('Вопрос', text='Вопрос')
        self.tree.heading('Баллы', text='Баллы')
        self.tree.heading('Состояние', text='Состояние')

        self.tree.pack(side=tk.LEFT)

        self.scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=self.scroll.set)

    def show_questions(self):
        """"метод передачи записей из бд вопросов в дерево"""
        self.db.show_cart_db()
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]


class DoctorFrame(MainFrame):
    """Юзеринтерфейс ВРАЧА"""
    def __init__(self, root_frame):
        super().__init__(root_frame)
        self.db = tdb
        self.tree = ttk.Treeview(self, columns=('№', 'Пациент', 'Вопросы','Баллы', 'Статус'),
                                 height=15, show='headings', selectmode="browse")
        self.scroll = tk.Scrollbar(self, command=self.tree.yview)
        self.init_user()

    def init_user(self):
        self.view_data()
        change_state_button = ShowResultButton(self)
        delete_order_button = DelResButton(self)
        update_button = UpdateButton(self)

        self.tree.column('№', width=50, anchor=tk.CENTER)
        self.tree.column('Пациент', width=50, anchor=tk.CENTER)
        self.tree.column('Вопросы', width=100, anchor=tk.CENTER)
        self.tree.column('Баллы', width=50, anchor=tk.CENTER)
        self.tree.column('Статус', width=50, anchor=tk.CENTER)

        self.tree.heading('№', text='№')
        self.tree.heading('Пациент', text='Пациент')
        self.tree.heading('Вопросы', text='Вопросы')
        self.tree.heading('Баллы', text='Баллы')
        self.tree.heading('Статус', text='Статус')
        self.tree.pack(side=tk.LEFT)
        self.scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=self.scroll.set)



