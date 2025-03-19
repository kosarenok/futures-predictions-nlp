"""
Module: database.py
Description: Module to work with database.
"""

from sqlalchemy import create_engine

from config.variables import (
    POSTGRES_USER,POSTGRES_DB,POSTGRES_PASSWORD
)

DRIVER = "postgresql"

ENGINE_URL = f"{DRIVER}://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:5432/{POSTGRES_DB}"

ENGINE = create_engine(ENGINE_URL)