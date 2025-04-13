import sqlite3

class QuizDB:
    def __init__(self, db_name='quiz_bowl.db'):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_all_tables()

    def create_table(self, table_name):
        self.cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT NOT NULL,
                option_a TEXT NOT NULL,
                option_b TEXT NOT NULL,
                option_c TEXT NOT NULL,
                option_d TEXT NOT NULL,
                correct_answer TEXT NOT NULL
            );
        ''')
        print(f"Table '{table_name}' created.")

    def create_all_tables(self):
        tables = ['ds_3850', 'econ_3610', 'mkt_4100', 'mkt_4900', 'ds_3841']
        for table in tables:
            self.create_table(table)
        self.connection.commit()
        self.connection.close()

if __name__ == '__main__':
    QuizDB()
