from flask import Flask, jsonify, request
from multiprocessing import Process

from db_config import *


db_creator()


if __name__ == "__main__":

    bd_data_engine = Process(target=db_data_generator)
    bd_data_engine.start()


app = Flask(__name__)


@app.route("/fetch-one")
def fetch_one():

    base = request.args.get("from")
    result = request.args.get("to")

    date_values = {}
    date_value = "null"

    if base != "USD":

        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()

        cursor.execute(
            "SELECT MAX(id),name_coin,datetime,coinvalue FROM currency_exchange WHERE name_coin=? ",
            (base,),
        )
        cursor = cursor.fetchall()

        connection.commit()
        connection.close()

        base_value = float(cursor[0][3])
        date_value = cursor[0][2]

        base_value = 1 / base_value

    else:

        base_value = 1.0

    date_values[base] = date_value

    if result != "USD":

        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()

        cursor.execute(
            "SELECT MAX(id),name_coin,datetime,coinvalue FROM currency_exchange WHERE name_coin=? ",
            (result,),
        )
        cursor = cursor.fetchall()

        connection.commit()
        connection.close()

        result_value = float(cursor[0][3])
        date_value = cursor[0][2]

    else:

        result_value = 1.0

    if base == result:
        value = 1.0
        date_value = None

    else:
        value = round((base_value * result_value), 5)

    date_values[result] = date_value

    updated = date_values.get(min(date_values))

    dataframe = {"base": base, "results": value, "updated": updated}

    return jsonify(dataframe)


@app.route("/fetch-multi")
def fetch_multi():

    base = request.args.get("from")
    results = request.args.get("to")
    results = results.split(",")

    values = {}

    if base != "USD":

        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()

        cursor.execute(
            "SELECT MAX(id),name_coin,datetime,coinvalue FROM currency_exchange WHERE name_coin=? ",
            (base,),
        )
        cursor = cursor.fetchall()

        connection.commit()
        connection.close()

        base_value = float(cursor[0][3])
        base_value = 1 / base_value

    else:

        base_value = 1.0

    for result in results:

        if result != "USD":

            connection = sqlite3.connect("database.db")
            cursor = connection.cursor()

            cursor.execute(
                "SELECT MAX(id),name_coin,datetime,coinvalue FROM currency_exchange WHERE name_coin=? ",
                (result,),
            )
            cursor = cursor.fetchall()

            connection.commit()
            connection.close()

            result_value = float(cursor[0][3])

        else:

            result_value = 1.0

        if base == result:
            value = 1.0

        else:
            value = round((base_value * result_value), 5)

        values[result] = value

    dataframe = {"base": base, "results": values}

    return jsonify(dataframe)


@app.route("/fetch-all")
def fetch_all():

    base = request.args.get("from")

    values = {}
    date_values = {}
    date_value = "null"

    if base != "USD":

        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()

        cursor.execute(
            "SELECT MAX(id),name_coin,datetime,coinvalue FROM currency_exchange WHERE name_coin=? ",
            (base,),
        )
        cursor = cursor.fetchall()

        connection.commit()
        connection.close()

        base_value = float(cursor[0][3])

        base_value = 1 / base_value

    else:
        base_value = 1.0

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute("SELECT DISTINCT name_coin FROM currency_exchange")
    cursor = cursor.fetchall()

    connection.commit()
    connection.close()

    for result in cursor:
        result = result[0]

        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()

        cursor.execute(
            "SELECT MAX(id),name_coin,datetime,coinvalue FROM currency_exchange WHERE name_coin=? ",
            (result,),
        )
        cursor = cursor.fetchall()

        connection.commit()
        connection.close()

        result_value = float(cursor[0][3])

        if base == result:
            value = 1.0

        else:
            value = round((base_value * result_value), 5)

        values[result] = value

    values["USD"] = round((base_value), 5)

    dataframe = {"base": base, "results": values}

    return jsonify(dataframe)


