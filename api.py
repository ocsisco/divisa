from flask import Flask, jsonify, request

import time
from datetime import datetime,timedelta
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
    datetime ,
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

            cursor.executemany("""
            INSERT INTO currency_exchange VALUES (
                null,
                ?,
                datetime('now'),
                ?)""",
                coins)

            connection.commit()
            connection.close()

                       
            #time.sleep(10)
        


if __name__=='__main__':

        generator_exchang = Process(target=generator_exchange)
        generator_exchang.start()
        






app = Flask(__name__)


@app.route("/fetch-one")
def fetch_one():

    base = request.args.get("from")
    result = request.args.get("to")

    date_values = {}


    if base != "USD":

        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        cursor.execute("SELECT MAX(id),name_coin,datetime,coinvalue FROM currency_exchange WHERE name_coin=? ",(base,))
        cursor = cursor.fetchall()

        connection.commit()
        connection.close()

        
        base_value = float(cursor[0][3])
        date_value = cursor[0][2]

        base_value = 1/base_value


    else:
        
        base_value = 1.
        date_value = "null"
        


    date_values[base]=date_value


    if result != "USD":

        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        cursor.execute("SELECT MAX(id),name_coin,datetime,coinvalue FROM currency_exchange WHERE name_coin=? ",(result,))
        cursor = cursor.fetchall()
        
        connection.commit()
        connection.close()


        result_value = float(cursor[0][3])
        date_value = cursor[0][2]

    else:

        result_value = 1.
        date_value = "null"
        


    date_values[result]=date_value



    updated = date_values.get(min(date_values))



    value = round((base_value * result_value),5)


        
    dataframe = { "base":base , "results":value , "updated":updated}
    

        
    return jsonify(dataframe)



@app.route("/fetch-multi")
def fetch_multi():

    base = request.args.get("from")
    results = request.args.get("to")
    results = results.split(",")
    

    values = {}
    date_values = {}
    


    for name_of_coin_in_result in results:


        if base != "USD":

            connection = sqlite3.connect('database.db')
            cursor = connection.cursor()

            cursor.execute("SELECT MAX(id),name_coin,datetime,coinvalue FROM currency_exchange WHERE name_coin=? ",(base,))
            cursor = cursor.fetchall()

            connection.commit()
            connection.close()

            base_value = float(cursor[0][3])
            date_value = cursor[0][2]

            base_value = 1/base_value

        else:
            
            date_value = "null"
            base_value = 1.



        date_values[base]=date_value



        if name_of_coin_in_result != "USD":

            connection = sqlite3.connect('database.db')
            cursor = connection.cursor()

            cursor.execute("SELECT MAX(id),name_coin,datetime,coinvalue FROM currency_exchange WHERE name_coin=? ",(name_of_coin_in_result,))
            cursor = cursor.fetchall()

            connection.commit()
            connection.close()

            result_value = float(cursor[0][3])
            date_value = cursor[0][2]
            

        else:

            date_value = "null"
            result_value = 1.


        
        date_values[name_of_coin_in_result]=date_value






        value = round((base_value * result_value),5)
        values[name_of_coin_in_result]=value

        
        




    updated = date_values.get(min(date_values))

    
    

    dataframe = { "base":base , "results":values , "updated": updated}
    

        
    return jsonify(dataframe)



@app.route("/fetch-all")
def fetch_all():
    return()

@app.route("/convert")
def convert():
    return()

@app.route("/currencies")
def route():
    return()











if __name__ == '__main__':
    app.run(debug=False)

