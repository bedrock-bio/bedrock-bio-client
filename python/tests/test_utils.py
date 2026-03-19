import json
from unittest.mock import MagicMock, patch

import duckdb
import pytest

import bedrock_bio.utils as utils


@pytest.fixture(autouse=True)
def _reset_cache():
    utils._catalog = None
    utils._credentials = None
    utils._conn = None
    yield
    if utils._conn is not None:
        utils._conn.close()
    utils._catalog = None
    utils._credentials = None
    utils._conn = None


FAKE_CATALOG = {"dataset_a": "s3://bucket/a.json", "dataset_b": "s3://bucket/b.json"}
FAKE_CREDENTIALS = {
    "BB_R2_ACCOUNT_ID": "abc123",
    "BB_R2_ACCESS_KEY_ID": "key123",
    "BB_R2_SECRET_ACCESS_KEY": "secret123",
}


def _mock_urlopen(data):
    response = MagicMock()
    response.read.return_value = json.dumps(data).encode()
    response.__enter__ = lambda s: s
    response.__exit__ = MagicMock(return_value=False)
    return response


class TestGetCatalog:
    def test_fetches_from_url(self):
        with patch("bedrock_bio.utils.urllib.request.urlopen") as mock:
            mock.return_value = _mock_urlopen(FAKE_CATALOG)
            result = utils.get_catalog()
        assert result == FAKE_CATALOG

    def test_caches_result(self):
        with patch("bedrock_bio.utils.urllib.request.urlopen") as mock:
            mock.return_value = _mock_urlopen(FAKE_CATALOG)
            utils.get_catalog()
            utils.get_catalog()
        mock.assert_called_once()

    def test_connection_error(self):
        with patch("bedrock_bio.utils.urllib.request.urlopen", side_effect=OSError):
            with pytest.raises(ConnectionError, match="Unable to access catalog URL"):
                utils.get_catalog()


class TestGetCredentials:
    def test_fetches_from_url(self):
        with patch("bedrock_bio.utils.urllib.request.urlopen") as mock:
            mock.return_value = _mock_urlopen(FAKE_CREDENTIALS)
            result = utils.get_credentials()
        assert result == FAKE_CREDENTIALS

    def test_caches_result(self):
        with patch("bedrock_bio.utils.urllib.request.urlopen") as mock:
            mock.return_value = _mock_urlopen(FAKE_CREDENTIALS)
            utils.get_credentials()
            utils.get_credentials()
        mock.assert_called_once()

    def test_uses_env_var_overrides(self, monkeypatch):
        monkeypatch.setenv("BB_R2_ACCOUNT_ID", "env_account")
        monkeypatch.setenv("BB_R2_ACCESS_KEY_ID", "env_key")
        monkeypatch.setenv("BB_R2_SECRET_ACCESS_KEY", "env_secret")
        with patch("bedrock_bio.utils.urllib.request.urlopen") as mock:
            result = utils.get_credentials()
        mock.assert_not_called()
        assert result["BB_R2_ACCOUNT_ID"] == "env_account"
        assert result["BB_R2_ACCESS_KEY_ID"] == "env_key"
        assert result["BB_R2_SECRET_ACCESS_KEY"] == "env_secret"

    def test_partial_env_vars_fetches_from_url(self, monkeypatch):
        monkeypatch.setenv("BB_R2_ACCOUNT_ID", "env_account")
        monkeypatch.delenv("BB_R2_ACCESS_KEY_ID", raising=False)
        monkeypatch.delenv("BB_R2_SECRET_ACCESS_KEY", raising=False)
        with patch("bedrock_bio.utils.urllib.request.urlopen") as mock:
            mock.return_value = _mock_urlopen(FAKE_CREDENTIALS)
            result = utils.get_credentials()
        mock.assert_called_once()
        assert result == FAKE_CREDENTIALS

    def test_connection_error(self):
        with patch("bedrock_bio.utils.urllib.request.urlopen", side_effect=OSError):
            with pytest.raises(ConnectionError, match="Unable to fetch credentials"):
                utils.get_credentials()


class TestGetConnection:
    def test_creates_duckdb_connection_with_s3_secret(self):
        with patch("bedrock_bio.utils.get_credentials", return_value=FAKE_CREDENTIALS):
            conn = utils.get_connection()
        assert isinstance(conn, duckdb.DuckDBPyConnection)
        rows = conn.sql("FROM duckdb_secrets()").fetchall()
        assert len(rows) == 1
        secret_string = rows[0][-1]  # last column is secret_string
        assert "s3" in str(rows[0])
        assert "r2.cloudflarestorage.com" in secret_string

    def test_caches_connection(self):
        with patch("bedrock_bio.utils.get_credentials", return_value=FAKE_CREDENTIALS):
            conn1 = utils.get_connection()
            conn2 = utils.get_connection()
        assert conn1 is conn2
