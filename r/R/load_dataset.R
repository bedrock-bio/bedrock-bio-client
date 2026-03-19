#' Lazily query a dataset
#'
#' @param name Dataset identifier (e.g., "ukb_ppp.pqtls")
#' @returns A lazy `tbl` backed by DuckDB, compatible with dplyr verbs.
#'
#' @examplesIf bedrockbio:::has_connection()
#' library(bedrockbio)
#' library(dplyr)
#'
#' df <- load_dataset("ukb_ppp.pqtls") |>
#'   filter(
#'     ancestry == "EUR",
#'     protein_id == "A0FGR8"
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
#'
#' @export
load_dataset <- function(name) {
  catalog <- bedrockbio:::get_catalog()

  if (!name %in% names(catalog)) {
    stop(
      "Dataset '", name, "' not found in catalog. ",
      "See list_datasets() for available datasets.",
      call. = FALSE
    )
  }

  metadata_url <- catalog[[name]]
  query <- sprintf("SELECT * FROM iceberg_scan('%s')", metadata_url)

  conn <- bedrockbio:::get_connection()
  dplyr::tbl(conn, dplyr::sql(query))
}
