import pytest

from bedrock_bio.describe_dataset import describe_dataset


class TestDescribeDataset:
    def test_no_dataset(self):
        with pytest.raises(ValueError, match="not found in catalog"):
            describe_dataset("not_a_dataset")

    def test_returns_expected_keys(self):
        result = describe_dataset("ukb_ppp.pqtls")
        assert result["name"] == "ukb_ppp.pqtls"
        assert isinstance(result["description"], str)
        assert len(result["description"]) > 0
        assert isinstance(result["citation"], dict)
        assert isinstance(result["source_url"], str)
        assert isinstance(result["license"], str)
        assert isinstance(result["columns"], list)
        assert len(result["columns"]) > 0

    def test_columns_have_expected_fields(self):
        result = describe_dataset("dbsnp.vcf")
        for col in result["columns"]:
            assert "name" in col
            assert "type" in col
            assert "description" in col
