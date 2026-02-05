.onLoad <- function(libname, pkgname) {
  conn <- DBI::dbConnect(duckdb::duckdb())
  on.exit(DBI::dbDisconnect(conn))

  tryCatch(
    {
      DBI::dbExecute(conn, "INSTALL httpfs")
    },
    error = function(e) {}
  )
}
