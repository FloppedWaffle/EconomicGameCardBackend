import sqlite3

SQLITE_PATH = "C:/Users/FloppedWaffle/Desktop/Проекты/EconomicGame 2023/Flask Backend (indev)/data/payments.sqlite"

class gameDB:
    """Управление базой данных игры"""

    def __init__(self, db_file):
        self.con = sqlite3.connect(db_file)
        self.cur = self.con.cursor()


    def create_table_players(self):   # tax_paid имеет 3 значения, 0 - неуплачены, 1 - уплачены, 2 - уплачены всегда (для госслужащих) 
        with self.con:
            self.cur.execute("""
                            CREATE TABLE IF NOT EXISTS players(
                            player_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            nfc_uid VARCHAR(32) NOT NULL UNIQUE,
                            firstname VARCHAR(32) NOT NULL,
                            lastname VARCHAR(32) NOT NULL,
                            grade VARCHAR(16) NOT NULL,
                            balance INTEGER NOT NULL,
                            tax_paid INTEGER NOT NULL,
                            company_id INTEGER NOT NULL,
                            is_founder INTEGER NOT NULL,
                            is_minister INTEGER NOT NULL,
                            is_minister_paid INTEGER)
                            """)
            self.con.commit()


    def create_table_teachers(self):
        with self.con:
            self.cur.execute("""
                            CREATE TABLE IF NOT EXISTS teachers(
                            teacher_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            nfc_uid VARCHAR(32) NOT NULL UNIQUE,
                            password VARCHAR(64) NOT NULL UNIQUE,
                            firstname VARCHAR(32) NOT NULL,
                            middlename VARCHAR(32) NOT NULL,
                            subject_name VARCHAR(256) NOT NULL UNIQUE,
                            balance INTEGER NOT NULL)
                            """)
            self.con.commit()


    def create_table_companies(self):
        with self.con:
            self.cur.execute("""
                            CREATE TABLE IF NOT EXISTS companies(
                            company_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            password VARCHAR(64) NOT NULL UNIQUE,
                            name VARCHAR(256) NOT NULL UNIQUE,
                            balance INTEGER NOT NULL,
                            profit INTEGER NOT NULL,
                            taxes INTEGER NOT NULL,
                            is_state INTEGER NOT NULL)
                            """)
            self.con.commit()


    def create_table_services(self):
        with self.con:
            self.cur.execute("""
                            CREATE TABLE IF NOT EXISTS services(
                            service_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            company_id INTEGER NOT NULL,
                            name VARCHAR(64) NOT NULL UNIQUE,
                            quantity INTEGER NOT NULL,
                            cost INTEGER NOT NULL)
                            """)
            self.con.commit()


    def create_table_bankers(self):
        with self.con:
            self.cur.execute("""
                            CREATE TABLE IF NOT EXISTS bankers(
                            banker_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            password VARCHAR(64) NOT NULL UNIQUE)
                            """)



    def erase_tables_all(self):
        with self.con:
            self.cur.execute("""DROP TABLE IF EXISTS players;""")
            self.cur.execute("""DROP TABLE IF EXISTS teachers;""")
            self.cur.execute("""DROP TABLE IF EXISTS companies;""")
            self.cur.execute("""DROP TABLE IF EXISTS services;""")
            self.cur.execute("""DROP TABLE IF EXISTS bankers;""")
            self.con.commit()
    

    def erase_table_players(self):
        with self.con:
            self.cur.execute("""DROP TABLE IF EXISTS players;""")
            self.con.commit()


    def erase_table_teachers(self):
        with self.con:
            self.cur.execute("""DROP TABLE IF EXISTS teachers;""")
            self.con.commit()


    def erase_table_companies(self):
        with self.con:
            self.cur.execute("""DROP TABLE IF EXISTS companies;""")
            self.con.commit()


    def erase_table_services(self):
        with self.con:
            self.cur.execute("""DROP TABLE IF EXISTS services;""")
            self.con.commit()


    def erase_table_bankers(self):
        with self.con:
            self.cur.execute("""DROP TABLE IF EXISTS bankers;""")
            self.con.commit()


    def add_players_in_db(self):
        with sqlite3.connect(SQLITE_PATH) as con:
            cur = con.cursor()

            # тест всех функций, связанных с игроком
            cur.execute("""
                    INSERT INTO players(firstname, lastname, grade, balance, tax_paid, is_minister, is_minister_paid, nfc_uid, is_founder, company_id)
                    VALUES("Василий", "Пупкин", "5Б", 100, 1, 0, 0, "04 9a 4c 52 a6 34 80", 1, 1)
                    """) # 04 9a 4c 52 a6 34 80 - карта школы
            
            

            # тест вывода у учителей
            cur.execute("""
                INSERT INTO players(firstname, lastname, grade, balance, tax_paid, is_minister, is_minister_paid, nfc_uid, is_founder, company_id) 
                VALUES("Терентий", "Первый", "7Ы", 0, 1, 0, 0, "nfc_test1", 0, 0)
                """)
            cur.execute("""
                    INSERT INTO players(firstname, lastname, grade, balance, tax_paid, is_minister, is_minister_paid, nfc_uid, is_founder, company_id)
                    VALUES("Терентий", "Второй", "8Г (ШО-2) (фирма)", 0, 0, 0, 0, "nfc_test2", 1, 1)
                    """)

            cur.execute("""
                INSERT INTO players(firstname, lastname, grade, balance, tax_paid, company_id, is_founder, is_minister, is_minister_paid, nfc_uid) 
                VALUES("Петя", "Иванов", "5B", 0, 1, 1, 1, 0, 0, "nfc_test4")
                """)
            cur.execute("""
                        INSERT INTO players(firstname, lastname, grade, balance, tax_paid, company_id, is_founder, is_minister, is_minister_paid, nfc_uid) 
                        VALUES("Лёшка", "Петров", "5В", 0, 1, 1, 1, 0, 0, "nfc_test5")
                        """)

            con.commit()


    def add_teachers_in_db(self):
        with sqlite3.connect(SQLITE_PATH) as con:
            cur = con.cursor()

            # учителя
            cur.execute("""
                        INSERT INTO teachers(firstname, middlename, password, subject_name, balance, nfc_uid) 
                        VALUES("Константин", "Константинович", "61e521e174982c310b25e3ff93616b76459b580fdd455305e90f5a808fb2d65c",
                        'Государственное предприятие "Математический ответник"', 1337, "04 32 3e 42 85 68 80")
                        """) # teacherpas hash
                             # 04 32 3e 42 85 68 80 - тройка

            con.commit()


    def add_companies_and_services_in_db(self):
        with sqlite3.connect(SQLITE_PATH) as con:
            cur = con.cursor()

            # 1 фирма (id 1)
            cur.execute("""
                        INSERT INTO companies(password, name, balance, taxes, profit, is_state) 
                        VALUES("db23bc16ec47a980f2c6b8b4e5e020ee43c76ebea08a6ddcc9c0233b25d3a31e", "Пельменная", 100, 200, 50, 0)
                        """) # companypas hash
            
            # услуги 1 фирмы
            cur.execute(f""" 
                        INSERT INTO services(company_id, name, quantity, cost)
                        VALUES(1, "1 тюлень", 10, 20)
                        """)
            cur.execute(f""" 
                        INSERT INTO services(company_id, name, quantity, cost)
                        VALUES(1, "1 олень", 15, 30)
                        """)
            cur.execute(f""" 
                        INSERT INTO services(company_id, name, quantity, cost)
                        VALUES(1, "1 пельмень", 15, 30)
                        """)



            # сосисочная (столовка)
            cur.execute("""
                        INSERT INTO companies(company_id, password, name, balance, taxes, profit, is_state) 
                        VALUES(50, "51e8e4c4d6bc571330275750d9b035f182d531fc0398a3ca56114e1acdcfa153", "Сосисочная", 0, 0, 126, 1)
                        """) # sosisochno hash
            
            # услуги сосисочной
            for i in range(1, 11):
                cur.execute(f""" 
                            INSERT INTO services(company_id, name, quantity, cost)
                            VALUES(50, "{i} сосисок в тесте", 10, 15)
                            """)
                cur.execute(f""" 
                            INSERT INTO services(company_id, name, quantity, cost) 
                            VALUES(50, "{i} бутербродов", 20, 30)
                            """)

            con.commit()


    def add_bankers_in_db(self):
        with sqlite3.connect(SQLITE_PATH) as con:
            cur = con.cursor()
            # банкиры
            cur.execute("""
                    INSERT INTO bankers(password) 
                    VALUES("5e4cb00cf41d2565816f9ff62a0a23729d17de7183fc91bf59033b606d70b39a")
                    """)
            con.commit()



