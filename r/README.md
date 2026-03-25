
# bedrockbio

Open-Access Computational Biology Datasets

## Description

Efficiently access a curated library of open-access computational biology
datasets. Datasets support predicate pushdown and projection to the cloud
storage backend, enabling quick, iterative access to otherwise massive,
unwieldy datasets.

`bedrockbio` consists of three user-facing functions:

- `list_datasets()`: returns a character vector of available dataset identifiers
- `describe_dataset("<name>")`: returns metadata, citation, and column
  definitions for a dataset
- `load_dataset("<name>", ...)`: takes a dataset name and required partition
  filters, and returns a lazily-evaluated data frame

`dplyr` verbs (`filter`, `select`) can be used on the data frame returned by
`load_dataset` to push down additional row filters and column selections to the
storage backend.

## Installation

Install from [CRAN](https://cran.r-project.org/):

```r
install.packages("bedrockbio")
```

Or install the current development version from
[GitHub](https://github.com/bedrock-bio/bedrock-bio-client):

```r
# install.packages("pak")
pak::pak("bedrock-bio/bedrock-bio-client/r")
```

## Examples

Load the package (and `dplyr` for downstream data frame manipulation):

```r
library(bedrockbio)
library(dplyr)
```

List available datasets:

```r
list_datasets()
```

Describe a dataset to see its metadata, citation, and columns:

```r
describe_dataset("ukb_ppp.pqtls")
```

Lazily load a dataset with required partition filters, select columns, and
collect the relevant subset into an in-memory data frame:

```r
df <- load_dataset(
  "ukb_ppp.pqtls",
  ancestry = "EUR",
  protein_id = "A0FGR8",
  panel = "Inflammation"
) |>
  select(
    chromosome,
    position,
    effect_allele,
    other_allele,
    beta,
    neg_log_10_p_value
  ) |>
  collect()
```

## Dataset Requests

To request the addition of a new dataset to the library, open an
[issue](https://github.com/bedrock-bio/bedrock-bio-client/issues).
