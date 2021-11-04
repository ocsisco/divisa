from flask import Flask, jsonify, request
from multiprocessing import Process

from db_config import*



db_creator()



if __name__=='__main__':

        bd_data_engine = Process(target=db_data_generator)
        bd_data_engine.start()
        




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


    if base == result:
        updated = "null"
    else:
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




    for name_of_coin_in_result in results:


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

    base = request.args.get("from")
    
    values = {}
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
            
        date_value = "null"
        base_value = 1.





    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    cursor.execute("SELECT DISTINCT name_coin FROM currency_exchange")
    cursor = cursor.fetchall()

    connection.commit()
    connection.close()


    for name_of_coin in cursor:
        name_of_coin = name_of_coin[0]


        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        cursor.execute("SELECT MAX(id),name_coin,datetime,coinvalue FROM currency_exchange WHERE name_coin=? ",(name_of_coin,))
        cursor = cursor.fetchall()

        connection.commit()
        connection.close()

        result_value = float(cursor[0][3])
        date_value = cursor[0][2]
            

        

        date_values[name_of_coin]=date_value






        value = round((base_value * result_value),5)
        values[name_of_coin]=value

    values["USD"]=round((base_value),5)

        
        




    updated = date_values.get(min(date_values))

    
    

    dataframe = { "base":base , "results":values , "updated": updated}
    

        
    return jsonify(dataframe)







    







@app.route("/convert")
def convert():
    return()

@app.route("/currencies")
def route():
    return()











if __name__ == '__main__':
    app.run(debug=False)

