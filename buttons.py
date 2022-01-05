import tkinter

from test import *


class DefaultButton(tk.Frame):
    """Дефолтный конструктор кнопок"""
    def __init__(self, toolbar, text, command, image, side='l'):
        super().__init__(toolbar)
        btn_open_dialog = tk.Button(toolbar, text=text, command=command, bg='#e3f2fd', bd=0,
                                    compound=tk.TOP, image=image)
        if side == 'r':
            btn_open_dialog.pack(side=tk.RIGHT)
        elif side == 'c':
            btn_open_dialog.pack(side=tk.LEFT, expand = tk.YES)
        else:
            btn_open_dialog.pack(side=tk.LEFT)


class AddButton(DefaultButton):
    """Кнопка добавления вопроса"""
    def __init__(self, frame):
        self.img = tk.PhotoImage(file='icons/add.png')
        super().__init__(toolbar=frame.toolbar,
                         text='Добавить Вопрос',
                         command=AddFrame,
                         image=self.img,
                         side = 'c')


class DelButton(DefaultButton):
    """Кнопка удаления вопроса"""
    def __init__(self, frame):
        self.img = tk.PhotoImage(file='icons/delete.png')
        self.frame = frame
        super().__init__(frame.toolbar,
                         text='Удалить Вопрос',
                         command=lambda: self.safe_del(),
                         image=self.img,
                         side = 'c')

    def safe_del(self):
        """Срабатывание только при выбранном вопросе"""
        try:
            DelFrame(self.frame.get_user_id())
        except:
            pass


class EditQuestButton(DefaultButton):
    """Кнопка редактирования вопроса"""
    def __init__(self, frame):
        self.img = tk.PhotoImage(file='icons/edit.png')
        self.frame = frame
        super().__init__(frame.toolbar,
                         text='Изменить Вопрос',
                         command=lambda: self.safe_edit(),
                         image=self.img,
                         side = 'c')

    def safe_edit(self):
        """Срабатывание только при выбранном вопроса"""
        try:
            EditFrame(self.frame.get_user_id())
        except:
            pass


class YesAnswerButton(DefaultButton):
    """Кнопка ответа ДА"""
    def __init__(self, frame):
        self.img = tk.PhotoImage(file='icons/yes.png')
        self.frame = frame
        super().__init__(frame.toolbar,
                         text='Да',
                         command=lambda: self.safe_Yes(),
                         image=self.img,
                         side='c')

    def safe_Yes(self):
        """Срабатывание только при выбранном товаре"""
        try:
            AddToTestFrame(self.frame.get_user_id())
        except:
            pass


class NoAnswerButton(DefaultButton):
    def __init__(self, frame):
        self.img = tk.PhotoImage(file='icons/no.png')
        self.frame = frame
        super().__init__(frame.toolbar,
                         text='Нет',
                         command=lambda: self.safe_No(),
                         image=self.img,
                         side='c')

    def safe_No(self):
        """Срабатывание только при выбранном вопросе"""
        try:
            DelFromTestFrame(self.frame.get_user_id())
        except:
            pass


class ShowSymptomsButton(DefaultButton):
    """Кнопка просмотр симптомов"""
    def __init__(self, frame):
        self.img = tk.PhotoImage(file='icons/list.png')
        self.frame = frame
        super().__init__(frame.toolbar,
                         text='Симптомы',
                         command=lambda: frame.show_questions(),
                         image=self.img)


class DelSymptomsButton(DefaultButton):
    """Кнопка сброса"""
    def __init__(self, frame):
        self.img = tk.PhotoImage(file='icons/again.png')
        self.frame = frame
        super().__init__(frame.toolbar,
                         text='Сбросить',
                         command=lambda: CleanProgress(),
                         image=self.img)


class ResultButton(DefaultButton):
    """Кнопка просмотра результата"""
    def __init__(self, frame):
        self.img = tk.PhotoImage(file='icons/result.png')
        super().__init__(frame.toolbar,
                         text='Результат',
                         command=lambda: AnamnesisFrame(frame.session_username),
                         image=self.img,
                         side='r')


class ShowAnswersButton(DefaultButton):
    """Кнопка сохранения ответов пациента"""
    def __init__(self, frame):
        self.img = tk.PhotoImage(file='icons/save.png')
        super().__init__(frame.toolbar,
                         text='Сохранить',
                         command=lambda: ShowAnswersFrame(frame.session_username),
                         image=self.img,
                         side='r')


class ShowResultButton(DefaultButton):
    """Кнопка проверки результата"""
    def __init__(self, frame):
        self.img = tk.PhotoImage(file='icons/check.png')
        self.frame = frame
        super().__init__(frame.toolbar,
                         text='Проверка результата',
                         command=lambda: self.safe_change(),
                         image=self.img)

    def safe_change(self):
        """Срабатывание только при выборе"""
        try:
            ChangeStatusFrame(self.frame.get_user_id())
        except:
            pass


class DelResButton(DefaultButton):
    """Кнопка удаления результата"""
    def __init__(self, frame):
        self.img = tk.PhotoImage(file='icons/delete.png')
        self.frame = frame
        super().__init__(frame.toolbar,
                         text='Удалить результат',
                         command=lambda: self.safe_del_order(),
                         image=self.img)

    def safe_del_order(self):
        """Срабатывание только при выбранном заказе"""
        try:
            RmFrame(self.frame.get_user_id())
        except:
            pass


class UpdateButton(DefaultButton):
    """Кнопка перезагрузки дерева отображения"""
    def __init__(self, frame):
        self.img = tk.PhotoImage(file='icons/updating.png')
        super().__init__(frame.toolbar,
                         text='Обновить',
                         command=lambda: frame.view_data(),
                         image=self.img,
                         side='r')