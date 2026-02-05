## R CMD check results

0 errors | 0 warnings | 0 notes

## Notes for CRAN

This package installs the DuckDB 'httpfs' extension on first load
to enable reading parquet files over HTTPS. This is required for
core functionality and only occurs once per user installation.

## Test environments

* local macOS (aarch64-apple-darwin), R 4.5.2
* GitHub Actions macOS-latest, R release
* GitHub Actions windows-latest, R release
* GitHub Actions ubuntu-latest, R release
* GitHub Actions ubuntu-latest, R oldrel-1
* GitHub Actions ubuntu-latest, R oldrel-2
* GitHub Actions ubuntu-latest, R oldrel-3
* GitHub Actions ubuntu-latest, R oldrel-4