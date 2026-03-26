import duckdb
import pytest

from bedrock_bio.load_dataset import load_dataset


class TestLoadDataset:
    def test_no_dataset(self):
        with pytest.raises(ValueError, match="not found in catalog"):
            load_dataset("not_a_dataset")

    def test_missing_filters(self):
        with pytest.raises(ValueError, match="Missing required filters"):
            load_dataset("dbsnp.vcf")

    def test_unknown_filter(self):
        with pytest.raises(ValueError, match="Unknown filters"):
            load_dataset(
                "dbsnp.vcf",
                build="b157",
                assembly="GRCh38",
                chromosome="22",
                fake="value",
            )

    def test_invalid_allowed_value(self):
        with pytest.raises(ValueError, match="Invalid value"):
            load_dataset("dbsnp.vcf", build="b157", assembly="INVALID", chromosome="22")

    def test_coerces_int_to_string(self):
        result = load_dataset(
            "dbsnp.vcf", build="b157", assembly="GRCh38", chromosome=22
        )
        assert isinstance(result, duckdb.DuckDBPyRelation)

    def test_coerces_case(self):
        result = load_dataset(
            "dbsnp.vcf", build="b157", assembly="grch38", chromosome="22"
        )
        assert isinstance(result, duckdb.DuckDBPyRelation)

    def test_no_filters_for_dummy_partition(self):
        result = load_dataset("ukb_ppp.assays")
        assert isinstance(result, duckdb.DuckDBPyRelation)

    def test_filters_in_query(self):
        result = load_dataset(
            "dbsnp.vcf", build="b157", assembly="GRCh38", chromosome="22"
        )
        plan = result.explain()
        assert "build" in plan
        assert "assembly" in plan
        assert "chromosome" in plan

    def test_collect(self):
        result = load_dataset(
            "dbsnp.vcf", build="b157", assembly="GRCh38", chromosome="22"
        )
        rows = result.limit(5).fetchall()
        assert len(rows) == 5

    def test_select(self):
        result = (
            load_dataset("dbsnp.vcf", build="b157", assembly="GRCh38", chromosome="22")
            .select("chromosome", "position")
            .limit(5)
        )
        assert result.columns == ["chromosome", "position"]

    def test_filter(self):
        result = load_dataset(
            "dbsnp.vcf", build="b157", assembly="GRCh38", chromosome="22"
        ).limit(5)
        rows = result.fetchall()
        assert len(rows) == 5

        chromosome_idx = result.columns.index("chromosome")
        unique_values = {row[chromosome_idx] for row in rows}
        assert unique_values == {"22"}
