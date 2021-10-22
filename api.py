from flask import Flask, jsonify

import time
from datetime import datetime
import os
from multiprocessing import Process
import sqlite3

from scrap_and_generate import *




connection = sqlite3.connect('database.db')
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS currency_exchange(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name_coin varchar(255),
    datetime int,
    coinvalue float(255)
);
""")

connection.commit()
connection.close()




def generator_exchange():
        while 1:

            GBP = (generate_exchange(USDtoGBP,0.05,False))
            EUR = (generate_exchange(USDtoEUR,0.05,False))




            coins = [
                ("GBP",GBP),
                ("EUR",EUR),
            ]



            connection = sqlite3.connect('database.db')
            cursor = connection.cursor()

            cursor.executemany("INSERT INTO currency_exchange VALUES (null,?,julianday('now'),?)",coins)

            connection.commit()
            connection.close()

                       
            time.sleep(10)
        


if __name__=='__main__':

        generator_exchang = Process(target=generator_exchange)
        generator_exchang.start()
        






app = Flask(__name__)


@app.route("/USDTOEUR")
@app.route("/EURTOUSD")
@app.route("/")
def main():

    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM currency_exchange ;")
    currency_exchange = cursor.fetchall()

    connection.commit()
    connection.close()

            

    return jsonify(currency_exchange)


if __name__ == '__main__':
    app.run(debug=False)

