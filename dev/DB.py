import psycopg2


class UsersDB:
    """
    База данных heroku PostgreSQL
    """

    def __init__(self):
        self.connection = psycopg2.connect(host="----",
                                           database="----",
                                           user="----",
                                           port="----",
                                           password="----")
        self.cursor = self.connection.cursor()
        # TABLE users_database
        #                   (ID             INT       PRIMARY KEY,
        #                   USER_ID         INT,
        #                   SUBSCRIPTION    BOOL,
        #                   CURRENCY        STRING);

    def user_exists_in_database(self, user_id):
        """
        Проверяет есть ли пользователь с user_id в базе данных
        """
        with self.connection:
            self.cursor.execute(
                f'SELECT * FROM users_database WHERE USER_ID = {user_id}')
            res = self.cursor.fetchall()
            return bool(len(res))

    def add_user(self, user_id, subscription=True, currency="RUB"):
        """
        Добавляет пользователя в базу данных, по умолчанию ставит ему валюту RUB
        """
        with self.connection:
            self.cursor.execute("SELECT * FROM users_database")
            num = len(self.cursor.fetchall())
            if not self.user_exists_in_database(user_id):
                self.cursor.execute(
                    "INSERT INTO users_database (ID, USER_ID, SUBSCRIPTION, CURRENCY)" +
                    f" VALUES {(num + 1, user_id, subscription, currency)}")

    def update_user(self, user_id, subscription=None, currency=None):
        """
        Обновляет информацию о пользователе в базе данных (subscription и currency, если их передали)
        """
        with self.connection:
            if self.user_exists_in_database(user_id):
                if currency is None:
                    self.cursor.execute(
                        f"UPDATE users_database SET SUBSCRIPTION = {subscription} WHERE USER_ID = {user_id}")
                elif subscription is None:
                    self.cursor.execute(
                        f"UPDATE users_database SET CURRENCY = '{currency}' WHERE USER_ID = {user_id}")
                else:
                    self.cursor.execute(
                        f"UPDATE users_database SET SUBSCRIPTION = {subscription} " +
                        f"CURRENCY = '{currency}' WHERE USER_ID = {user_id}")

            else:
                self.add_user(user_id)

    def user_is_subscribed(self, user_id):
        """
        Проверяет подписан ли пользователь с user_id
        :return: True или False
        """
        with self.connection:
            if self.user_exists_in_database(user_id):
                self.cursor.execute(
                    f"SELECT SUBSCRIPTION FROM users_database WHERE USER_ID = {user_id}")
                return self.cursor.fetchone()[0]
            else:
                return False

    def get_currency(self, user_id):
        """
        Возвращает валюту выбранную пользователем с user_id,
        если пользователь не в базе данных - возвращает None
        """
        with self.connection:
            if self.user_exists_in_database(user_id):
                self.cursor.execute(
                    f"SELECT CURRENCY FROM users_database WHERE USER_ID = {user_id}")
                return self.cursor.fetchone()[0]
            else:
                return None

    def subscribed_users(self):
        """
        Возвращает список всех подписанных пользователей (их user_id и валюту)
        """
        with self.connection:
            self.cursor.execute("SELECT USER_ID, CURRENCY FROM users_database WHERE SUBSCRIPTION = 'True'")
            return self.cursor.fetchall()

    def print_info(self, user_id=None):
        """
        Печатает всю базу данных
        """
        if user_id is None:
            self.cursor.execute("SELECT * FROM users_database")
        else:
            self.cursor.execute(f"SELECT * FROM users_database WHERE USER_ID = {user_id}")
        rows = self.cursor.fetchall()
        for row in rows:
            print("ID", row[0])
            print("USER_ID", row[1])
            print("SUBSCRIPTION", row[2])
            print("CURRENCY", row[3])