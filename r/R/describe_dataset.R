#' Describe a dataset's metadata, citation, and columns
#'
#' @param name Dataset identifier (e.g., "ukb_ppp.pqtls")
#' @returns A named list with name, description, citation, source_url,
#'   license, and columns.
#'
#' @examplesIf bedrockbio:::has_connection()
#' library(bedrockbio)
#' info <- describe_dataset("ukb_ppp.pqtls")
#' info$name
#'
#' @export
describe_dataset <- function(name) {
  catalog <- get_catalog()

  if (!name %in% names(catalog)) {
    stop(
      "Dataset '", name, "' not found in catalog. ",
      "See list_datasets() for available datasets.",
      call. = FALSE
    )
  }

  entry <- catalog[[name]]
  list(
    name = name,
    description = entry$description,
    citation = entry$citation,
    source_url = entry$source_url,
    license = entry$license,
    columns = entry$columns
  )
}
