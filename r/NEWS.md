# bedrockbio 1.2.0

* Initial CRAN submission.
* `list_datasets()`: list available datasets.
* `load_dataset()`: lazily query a dataset with required partition filters and
  predicate pushdown via 'DuckDB' and 'Apache Iceberg'.
* `describe_dataset()`: view dataset metadata, citation, and column definitions.
