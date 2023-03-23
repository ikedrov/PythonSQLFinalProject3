'''
1. Создать базу данных mobile_calls.db
2. Создать таблицу mobile_users с колонками UserID (INTEGER), User (TEXT), Balance (INTEGER)
3. Создать таблицу mobile_price с колонками PriceID (INTEGER), Mts_Mts(INTEGER), Mts_Tele2(INTEGER),
   Mts_Yota(INTEGER)
4. Заполнение таблицы mobile_users:
    1, User1, 500
5. Заполнение таблицы mobile_price:
    1, 1, 2, 3
6. Создать файл report_mobile.csv, включающий поля Date, Operator ( из таблицы mobile_price), Count_min, Amount.
7. Создать метод report_operation, который будет принимать в себя следующие значения и помещать в report_mobile.csv
при успешной прохождении операции.
8. Разработать следующую логику:
    - ежедневно совершается 1 звонок
    - происходит рандомный выбор Operator из таблицы mobile_price
    - происходит рандомное время звонка от 1 до 10 минут
    - происходит списание денежных средств с баланса - Amount = Operator * Count_min
    - длительность кода - 30 циклов - 30 итераций (месяц)

9. Предусмотреть проверку на достаточную величину баланса, оповещение о недостаточности денежных средств,
невозможности уйти в минус.

'''


import csv
import sqlite3
import random
import datetime


now_date = datetime.datetime.utcnow().strftime('%H:%M-%d.%m.%Y')
class SqlCalls:

    @staticmethod
    def create_table_users():
        with sqlite3.connect('mobile_calls.db') as db:
            cur = db.cursor()
            cur.execute('''CREATE TABLE IF NOT EXISTS mobile_users(
                UserID INTEGER PRIMARY KEY AUTOINCREMENT,
                User TEXT NOT NULL,
                Balance INTEGER NOT NULL);''')
            print('Создана таблица mobile_users')

    @staticmethod
    def create_table_prices():
        with sqlite3.connect('mobile_calls.db') as db:
            cur = db.cursor()
            cur.execute('''CREATE TABLE IF NOT EXISTS mobile_price(
                PriceID INTEGER PRIMARY KEY AUTOINCREMENT,
                Mts_Mts INTEGER NOT NULL,
                Mts_Tele2 INTEGER NOT NULL,
                Mts_Yota INTEGER NOT NULL);''')
            print('Создана таблица mobile_price')

    @staticmethod
    def add_users(data_users):
        with sqlite3.connect('mobile_calls.db') as db:
            cur = db.cursor()
            cur.execute(
                '''INSERT OR REPLACE INTO mobile_users (User, Balance) VALUES (?, ?)''',
                data_users)
            print('Добавлен новый пользователь')

    @staticmethod
    def add_prices(data_prices):
        with sqlite3.connect('mobile_calls.db') as db:
            cur = db.cursor()
            cur.execute(
                '''INSERT OR REPLACE INTO mobile_price (Mts_Mts, Mts_Tele2, Mts_Yota) VALUES (?, ?, ?)''',
                data_prices)
            print('Добавлены расценки')

    @staticmethod
    def calls():

        with sqlite3.connect('mobile_calls.db') as db:

            cur = db.cursor()
            cur.execute('''SELECT Balance FROM mobile_users''')
            balance_result = cur.fetchone()
            balance = balance_result[0]

            cur = db.cursor()
            cur.execute('''SELECT Mts_Mts, Mts_Tele2, Mts_Yota FROM mobile_price''')
            prices_result = cur.fetchall()
            prices = [prices_result[0][0], prices_result[0][1], prices_result[0][2]]

            for i in range(30):
                count_min = random.randint(1, 10)
                operator = random.choice(prices)

                if balance >= count_min * operator:
                    cur.execute(f'''UPDATE mobile_users SET Balance = Balance -  {count_min * operator}''')
                    db.commit()
                    balance -= count_min * operator
                    SqlCalls.operation_report(now_date, operator, count_min, count_min * operator)
                else:
                    print('Недостаточно средств на счете')
                    break

    @staticmethod
    def operation_report(now_date, operator, count_min, amount):

        user_data = [
            (now_date, operator, count_min, amount)
        ]

        with open('report.csv', 'a', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerows(
                user_data
            )
        print('Добавлена информация о звонке')

