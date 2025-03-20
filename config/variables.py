"""
Module: variables.py
Description: Module to work with project variables.
"""

import os

from dotenv import load_dotenv

load_dotenv()

BINGX_API_KEY = os.getenv("BINGX_API_KEY", "")
BINGX_SECRET_KEY = os.getenv("BINGX_SECRET_KEY", "")

POSTGRES_DB = os.getenv("POSTGRES_DB", "")
POSTGRES_USER = os.getenv("POSTGRES_USER", "")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "")

CRYPTO_PANIC_API_KEY = os.getenv("CRYPTO_PANIC_API_KEY", "")

CRYPTO_PANIC_BASE_URL = "https://cryptopanic.com/api/v1/posts/?auth_token={}".format(
    CRYPTO_PANIC_API_KEY
)
