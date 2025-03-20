"""
Module: database.py
Description: Module to work with database.
"""

from sqlalchemy import create_engine

from config.variables import POSTGRES_DB, POSTGRES_PASSWORD, POSTGRES_USER

DRIVER = "postgresql"

ENGINE_URL = f"{DRIVER}://{POSTGRES_USER}:{POSTGRES_PASSWORD}@postgres_main:5432/{POSTGRES_DB}"

ENGINE = create_engine(ENGINE_URL)
