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
  catalog_url = "https://data.bedrock.bio/catalog.json"
  jsonlite::fromJSON(catalog_url)$datasets
}