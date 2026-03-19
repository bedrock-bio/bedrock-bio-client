pkg <- new.env(parent = emptyenv())

.onLoad <- function(libname, pkgname) {
  pkg$domain <- Sys.getenv("BB_R2_DOMAIN", "data.bedrock.bio")
  pkg$catalog_url <- paste0("https://", pkg$domain, "/catalog.json")
  pkg$credentials_url <- paste0("https://", pkg$domain, "/credentials.json")
}

.onUnload <- function(libpath) {
  if (!is.null(pkg$conn)) {
    DBI::dbDisconnect(pkg$conn, shutdown = TRUE)
  }
}
