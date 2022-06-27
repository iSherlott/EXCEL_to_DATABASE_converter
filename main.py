import pandas as pd
import os
import sqlite3

company = 'sanofi'

file_name = './assets'
entries = os.listdir(file_name)

convert = {
    "int64": "INTEGER",
    "float64": "DOUBLE(10,2)",
    "object": "VARCHAR(255)",
    "datetime64[ns]": "DATETIME"
}

con = sqlite3.connect('database/db.db')
cur = con.cursor()

for x in range(len(entries)):
    print(f'Carregando Arquivo: {entries[x]}')

    df = pd.read_excel(f'assets/{entries[x]}')
    headers = list(df.columns)
    headersType = list(df.dtypes)

    name = entries[x].replace(".xlsx", "")

    columns = []
    print(name)
    for x in range(len(headers)):
        print(f'{headers[x]} {convert[str(headersType[x])]}')
        columns.append(f'{headers[x]} {convert[str(headersType[x])]}')

    cur.execute(f'CREATE TABLE IF NOT EXISTS {name} ({", ".join(columns)})')

for x in range(len(entries)):
    print(f'Carregando Data: {entries[x]}')
    df = pd.read_excel(f'assets/{entries[x]}')
    headers = list(df.columns)

    name = entries[x].replace(".xlsx", "")

    for index, row in df.iterrows():
        _row = []

        for header in headers:
            _row.append(str(row[header]).replace("'", ""))

        value = "', '".join(_row)
        aspas = "'"

        query = f'INSERT INTO {name} ({", ".join(headers)}) VALUES ({aspas}{value}{aspas})'
        cur.execute(query)

con.commit()
con.close()
