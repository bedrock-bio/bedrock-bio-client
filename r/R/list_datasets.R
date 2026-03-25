#' List available datasets in the Bedrock Bio library
#'
#' @returns A character vector of dataset identifiers
#'
#' @examplesIf bedrockbio:::has_connection()
#' library(bedrockbio)
#' list_datasets()
#'
#' @export
list_datasets <- function() {
  catalog <- get_catalog()
  names(catalog)
}
