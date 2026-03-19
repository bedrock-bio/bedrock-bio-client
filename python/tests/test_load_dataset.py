from unittest.mock import MagicMock, patch

import pytest

from bedrock_bio.load_dataset import load_dataset

FAKE_CATALOG = {"dataset_a": "s3://bucket/a.json"}


def test_unknown_dataset_raises_key_error():
    with patch("bedrock_bio.load_dataset.get_catalog", return_value=FAKE_CATALOG):
        with pytest.raises(KeyError, match="not_real"):
            load_dataset("not_real")


def test_passes_catalog_url_to_iceberg_scan():
    mock_conn = MagicMock()
    with (
        patch("bedrock_bio.load_dataset.get_catalog", return_value=FAKE_CATALOG),
        patch("bedrock_bio.load_dataset.get_connection", return_value=mock_conn),
    ):
        load_dataset("dataset_a")
    mock_conn.sql.assert_called_once_with(
        "SELECT * FROM iceberg_scan('s3://bucket/a.json')"
    )


def test_kwargs_apply_equality_filters():
    mock_rel = MagicMock()
    mock_conn = MagicMock()
    mock_conn.sql.return_value = mock_rel
    mock_rel.filter.return_value = mock_rel
    with (
        patch("bedrock_bio.load_dataset.get_catalog", return_value=FAKE_CATALOG),
        patch("bedrock_bio.load_dataset.get_connection", return_value=mock_conn),
    ):
        load_dataset("dataset_a", ancestry="EUR")
    mock_rel.filter.assert_called_once()
