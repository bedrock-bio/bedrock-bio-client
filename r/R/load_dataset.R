#' Lazily read a dataset from the Bedrock Bio library
#'
#' @param name Dataset name (e.g., "ukb_ppp/pqtls")
#' @return A lazy dplyr table
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
#'    ) |>
#'   select(
#'     chromosome, 
#'     position, 
#'     effect_allele, 
#'     other_allele, 
#'     beta, 
#'     neg_log_10_p_value
#'    ) |>
#'    collect()
#' }
#' 
#' @export
load_dataset <- function(name) {
  base_url <- "https://data.bedrock.bio"
  manifest_url <- paste0(base_url, "/manifests/", name, ".json")
  
  files <- jsonlite::fromJSON(manifest_url)$files
  urls <- paste0(base_url, "/", name, "/", files)
  
  sink(nullfile())
  conn <- DBI::dbConnect(duckdb::duckdb())
  sink()
  
  DBI::dbExecute(conn, "LOAD httpfs")
  DBI::dbExecute(conn, "SET enable_progress_bar = false")
  
  query <- paste0(
    "SELECT * FROM read_parquet([", 
    paste0("'", urls, "'", collapse=", "), 
    "], hive_partitioning=true)"
  )
  
  dplyr::tbl(conn, dplyr::sql(query))
}