def pass_period():
    # TODO: Каждый час, каждый период нужно переносить профит (домноженный на 0.1) на налоги у чатсных фирм
    # TODO: Каждый час, каждый период нужно обнулять налоги всем игрокам, кроме гос. министров, владельцев и работников фирм
    # TODO: Каждый час, каждый период нужно обнулять is_minister_paid, чтобы министры могли брать зарплату


    with sqlite3.connect(SQLITE_PATH) as con:
        cur = con.cursor()

        # обнуляем налоги
        cur.execute("""
                    UPDATE players
                    SET tax_paid = 0
                    WHERE is_founder = 0 AND is_minister = 0 AND company_id = 0;
                    """)
        
        # обнуляем статус выдачи зарплаты министрам
        cur.execute("""
                    UPDATE players
                    SET is_minister_paid = 0
                    WHERE is_minister = 1;
                    """)
        
        # переносим десятую часть дохода на налоги, а доход обнуляем
        cur.execute("""
                    UPDATE companies
                    SET taxes = taxes + profit * 0.1, profit = 0
                    WHERE is_state = 0;
                    """)



if __name__ == "__main__":
    passPer = False
    if passPer:
        pass_period()
    else:
        db_mgr = gameDB(SQLITE_PATH)
        
        db_mgr.erase_table_players()
        db_mgr.erase_table_teachers()
        db_mgr.erase_table_companies()
        db_mgr.erase_table_services()
        db_mgr.erase_table_bankers()

        db_mgr.create_table_players()
        db_mgr.create_table_teachers()
        db_mgr.create_table_companies()
        db_mgr.create_table_services()
        db_mgr.create_table_bankers()


        db_mgr.add_players_in_db()
        db_mgr.add_teachers_in_db()
        db_mgr.add_companies_and_services_in_db()
        db_mgr.add_bankers_in_db()
