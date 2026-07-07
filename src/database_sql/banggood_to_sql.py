# src/database_sql/banggood_to_sql.py
import pandas as pd
from sqlalchemy import create_engine
from util.logger import log

def upload_to_sql():
    log("STEP 4: Uploading cleaned data to SQL Server...")

    # 1. Load cleaned CSV
    df = pd.read_csv("data/cleaned/combined_cleaned.csv")

    # 2. SQL Server connection using Windows Authentication
    server = "."  # Local default instance
    database = "BanggoodDB"

    connection_string = (
        f"mssql+pyodbc://{server}/{database}"
        "?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
    )
    engine = create_engine(connection_string)

    # 3. Insert DataFrame into SQL Server
    df.to_sql('BanggoodProducts', con=engine, if_exists='replace', index=False)
    log("Data inserted into SQL Server successfully!")

if __name__ == "__main__":
    upload_to_sql()
