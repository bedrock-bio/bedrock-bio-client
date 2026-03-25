
# bedrock-bio

Open-Access Computational Biology Datasets

## Description

Efficiently access a curated library of open-access computational biology
datasets. Datasets support predicate pushdown and projection to the cloud
storage backend, enabling quick, iterative access to otherwise massive,
unwieldy datasets.

`bedrock_bio` consists of three user-facing functions:

- `list_datasets()`: returns a list of available dataset identifiers
- `describe_dataset('<name>')`: returns metadata, citation, and column
  definitions for a dataset
- `load_dataset('<name>', **filters)`: takes a dataset name and required
  partition filters, and returns a lazy DuckDB relation

DuckDB methods (`filter`, `select`, `limit`) can be used on the relation
returned by `load_dataset` to push down additional row filters and column
selections to the storage backend.

## Installation

To install the latest release from [PyPI](https://pypi.org/project/bedrock_bio/):

```bash
pip install bedrock-bio
```

Or install the current development version from
[GitHub](https://github.com/bedrock-bio/bedrock-bio-client):

```bash
pip install git+https://github.com/bedrock-bio/bedrock-bio-client.git@main#subdirectory=python
```

## Examples

```python
import bedrock_bio as bb
```

List available datasets:

```python
bb.list_datasets()
```

Describe a dataset to see its metadata, citation, and columns:

```python
bb.describe_dataset('ukb_ppp.pqtls')
```

Lazily load a dataset with required partition filters, select columns, and
collect into an in-memory data frame:

```python
df = bb.load_dataset('ukb_ppp.pqtls', ancestry='EUR', protein_id='A0FGR8', panel='Inflammation') \
  .select('chromosome, position, effect_allele, other_allele, beta, neg_log_10_p_value') \
  .fetchdf()
```

## Dataset Requests

To request the addition of a new dataset to the library, open an
[issue](https://github.com/bedrock-bio/bedrock-bio-client/issues).
