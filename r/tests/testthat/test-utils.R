reset_pkg <- function() {
  pkg <- bedrockbio:::pkg
  pkg$catalog <- NULL
  pkg$credentials <- NULL
  if (!is.null(pkg$conn)) {
    try(DBI::dbDisconnect(pkg$conn, shutdown = TRUE), silent = TRUE)
  }
  pkg$conn <- NULL
  pkg$catalog_url <- "https://fake.test/catalog.json"
  pkg$credentials_url <- "https://fake.test/credentials.json"
}

fake_catalog <- list(
  dataset_a = "s3://bucket/a.json",
  dataset_b = "s3://bucket/b.json"
)

fake_credentials <- list(
  BB_R2_ACCOUNT_ID = "abc123",
  BB_R2_ACCESS_KEY_ID = "key123",
  BB_R2_SECRET_ACCESS_KEY = "secret123"
)


# --- get_catalog ---

test_that("get_catalog fetches from URL", {
  reset_pkg()
  local_mocked_bindings(
    fromJSON = function(...) fake_catalog,
    .package = "jsonlite"
  )
  result <- bedrockbio:::get_catalog()
  expect_equal(result, fake_catalog)
})

test_that("get_catalog caches result", {
  reset_pkg()
  call_count <- 0L
  local_mocked_bindings(
    fromJSON = function(...) {
      call_count <<- call_count + 1L
      fake_catalog
    },
    .package = "jsonlite"
  )
  bedrockbio:::get_catalog()
  bedrockbio:::get_catalog()
  expect_equal(call_count, 1L)
})

test_that("get_catalog raises error on connection failure", {
  reset_pkg()
  local_mocked_bindings(
    fromJSON = function(...) stop("connection refused"),
    .package = "jsonlite"
  )
  expect_error(
    bedrockbio:::get_catalog(),
    "Unable to access catalog URL"
  )
})


# --- get_credentials ---

test_that("get_credentials fetches from URL", {
  reset_pkg()
  local_mocked_bindings(
    fromJSON = function(...) fake_credentials,
    .package = "jsonlite"
  )
  result <- bedrockbio:::get_credentials()
  expect_equal(result, fake_credentials)
})

test_that("get_credentials caches result", {
  reset_pkg()
  call_count <- 0L
  local_mocked_bindings(
    fromJSON = function(...) {
      call_count <<- call_count + 1L
      fake_credentials
    },
    .package = "jsonlite"
  )
  bedrockbio:::get_credentials()
  bedrockbio:::get_credentials()
  expect_equal(call_count, 1L)
})

test_that("get_credentials uses env var overrides", {
  reset_pkg()
  withr::local_envvar(
    BB_R2_ACCOUNT_ID = "env_account",
    BB_R2_ACCESS_KEY_ID = "env_key",
    BB_R2_SECRET_ACCESS_KEY = "env_secret"
  )
  call_count <- 0L
  local_mocked_bindings(
    fromJSON = function(...) {
      call_count <<- call_count + 1L
      fake_credentials
    },
    .package = "jsonlite"
  )
  result <- bedrockbio:::get_credentials()
  expect_equal(call_count, 0L)
  expect_equal(result$BB_R2_ACCOUNT_ID, "env_account")
  expect_equal(result$BB_R2_ACCESS_KEY_ID, "env_key")
  expect_equal(result$BB_R2_SECRET_ACCESS_KEY, "env_secret")
})

test_that("get_credentials fetches from URL with partial env vars", {
  reset_pkg()
  withr::local_envvar(
    BB_R2_ACCOUNT_ID = "env_account",
    BB_R2_ACCESS_KEY_ID = "",
    BB_R2_SECRET_ACCESS_KEY = ""
  )
  local_mocked_bindings(
    fromJSON = function(...) fake_credentials,
    .package = "jsonlite"
  )
  result <- bedrockbio:::get_credentials()
  expect_equal(result, fake_credentials)
})

test_that("get_credentials raises error on connection failure", {
  reset_pkg()
  local_mocked_bindings(
    fromJSON = function(...) stop("connection refused"),
    .package = "jsonlite"
  )
  expect_error(
    bedrockbio:::get_credentials(),
    "Unable to fetch credentials"
  )
})


# --- get_connection ---

test_that("get_connection creates DuckDB connection with S3 secret", {
  reset_pkg()
  local_mocked_bindings(
    get_credentials = function() fake_credentials,
    .package = "bedrockbio"
  )
  conn <- bedrockbio:::get_connection()
  expect_s4_class(conn, "duckdb_connection")
  secrets <- DBI::dbGetQuery(conn, "FROM duckdb_secrets()")
  expect_equal(nrow(secrets), 1L)
  expect_equal(secrets$type, "s3")
  expect_true(grepl("r2.cloudflarestorage.com", secrets$secret_string))
})

test_that("get_connection caches connection", {
  reset_pkg()
  local_mocked_bindings(
    get_credentials = function() fake_credentials,
    .package = "bedrockbio"
  )
  conn1 <- bedrockbio:::get_connection()
  conn2 <- bedrockbio:::get_connection()
  expect_identical(conn1, conn2)
})
