import sqlite3


class MedicineDB:
    """Создание бд медтеста"""
    def __init__(self):
        self.conn = sqlite3.connect('test.db')
        self.c = self.conn.cursor()
        self._create_questions_db()
        self._create_users_db()
        self._create_orders_db()

    def _create_questions_db(self):
        """Создание таблицы вопросов"""
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS questions (id INTEGER PRIMARY KEY, description TEXT NOT NULL, costs REAL NOT 
            NULL, cart TEXT)''')
        self.conn.commit()

    def _create_users_db(self):
        """Создание таблицы юзеров"""
        self.c.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT NOT NULL PRIMARY KEY,password TEXT NOT NULL, 
                role TEXT NOT NULL);''')
        self.conn.commit()

    def _create_orders_db(self):
        """Создание таблицы заказов"""
        self.c.execute('''CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY, username TEXT NOT NULL, 
                goods_ids TEXT NOT NULL, score REAL NOT NULL, state TEXT NOT NULL);''')
        self.conn.commit()


class QuestionsDB(MedicineDB):
    """Таблица вопросов"""
    def __init__(self):
        super().__init__()
        self.clean_cart_db()    # При первой инициации в сессии очистка состояний корзины

    def insert_data_db(self, description, cost):
        """Добавление вопроса в бд"""
        self.c.execute('''INSERT INTO questions(description, costs, cart) VALUES (?, ?, ?)''',
                       (description, cost, 'Нет'))
        self.conn.commit()

    def edit_record_db(self, description, cost, sel_id):
        """Обновление информации о вопросе в бд"""
        self.c.execute('''UPDATE questions SET description=?, costs=? WHERE ID=?''', (description, cost, sel_id))
        self.conn.commit()

    def add_to_cart_db(self, sel_id):
        """Смена статуса на \"Да\" в бд"""
        self.c.execute('''UPDATE questions SET cart=? WHERE ID=?''', ('Да', sel_id))
        self.conn.commit()

    def rm_from_cart_db(self, sel_id):
        """Смена статуса на \"Нет"\" в бд"""
        self.c.execute('''UPDATE questions SET cart=? WHERE ID=?''', ('Нет', sel_id))
        self.conn.commit()

    def view_data_db(self):
        """Получение всех записей из таблицы вопросов"""
        self.c.execute('''SELECT * FROM questions''')

    def del_record_db(self, sel_id):
        """Удаление вопроса по id"""
        self.c.execute('''DELETE FROM questions WHERE id=?''', (sel_id,))
        self.conn.commit()


    def show_cart_db(self):
        """Получение всех вопросов с состоянием \"Да"\""""
        description = ('%Да%',)
        self.c.execute('''SELECT * FROM questions WHERE cart LIKE ?''', description)

    def default_data_db(self, sel_id):
        """Получение записи вопроса по id"""
        self.c.execute('''SELECT * FROM questions WHERE id=?''', (sel_id,))


    def clean_cart_db(self):
        """Смена састояния всех вопросов на \"Нет\""""
        self.c.execute('''UPDATE questions SET cart = "Нет"''')
        self.conn.commit()


class UsersDB(MedicineDB):
    """Таблица юзеров"""
    def __init__(self):
        super().__init__()

    def find_user_db(self, username, password):
        """Получение юзера по юзернейму и паролю"""
        self.c.execute('''SELECT * FROM users WHERE username = ? and password = ?''', (username, password))

    def create_user_db(self, username, password, role):
        """Запись юзера в бд"""
        self.c.execute('''INSERT INTO users(username,password, role) VALUES(?,?,?)''', (username, password, role))
        self.conn.commit()

    def find_username_db(self, username):
        """Проверка наличия юзернейма в бд"""
        self.c.execute('''SELECT username FROM users WHERE username = ?''', (username,))

    def find_usermode_db(self, username):
        """Получение роли по юзернейму из бд"""
        self.c.execute('''SELECT role FROM users WHERE username = ?''', (username,))


class TestDB(MedicineDB):
    """Таблица вопросов"""
    def __init__(self):
        super().__init__()

    def view_data_db(self):
        """Получение всех записей из таблицы вопросов"""
        self.c.execute('''SELECT * FROM orders''')

    def get_orders_by_username_db(self, username):
        """Получение всех записей о вопросах от юзернейма"""
        self.c.execute('''SELECT ID, SCORE, STATE FROM orders WHERE username = ? ''', (username,))

    def get_total_by_username_db(self, username):
        """Получение total юзернейма"""
        self.c.execute('''SELECT SCORE FROM orders WHERE username = ? ''', (username,))

    def default_data_db(self, sel_id):
        """Получение записи о вопросе по id заказа"""
        self.c.execute('''SELECT * FROM orders WHERE id=?''', (sel_id,))


    def create_order_db(self, username, goods_ids, score):
        """Создание записи о вопросе в бд"""
        self.c.execute('''INSERT INTO orders(username, goods_ids, score, state) VALUES(?,?,?,?)''',
                       (username, goods_ids, score, 'Wait'))
        self.conn.commit()

    def update_order_state_db(self, order_id, state):
        """Обновление статуса вопроса в бд"""
        self.c.execute('''UPDATE orders SET state=? WHERE ID=?''', (state, order_id))
        self.conn.commit()

    def delete_order_db(self, order_id):
        """Удаление записи вопроса из бд"""
        self.c.execute('''DELETE FROM orders WHERE id=?''', (order_id,))
        self.conn.commit()
        print(order_id, ' order deld')