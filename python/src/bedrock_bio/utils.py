import duckdb
import json
import os
import urllib.request

BB_R2_DOMAIN = os.environ.get("BB_R2_DOMAIN", "data.bedrock.bio")
CATALOG_URL = f"https://{BB_R2_DOMAIN}/catalog.json"
CREDENTIALS_URL = f"https://{BB_R2_DOMAIN}/credentials.json"

_conn = None
_catalog = None
_credentials = None


def get_catalog() -> dict[str, str]:
    global _catalog
    if _catalog is not None:
        return _catalog

    try:
        with urllib.request.urlopen(CATALOG_URL) as response:
            _catalog = json.loads(response.read())
    except Exception:
        raise ConnectionError(
            f"Unable to access catalog URL '{CATALOG_URL}'. "
            "Check internet connection and try again."
        )
    return _catalog


def get_credentials() -> dict[str, str]:
    global _credentials
    if _credentials is not None:
        return _credentials

    override_credentials = {
        "BB_R2_ACCOUNT_ID": os.environ.get("BB_R2_ACCOUNT_ID", ""),
        "BB_R2_ACCESS_KEY_ID": os.environ.get("BB_R2_ACCESS_KEY_ID", ""),
        "BB_R2_SECRET_ACCESS_KEY": os.environ.get("BB_R2_SECRET_ACCESS_KEY", ""),
    }

    if all(override_credentials.values()):
        _credentials = override_credentials
    else:
        try:
            with urllib.request.urlopen(CREDENTIALS_URL) as response:
                _credentials = json.loads(response.read())
        except Exception:
            raise ConnectionError(
                f"Unable to fetch credentials from '{CREDENTIALS_URL}'. "
                "Check internet connection and try again."
            )
    return _credentials


def get_connection() -> duckdb.DuckDBPyConnection:
    global _conn
    if _conn is not None:
        return _conn

    credentials = get_credentials()
    _conn = duckdb.connect()
    _conn.sql(f"""
        CREATE SECRET (
            TYPE s3,
            KEY_ID '{credentials["BB_R2_ACCESS_KEY_ID"]}',
            SECRET '{credentials["BB_R2_SECRET_ACCESS_KEY"]}',
            ENDPOINT '{credentials["BB_R2_ACCOUNT_ID"]}.r2.cloudflarestorage.com',
            URL_STYLE 'path'
        )
    """)
    return _conn
