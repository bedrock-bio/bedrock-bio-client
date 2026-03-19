from unittest.mock import patch

from bedrock_bio.list_datasets import list_datasets

FAKE_CATALOG = {"dataset_a": "s3://bucket/a.json", "dataset_b": "s3://bucket/b.json"}


def test_returns_dataset_names():
    with patch("bedrock_bio.list_datasets.get_catalog", return_value=FAKE_CATALOG):
        result = list_datasets()
    assert result == ["dataset_a", "dataset_b"]


def test_returns_empty_list_for_empty_catalog():
    with patch("bedrock_bio.list_datasets.get_catalog", return_value={}):
        result = list_datasets()
    assert result == []
