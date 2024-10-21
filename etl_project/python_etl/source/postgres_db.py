import logging
import sqlalchemy
from sqlalchemy import create_engine

from config.base import settings


def create_postgresql_connection() -> sqlalchemy.Engine or None:
    """
    This function constructs a PostgreSQL database URL based on the settings provided
    in the `settings` object.
    :return: sqlalchemy.engine.base.Engine or None: A SQLAlchemy engine if the connection
        is successful, or None if an error occurs during the connection attempt.
    """
    try:
        db_url = f'postgresql://{settings.postgres.user}:{settings.postgres.password}@{settings.postgres.host}/{settings.postgres.dbname}'
        engine = create_engine(db_url)
        logging.info("Successfully connected to PostgreSQL")
        return engine
    except Exception as e:
        logging.error("Error connecting to PostgreSQL:", e)
        return None