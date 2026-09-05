import pandas as pd
import json
import sqlite3
# Read CSV file
csv_data = pd.read_csv("customer_profiles.csv")

print("========== CUSTOMER DATA ==========")
print(csv_data.head())

print("\n========== DATASET INFORMATION ==========")
csv_data.info()

print("\n========== STATISTICAL SUMMARY ==========")
print(csv_data.describe(include="all"))

# Read JSON file
with open("api_transactions.json", "r") as file:
    api_data = json.load(file)

print("\n========== API TRANSACTIONS ==========")
print(api_data)


# Read configuration file
with open("config.txt", "r") as file:
    config = file.read()

print("\n========== CONFIGURATION ==========")
print(config)

print("\n========== MISSING VALUES ==========")
print(csv_data.isnull().sum())
print("\n========== DUPLICATE RECORDS ==========")
print(csv_data.duplicated().sum())

print("\n========== STORING DATA INTO SQLITE ==========")

conn = sqlite3.connect("customer.db")

csv_data.to_sql("Customers", conn, if_exists="replace", index=False)

print("Data stored successfully in SQLite database.")

conn.close()
# Generate Data Quality Log
with open("quality_log.txt", "w") as file:
    file.write("========== DATA QUALITY REPORT ==========\n\n")
    file.write("Missing Values:\n")
    file.write(str(csv_data.isnull().sum()))
    file.write("\n\n")
    file.write(f"Duplicate Records: {csv_data.duplicated().sum()}\n")
    file.write("\nValidation Completed Successfully.")

print("Quality log generated successfully.")