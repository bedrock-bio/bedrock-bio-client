#' Fetch the dataset catalog
#' @returns A named list mapping dataset names to metadata URLs.
#' @keywords internal
#' @export
get_catalog <- function() {
  if (!is.null(pkg$catalog)) {
    return(pkg$catalog)
  }

  pkg$catalog <- tryCatch(
    jsonlite::fromJSON(pkg$catalog_url),
    error = function(e) {
      stop(
        "Unable to access catalog URL '", pkg$catalog_url, "'. ",
        "Check internet connection and try again.",
        call. = FALSE
      )
    }
  )
  pkg$catalog
}

#' Fetch R2 credentials
#' @returns A named list of credential values.
#' @keywords internal
#' @export
get_credentials <- function() {
  if (!is.null(pkg$credentials)) {
    return(pkg$credentials)
  }

  override_credentials <- list(
    BB_R2_ACCOUNT_ID = Sys.getenv("BB_R2_ACCOUNT_ID"),
    BB_R2_ACCESS_KEY_ID = Sys.getenv("BB_R2_ACCESS_KEY_ID"),
    BB_R2_SECRET_ACCESS_KEY = Sys.getenv("BB_R2_SECRET_ACCESS_KEY")
  )

  pkg$credentials <- if (all(nzchar(override_credentials))) {
    override_credentials
  } else {
    tryCatch(
      jsonlite::fromJSON(pkg$credentials_url),
      error = function(e) {
        stop(
          "Unable to fetch credentials from '", pkg$credentials_url, "'. ",
          "Check internet connection and try again.",
          call. = FALSE
        )
      }
    )
  }
  pkg$credentials
}

#' Get a DuckDB connection configured for R2
#' @returns A DuckDB connection object.
#' @keywords internal
#' @export
get_connection <- function() {
  if (!is.null(pkg$conn)) {
    return(pkg$conn)
  }

  credentials <- get_credentials()
  pkg$conn <- DBI::dbConnect(duckdb::duckdb())

  DBI::dbExecute(pkg$conn, sprintf(
    "CREATE SECRET (
      TYPE s3,
      KEY_ID '%s',
      SECRET '%s',
      ENDPOINT '%s.r2.cloudflarestorage.com',
      URL_STYLE 'path'
    )",
    credentials$BB_R2_ACCESS_KEY_ID,
    credentials$BB_R2_SECRET_ACCESS_KEY,
    credentials$BB_R2_ACCOUNT_ID
  ))

  pkg$conn
}

#' Check if a connection can be established
#' @returns `TRUE` if a connection is available, `FALSE` otherwise.
#' @keywords internal
#' @export
has_connection <- function() {
  tryCatch(
    {
      get_connection()
      TRUE
    },
    error = function(e) FALSE
  )
}
