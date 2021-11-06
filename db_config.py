import sqlite3
import time

from scrap_and_generate import *



def db_creator():


    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS currency_exchange(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name_coin varchar(255),
            datetime ,
            coinvalue float(255)
        );
        """)

    connection.commit()
    connection.close()



def db_data_generator():


        while 1:

            GBP = (generate_exchange(USDtoGBP,0.05,False))
            EUR = (generate_exchange(USDtoEUR,0.05,False))




            coins = [
                (GBP),
                (EUR),
            ]



            connection = sqlite3.connect('database.db')
            cursor = connection.cursor()

            cursor.executemany("""
            INSERT INTO currency_exchange VALUES (
                null,
                ?,
                datetime('now'),
                ?)""",
                coins)

            connection.commit()
            connection.close()

                       
            time.sleep(6)
        
