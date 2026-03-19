test_that("list_datasets returns dataset names", {
  local_mocked_bindings(
    get_catalog = function() list(dataset_a = "url_a", dataset_b = "url_b"),
    .package = "bedrockbio"
  )
  result <- list_datasets()
  expect_equal(result, c("dataset_a", "dataset_b"))
})

test_that("list_datasets returns empty for empty catalog", {
  local_mocked_bindings(
    get_catalog = function() list(),
    .package = "bedrockbio"
  )
  result <- list_datasets()
  expect_null(result)
})
