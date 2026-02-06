#' List available datasets in the Bedrock Bio library
#'
#' @return A character vector of dataset names
#'
#' @examples
#' \dontrun{
#' library(bedrockbio)
#' list_datasets()
#' }
#'
#' @export
list_datasets <- function() {
  catalog_url <- "https://data.bedrock.bio/catalog.json"

  error_msg <- paste0(
    "Unable to access catalog URL '",
    catalog_url,
    "'. Check internet connection and try again."
  )

  tryCatch(
    jsonlite::fromJSON(catalog_url)$datasets,
    error = function(e) {
      stop(error_msg, call. = FALSE)
    }
  )
}
