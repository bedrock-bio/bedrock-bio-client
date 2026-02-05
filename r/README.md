
# bedrockbio

<!-- badges: start -->
<!-- badges: end -->

A simple application programming interface (API) for querying
curated datasets from the Bedrock Bio library. The API consists of a
single user-facing function, `load_dataset()`, which takes a dataset name 
and returns a lazily-evaluated data frame object. `dplyr` verbs (`filter`, 
`select`) can be used on the returned data frame to push down row filters 
and column selections to the storage backend, downloading and reading into 
memory only the requested subset of data.

## Installation

You can install the development version of `bedrockbio` from [GitHub](https://github.com/) with:

``` r
# install.packages("pak")
pak::pak("bedrock-bio/bedrock-bio-client/r")
```

## Examples

List datasets available in the Bedrock Bio library:

```r
library(bedrockbio)
list_datasets()
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

