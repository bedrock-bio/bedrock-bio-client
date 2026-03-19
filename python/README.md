
# bedrock-bio

Open-Access Computational Biology Datasets

## Description

Efficiently access a curated library of open-access computational biology
datasets. Datasets support predicate pushdown and projection to the cloud
storage backend, enabling quick, iterative access to otherwise massive,
unwieldy datasets.

`bedrock_bio` consists of two user-facing functions:

- `list_datasets()`: returns a list of available datasets
- `load_dataset('<name>')`: takes a dataset name and returns a lazy DuckDB
  relation.

DuckDB methods (`filter`, `select`, `limit`) can be used on the relation
returned by `load_dataset` to push down row filters and column selections to
the storage backend. This means that only a subset of rows and columns need to
be actually downloaded and read into memory.

## Installation

To install the latest release from [PyPI](https://pypi.org/project/bedrock_bio/):

```bash
pip install bedrock-bio
```

To install the current development version from
[GitHub](https://github.com/bedrock-bio/bedrock-bio-client/python):

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

Lazily load a dataset:

```python
rel = bb.load_dataset('ukb_ppp.pqtls')
```

Inspect the columns of a dataset before downloading:

```python
print(rel.columns)
```

Load with equality filters, then project and collect into an in-memory data
frame:

```python
df = bb.load_dataset('ukb_ppp.pqtls', ancestry='EUR', protein_id='A0FGR8') \
  .select('chromosome, position, effect_allele, other_allele, beta, neg_log_10_p_value') \
  .fetchdf()
```

## Dataset Requests

To request the addition of a new dataset to the library, open an
[issue](https://github.com/bedrock-bio/bedrock-bio-client/issues).