@app.route("/convert")
def convert():

    base = request.args.get("from")
    result = request.args.get("to")
    amount = request.args.get("amount")

    if base != "USD":

        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()

        cursor.execute(
            "SELECT MAX(id),name_coin,datetime,coinvalue FROM currency_exchange WHERE name_coin=? ",
            (base,),
        )
        cursor = cursor.fetchall()

        connection.commit()
        connection.close()

        base_value = float(cursor[0][3])

        base_rate = 1 / base_value
        base_value = float(amount) / base_value

    else:

        base_value = 1.0

    if result != "USD":

        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()

        cursor.execute(
            "SELECT MAX(id),name_coin,datetime,coinvalue FROM currency_exchange WHERE name_coin=? ",
            (result,),
        )
        cursor = cursor.fetchall()

        connection.commit()
        connection.close()

        result_value = float(cursor[0][3])

    else:

        result_value = 1.0

    if base == result:
        rate = 1
        value = base_value * result_value

    else:
        rate = base_rate * result_value
        value = base_value * result_value

    dataframe = {
        "base": base,
        "amount": amount,
        "result": {result: round((value), 2), "rate": round((rate), 5)},
    }

    return jsonify(dataframe)


@app.route("/currencies")
def currencies():

    avaiable_currencies = {}

    all_currencies = {
        "AED": "United Arab Emirates Dirham",
        "AFN": "Afghan Afghani",
        "ALL": "Albanian Lek",
        "AMD": "Armenian Dram",
        "ANG": "Dutch Guilders",
        "AOA": "Angolan Kwanza",
        "ARS": "Argentine Peso",
        "AUD": "Australian Dollar",
        "AWG": "Aruban Florin",
        "AZN": "Azerbaijani Manat",
        "BAM": "Bosnia-Herzegovina Convertible Mark",
        "BBD": "Barbadian Dollar",
        "BDT": "Bangladeshi Taka",
        "BGN": "Bulgarian Lev",
        "BHD": "Bahraini Dinar",
        "BIF": "Burundian Franc",
        "BMD": "Bermudian Dollar",
        "BND": "Bruneian Dollar",
        "BOB": "Bolivian Boliviano",
        "BRL": "Brazilian Real",
        "BSD": "Bahamian Dollar",
        "BTN": "Bhutanese Ngultrum",
        "BWP": "Botswanan Pula",
        "BZD": "Belizean Dollar",
        "CAD": "Canadian Dollar",
        "CDF": "Congolese Franc",
        "CHF": "Swiss Franc",
        "CLF": "Chilean Unit of Account UF",
        "CLP": "Chilean Peso",
        "CNH": "Chinese Yuan Offshore",
        "CNY": "Chinese Yuan",
        "COP": "Colombian Peso",
        "CUP": "Cuban Peso",
        "CVE": "Cape Verdean Escudo",
        "CZK": "Czech Republic Koruna",
        "DJF": "Djiboutian Franc",
        "DKK": "Danish Krone",
        "DOP": "Dominican Peso",
        "DZD": "Algerian Dinar",
        "EGP": "Egyptian Pound",
        "ERN": "Eritrean Nakfa",
        "ETB": "Ethiopian Birr",
        "EUR": "Euro",
        "FJD": "Fijian Dollar",
        "FKP": "Falkland Islands Pound",
        "GBP": "British Pound Sterling",
        "GEL": "Georgian Lari",
        "GHS": "Ghanaian Cedi",
        "GIP": "Gibraltar Pound",
        "GMD": "Gambian Dalasi",
        "GNF": "Guinean Franc",
        "GTQ": "Guatemalan Quetzal",
        "GYD": "Guyanaese Dollar",
        "HKD": "Hong Kong Dollar",
        "HNL": "Honduran Lempira",
        "HRK": "Croatian Kuna",
        "HTG": "Haitian Gourde",
        "HUF": "Hungarian Forint",
        "IDR": "Indonesian Rupiah",
        "ILS": "Israeli New Sheqel",
        "INR": "Indian Rupee",
        "IQD": "Iraqi Dinar",
        "IRR": "Iranian Rial",
        "ISK": "Icelandic Krona",
        "JMD": "Jamaican Dollar",
        "JOD": "Jordanian Dinar",
        "JPY": "Japanese Yen",
        "KES": "Kenyan Shilling",
        "KGS": "Kyrgystani Som",
        "KHR": "Cambodian Riel",
        "KMF": "Comorian Franc",
        "KPW": "North Korean Won",
        "KRW": "South Korean Won",
        "KWD": "Kuwaiti Dinar",
        "KYD": "Caymanian Dollar",
        "KZT": "Kazakhstani Tenge",
        "LAK": "Laotian Kip",
        "LBP": "Lebanese Pound",
        "LKR": "Sri Lankan Rupee",
        "LRD": "Liberian Dollar",
        "LSL": "Basotho Maloti",
        "LYD": "Libyan Dinar",
        "MAD": "Moroccan Dirham",
        "MDL": "Moldovan Leu",
        "MGA": "Malagasy Ariary",
        "MKD": "Macedonian Denar",
        "MMK": "Myanma Kyat",
        "MNT": "Mongolian Tugrik",
        "MOP": "Macanese Pataca",
        "MRU": "Mauritanian Ouguiya (1973–2017)",
        "MUR": "Mauritian Rupee",
        "MVR": "Maldivian Rufiyaa",
        "MWK": "Malawian Kwacha",
        "MXN": "Mexican Peso",
        "MYR": "Malaysian Ringgit",
        "MZN": "Mozambican Metical",
        "NAD": "Namibian Dollar",
        "NGN": "Nigerian Naira",
        "NOK": "Norwegian Krone",
        "NPR": "Nepalese Rupee",
        "NZD": "New Zealand Dollar",
        "OMR": "Omani Rial",
        "PAB": "Panamanian Balboa",
        "PEN": "Peruvian Nuevo Sol",
        "PGK": "Papua New Guinean Kina",
        "PHP": "Philippine Peso",
        "PKR": "Pakistani Rupee",
        "PLN": "Polish Zloty",
        "PYG": "Paraguayan Guarani",
        "QAR": "Qatari Rial",
        "RON": "Romanian Leu",
        "RSD": "Serbian Dinar",
        "RUB": "Russian Ruble",
        "RWF": "Rwandan Franc",
        "SAR": "Saudi Arabian Riyal",
        "SCR": "Seychellois Rupee",
        "SDG": "Sudanese Pound",
        "SEK": "Swedish Krona",
        "SGD": "Singapore Dollar",
        "SHP": "Saint Helena Pound",
        "SLL": "Sierra Leonean Leone",
        "SOS": "Somali Shilling",
        "SRD": "Surinamese Dollar",
        "SYP": "Syrian Pound",
        "SZL": "Swazi Emalangeni",
        "THB": "Thai Baht",
        "TJS": "Tajikistani Somoni",
        "TMT": "Turkmenistani Manat",
        "TND": "Tunisian Dinar",
        "TOP": "Tongan Pa'anga",
        "TRY": "Turkish Lira",
        "TTD": "Trinidad and Tobago Dollar",
        "TWD": "Taiwan New Dollar",
        "TZS": "Tanzanian Shilling",
        "UAH": "Ukrainian Hryvnia",
        "UGX": "Ugandan Shilling",
        "USD": "United States Dollar",
        "UYU": "Uruguayan Peso",
        "UZS": "Uzbekistan Som",
        "VND": "Vietnamese Dong",
        "VUV": "Ni-Vanuatu Vatu",
        "WST": "Samoan Tala",
        "XAF": "CFA Franc BEAC",
        "XCD": "East Caribbean Dollar",
        "XDR": "Special Drawing Rights",
        "XOF": "CFA Franc BCEAO",
        "XPF": "CFP Franc",
        "YER": "Yemeni Rial",
        "ZAR": "South African Rand",
        "ZMW": "Zambian Kwacha",
    }

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute("SELECT DISTINCT name_coin FROM currency_exchange")
    cursor = cursor.fetchall()

    connection.commit()
    connection.close()

    for currency in cursor:
        currency = currency[0]

        if currency in all_currencies:
            avaiable_currencies[currency] = all_currencies[currency]

    avaiable_currencies["USD"] = all_currencies["USD"]

    return jsonify(avaiable_currencies)


if __name__ == "__main__":
    app.run(debug=False)
