import sqlite3
import pandas as pd

conn = sqlite3.connect("customer.db")

df = pd.read_sql("SELECT * FROM Customers", conn)

print("========== DATA FROM SQLITE DATABASE ==========")
print(df)

conn.close()