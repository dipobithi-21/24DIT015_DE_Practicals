import os
import shutil
import pandas as pd

# Create Quarantine folder
os.makedirs("Quarantine", exist_ok=True)

# Check all CSV files
for file in os.listdir():
    if file.endswith(".csv"):
        df = pd.read_csv(file)

        if "CustomerID" not in df.columns:
            shutil.move(file, os.path.join("Quarantine", file))

            with open("system_log.txt", "a") as log:
                log.write(f"WARNING: {file} missing CustomerID column\n")

            print(f"{file} moved to Quarantine")

        else:
            print(f"{file} is valid")