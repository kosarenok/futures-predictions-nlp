"""Module for handling database operations using SQLAlchemy."""

from textwrap import dedent
from typing import Any, Dict, Literal, Optional

import pandas as pd
from sqlalchemy import Engine, text
from sqlalchemy.exc import SQLAlchemyError

from config.database import ENGINE
from src.utils.loggerring import logger


def get_query_from_sql_file(query_file_path: str) -> str:
    """
    Function for loading query from file. Returns query.

    Parameters
    ----------
    query_file_path : str
        Path to file with query.

    Returns
    -------
    str - loading query from file.
    """

    with open(query_file_path, "r", encoding="utf-8") as query_file:
        query = query_file.read()

    return query


def format_sql(query: str, params: Optional[Dict[str, Any]] = None) -> str:
    """
    Formats SQL query to remove unnecessary spaces and tabs.

    Parameters
    ----------
    query : str
        The SQL query to format
    params : dict, optional
        Parameters to pass to SQLAlchemy.

    Returns
    -------
    str
        Formatted SQL query
    """
    formatted_query = dedent(query).strip()

    if params:
        return formatted_query.format(**params)
    return formatted_query


def select(query: str, engine: Engine = ENGINE) -> pd.DataFrame:
    """
    Execute a SQL query and return the result as a DataFrame.

    Parameters
    ----------
    query : str
        The SQL query to execute.
    engine : sqlalchemy.engine.Engine, optional
        The SQLAlchemy engine to use. Default is the main engine.

    Returns
    -------
    pd.DataFrame
        The result of the query as a DataFrame.

    Raises
    ------
    Exception
        If there is an error executing the query.
    """

    try:
        with engine.connect() as connection:
            result = pd.read_sql(text(query), connection)
        return result

    except SQLAlchemyError as e:
        logger.error(f"Error executing query: {e}")
        raise Exception(f"Error executing query: {e}")


def execute(query: str, engine: Engine = ENGINE) -> None:
    """
    Execute a SQL query on the production database.

    Parameters
    ----------
    query : str
        The SQL query to execute.
    engine : sqlalchemy.engine.Engine, optional
        The SQLAlchemy engine to use. Default is the main

    Raises
    ------
    Exception
        If there is an error executing the query.
    """
    try:
        with engine.connect() as connection:
            with connection.begin():
                connection.execute(text(query))
    except SQLAlchemyError as e:
        logger.error(f"Error executing query: {e}")
        raise Exception(f"Error executing query: {e}")


def upload(
    data: pd.DataFrame,
    table_name: str,
    schema: str = "public",
    if_exists: Literal["fail", "replace", "append"] = "append",
    engine: Engine = ENGINE,
) -> None:
    """
    Upload data to a database table.

    Parameters
    ----------
    data : pd.DataFrame
        The data to upload.
    table_name : str
        The name of the table to upload the data to.
    schema : str, optional
        The database schema. Default is "public".
    if_exists : Literal["fail", "replace", "append"], optional
        How to behave if the table already exists:
        - "fail": Raise a ValueError.
        - "replace": Drop the table before inserting new values.
        - "append": Insert new values to the existing table.
        Default is "append".
    engine : sqlalchemy.engine.Engine, optional
        The SQLAlchemy engine to use. Default is the main engine.

    Raises
    ------
    Exception
        If there is an error uploading the data.
    """
    try:
        with engine.connect() as connection:
            data.to_sql(
                table_name,
                connection,
                schema=schema,
                index=False,
                if_exists=if_exists,
                method="multi",
            )
    except SQLAlchemyError as e:
        logger.error(f"Error uploading data: {e}")
        raise Exception(f"Error uploading data: {e}")


def upload_without_duplicates(
    data_df: pd.DataFrame, table_name: Literal["crypto_news", "futures_ohlcv"] = "crypto_news"
):
    """
    Upload news data to database, avoiding duplicate entries based on id.

    Parameters
    ----------
    data_df : pd.DataFrame
        DataFrame containing news data.
    table_name : Literal["crypto_news", "futures_ohlcv"]
        Name of the table to upload to. Default is "crypto_news".

    Raises
    ------
    ValueError
        If the table name is not recognized.
    """
    source_index = {
        "crypto_news": "id",
        "futures_ohlcv": "timestamp",
    }

    index_column = source_index.get(table_name)
    if not index_column:
        raise ValueError(f"Unknown table name: {table_name}")

    existing_ids_query = f"SELECT {index_column} FROM {table_name}"
    existing_ids_df = select(existing_ids_query)
    if existing_ids_df.empty:
        new_data = data_df
    else:
        existing_ids = set(existing_ids_df[index_column].tolist())
        new_data = data_df[~data_df[index_column].isin(existing_ids)]

    if not new_data.empty:
        upload(new_data, table_name, if_exists="append")
        logger.info(f"Added {len(new_data)} new entries to {table_name} table.")
    else:
        logger.warning(f"No new entries to add to {table_name} table.")
