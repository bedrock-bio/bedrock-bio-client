skip_on_cran()

test_that("list_datasets returns a character vector", {
  result <- list_datasets()
  expect_type(result, "character")
})
