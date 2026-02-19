
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
backend. This means that only a subset of rows and columns need to be actually
downloaded and read into memory.

## Installation

To install the latest release from [R-multiverse](https://community.r-multiverse.org/bedrockbio):

```r
Sys.setenv(NOT_CRAN = 'true');
install.packages('bedrockbio', repos = c('https://community.r-multiverse.org', 'https://cloud.r-project.org'))
```

To install the current development version from 
[GitHub](https://github.com/bedrock-bio/bedrock-bio-client/r):

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

Inspect the contents of a dataset before downloading and collecting into 
memory:

```r
load_dataset("ukb_ppp/pqtls") |>
  head() |>
  collect()
```

Lazily load a dataset, filter rows, select columns, and collect the relevant
subset into an in-memory data frame:

```r
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
[issue](https://github.com/bedrock-bio/bedrock-bio-client/issues).
