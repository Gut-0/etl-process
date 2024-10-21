import logging
import pandas as pd
import sqlalchemy
from sqlalchemy import text

from postgres_db import create_postgresql_connection

MAX_VALUE = 99999999999999.99


def populate_companies_table(engine: sqlalchemy.Engine, df: pd.DataFrame) -> None:
    try:
        df = df.drop(['id', 'amount', 'status', 'created_at', 'paid_at'], axis=1)
        df = df.drop_duplicates('company_id').drop_duplicates('name').dropna()
        df.rename(columns={'company_id': 'id', 'name': 'company_name'}, inplace=True)
        df.to_sql(name='companies', con=engine, if_exists='append', index=False)

        logging.info("Successfully inserted data to 'companies' table")
    except Exception as e:
        logging.error("Error loading data into the 'companies' table:", e)


def populate_charges_table(engine: sqlalchemy.Engine, df: pd.DataFrame) -> None:
    try:
        df = df.map(lambda x: None if pd.isna(x) else x)
        df_companies = df.drop(['id', 'amount', 'status', 'created_at', 'paid_at'], axis=1).drop_duplicates(
            'company_id').drop_duplicates('name')
        df = df.merge(df_companies, on='name', how='left')
        df['company_id_y'] = df['company_id_y'].fillna(df['company_id_x'])
        df = df.drop(['id', 'name', 'company_id_x'], axis=1).rename(columns={'company_id_y': 'company_id'})
        df['amount'] = df['amount'].apply(lambda x: x if x <= MAX_VALUE else 0)
        df.to_sql(name='charges', con=engine, if_exists='append', index=False)

        logging.info("Successfully inserted data to 'charges' table")
    except Exception as e:
        logging.error("Error loading data into the 'charges' table:", e)


def create_total_transactions_view(engine: sqlalchemy.Engine) -> None:
    try:
        query = """
            CREATE OR REPLACE VIEW total_amount_per_day AS
            SELECT 
                DATE(c.created_at) AS transaction_date, 
                co.company_name, 
                SUM(c.amount) AS total_amount 
            FROM 
                charges c 
            JOIN 
                companies co ON c.company_id = co.id 
            GROUP BY 
                transaction_date, co.company_name 
            ORDER BY 
                transaction_date, co.company_name;
            """
        with engine.connect() as connection:
            connection.execute(text(query))
            connection.commit()
            logging.info("Successfully created the 'total_amount_per_day' view in the database.")

        query = "SELECT * FROM total_amount_per_day;"
        result_df = pd.read_sql_query(query, engine)

        print(result_df)
    except Exception as e:
        logging.error("Error creating the transactions view:", e)


def main():
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting the ETL process...")

    engine = create_postgresql_connection()
    if engine is None:
        return

    df = pd.read_csv('input/data_prueba_tecnica.csv',
                     dtype={'id': str, 'name': str, 'company_id': str, 'amount': float, 'status': str},
                     parse_dates=['created_at', 'paid_at'])

    populate_companies_table(engine, df)
    populate_charges_table(engine, df)
    create_total_transactions_view(engine)
    logging.info("ETL process completed.")


if __name__ == "__main__":
    main()
