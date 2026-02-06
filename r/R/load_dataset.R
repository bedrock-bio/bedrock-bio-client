#' Lazily read a dataset from the Bedrock Bio library
#'
#' @param name Dataset name (e.g., "ukb_ppp/pqtls")
#' @return A lazy tibble
#'
#' @examples
#' \dontrun{
#' library(bedrockbio)
#' library(dplyr)
#'
#' df <- load_dataset("ukb_ppp/pqtls") |>
#'   filter(
#'     ancestry == "EUR",
#'     protein == "A0FGR8"
#'   ) |>
#'   select(
#'     chromosome,
#'     position,
#'     effect_allele,
#'     other_allele,
#'     beta,
#'     neg_log_10_p_value
#'   ) |>
#'   collect()
#' }
#'
#' @export
load_dataset <- function(name) {
  base_url <- "https://data.bedrock.bio"
  manifest_url <- paste0(base_url, "/", name, "/manifest.json")

  error_msg <- paste0(
    "Unable to access manifest URL '",
    manifest_url,
    "' for dataset '",
    name,
    "'. Check internet connection and try again."
  )

  files <- tryCatch(
    jsonlite::fromJSON(manifest_url)$files,
    error = function(e) {
      stop(error_msg, call. = FALSE)
    }
  )

  urls <- paste0(base_url, "/", files)
  tidypolars::scan_parquet_polars(urls, hive_partitioning = TRUE)
}
