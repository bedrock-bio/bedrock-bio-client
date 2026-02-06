
# bedrockbio

Open-Access Computational Biology Datasets

## Description

Efficiently access a curated library of open-access computational biology 
datasets. Datasets support predicate pushdown and projection to the cloud 
storage backend, enabling quick, iterative access to otherwise massive, 
unwieldy datasets.

`bedrockbio` consists of two user-facing functions:

- `list_datasets()`: returns a list of available datasets
- `load_dataset("<name>")`: takes a dataset name and returns a lazily-evaluated
  data frame. 
  
`dplyr` verbs (`filter`, `select`) can be used on the data frame returned by
`load_dataset` to push down row filters and column selections to the storage 
backend. This means that only the requested subset of rows and columns are
downloaded and read into memory.

## Installation

To install the latest release from CRAN:

```r
install.packages("bedrockbio")
```

To install the current development version from GitHub:

```r
# install.packages("pak")
pak::pak("bedrock-bio/bedrock-bio-client/r")
```

## Examples

List available datasets:

```r
library(bedrockbio)
list_datasets()
```

Inspect the contents of a dataset before downloading and collecting into 
memory:

```r
library(bedrockbio)
load_dataset("ukb_ppp/pqtls")
```

Lazily load a dataset, filter rows, select columns, and collect the relevant
subset of the dataset into an in-memory data frame:

``` r
library(bedrockbio)
library(dplyr)
 
df <- load_dataset("ukb_ppp/pqtls") |>
  filter(
    ancestry == "EUR", 
    protein == "A0FGR8"
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
[issue on GitHub](https://github.com/bedrock-bio/bedrock-bio-client/issues).
